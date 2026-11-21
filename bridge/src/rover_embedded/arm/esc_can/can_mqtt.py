"""
This file is for reading the serial port of the CANable and
forwarding the data to the MQTT bus.

This file is dumb ("ooga booga" ahhh). It does not do any thinking work,
that is the job of other files.

Here are the two topics:
    arm/can/rx/<id>
    arm/can/tx/<id>

Upstream files can subscribe to these and filter the incoming firehose
with a bit mask if they wish to do so.

The payload of the MQTT message is just the data in hex. 
"""

from __future__ import annotations

import logging
import threading

import can
import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)

RX_TOPIC_PREFIX = "arm/can/rx"
TX_TOPIC_PREFIX = "arm/can/tx"

TX_TOPIC_FILTER = f"{TX_TOPIC_PREFIX}/+"
RX_TOPIC_FILTER = f"{RX_TOPIC_PREFIX}/+"

DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883

def rx_topic(arb_id: int) -> str:
    "This is a helper function, returning a consistent topic name."
    return f"{RX_TOPIC_PREFIX}/{arb_id:03X}"

def tx_topic(arb_id: int) -> str:
    "Same deal"
    return f"{TX_TOPIC_PREFIX}/{arb_id:03X}"

def topic_arb_id(topic: str) -> int:
    "The counterspell to the above two, 'arm/can/tx/131' -> 0x131."
    return int(topic.rsplit("/", 1)[-1], 16)

class CanMqttBridge:
    """
    This unit of code has two jobs.

    Job One: The bus messages go to the RX topic
    Job Two: The TX topic messages go to the bus

    These jobs are separated into separate threads so as to not block anything.
    """
    
    # Initialize and set properties that other things should not change nor access
    def __init__(self, bus: can.BusABC, client: mqtt.Client,
                 *, qos: int = 0, retain: bool = False) -> None:
        self._bus = bus
        self._client = client
        self._qos = qos
        self._retain = retain
        self._stop = threading.Event()

        client.on_connect = self._on_connect
        client.on_message = self._on_message


    # On connection to the broker, subscribe to the TX filter i.e. the arm commands
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            log.error("MQTT connect failed: %s", reason_code)
            return
        client.subscribe(TX_TOPIC_FILTER, qos=self._qos)
        log.info("Connected to broker, listening on %s", TX_TOPIC_FILTER)

    # When it receives an arm command, it extracts the data/id + wraps it in a CAN frame, then sends it on the Bus.
    def _on_message(self, client, userdata, message):
        try:
            data = bytes.fromhex(message.payload.decode())
            is_fd = len(data) > 8   # longer than 8 bytes cannot be classic
            frame = can.Message(
                arbitration_id=topic_arb_id(message.topic),
                data=data,
                is_fd=is_fd,
                bitrate_switch=is_fd,
            )
        except (UnicodeDecodeError, ValueError):
            log.warning("Dropping malformed TX on %s: %r",
                        message.topic, message.payload)
            return

        try:
            self._bus.send(frame)
        except can.CanError as exc:
            log.error("Bus TX failed on %s: %s", message.topic, exc)


    # When it's starting, it chooses the default host/port to search for the broker on.
    # This might need configuring but it fits the Mosquitto default behavior.
    def start(self, host: str = DEFAULT_MQTT_HOST,
              port: int = DEFAULT_MQTT_PORT) -> None:
        self._client.connect(host, port)
        self._client.loop_start()

    # This is looping behavior. "Dormammu I've come to bargain" ahhh.
    # The 0.5s timeout is for checking the stop flag, both sending/receiving messages is smooth. 
    def run(self) -> None:
        """Block until stop(). Forwards every frame the bus receives."""
        while not self._stop.is_set():
            msg = self._bus.recv(timeout=0.5)
            if msg is None:
                continue
            self._client.publish(rx_topic(msg.arbitration_id),
                                 msg.data.hex(),
                                 qos=self._qos, retain=self._retain)

    def stop(self) -> None:
        self._stop.set()
        self._client.disconnect()
        self._client.loop_stop()
