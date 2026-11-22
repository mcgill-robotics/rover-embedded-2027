"""
These tests are meant to simulate actual usage. They incorporate
real mosquitto communication and a virtual CAN bus. 

These need Mosquitto installed (see conftest.py) and get skipped otherwise.
"""

import queue
import threading
import uuid

import can
import paho.mqtt.client as mqtt
import pytest

from rover_embedded.arm.esc_can.can_mqtt import (
        RX_TOPIC_FILTER,
        CanMqttBridge,
        rx_topic,
        tx_topic,
        )

WAIT = 2  # seconds, stays under the 5s pytest-timeout


def _connected_client(host, port) -> tuple[mqtt.Client, threading.Event]:
    "A plain ham sandwich MQTT client standing in for the UI."
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # Weird, overkill status tracking.
    connected = threading.Event()
    client.on_connect = lambda *args: connected.set()
    # Connect to the MQTT business through TCP.
    client.connect(host, port)
    # Read packets, and trigger callbacks when necessary.
    client.loop_start()
    assert connected.wait(WAIT), "test client could not connect"
    return client, connected


@pytest.fixture
def bridge_setup(mqtt_broker):
    """
    Sets up the broker and virtual CAN bus.
    """
    host, port = mqtt_broker
    channel = f"test-{uuid.uuid4()}"  # fresh virtual bus per test
    # Connect two nodes to the same bus
    bridge_bus = can.Bus(interface="virtual", channel=channel)
    arm_bus = can.Bus(interface="virtual", channel=channel)

    # The bridge itself is an MQTT client yknow:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    subscribed = threading.Event()
    client.on_subscribe = lambda *args: subscribed.set()  # bridge doesn't use this hook

    # Link the bridge virtual CAN with this new MQTT client
    bridge = CanMqttBridge(bridge_bus, client)
    bridge.start(host, port)
    runner = threading.Thread(target=bridge.run, daemon=True)
    runner.start()
    assert subscribed.wait(WAIT), "bridge never subscribed to the TX topics"

    # Yield the arm bus, because this is the only thing that the tests need.
    yield arm_bus

    bridge.stop()
    runner.join(timeout=WAIT)
    bridge_bus.shutdown()
    arm_bus.shutdown()


# MQTT command -> CAN frame on the bus.
def test_tx_topic_becomes_can_frame(mqtt_broker, bridge_setup):
    arm_bus = bridge_setup
    ui, _ = _connected_client(*mqtt_broker)
    try:
        ui.publish(tx_topic(0x131), "deadbeef").wait_for_publish(WAIT)
        frame = arm_bus.recv(timeout=WAIT)
    finally:
        ui.disconnect()
        ui.loop_stop()

    assert frame is not None, "no frame reached the bus"
    assert frame.arbitration_id == 0x131
    assert bytes(frame.data) == bytes.fromhex("deadbeef")
    assert not frame.is_fd


# CAN frame from the arm -> MQTT message on the RX topic.
def test_can_frame_becomes_rx_message(mqtt_broker, bridge_setup):
    arm_bus = bridge_setup
    ui, _ = _connected_client(*mqtt_broker)
    received = queue.Queue()
    subscribed = threading.Event()
    ui.on_message = lambda c, u, msg: received.put(msg)
    ui.on_subscribe = lambda *args: subscribed.set()
    try:
        ui.subscribe(RX_TOPIC_FILTER)
        assert subscribed.wait(WAIT)
        arm_bus.send(can.Message(arbitration_id=0x07F, data=b"\x01\x02\x03",
                                 is_extended_id=False))
        msg = received.get(timeout=WAIT)
    finally:
        ui.disconnect()
        ui.loop_stop()

    assert msg.topic == rx_topic(0x07F)
    assert msg.payload.decode() == "010203"


# Garbage payloads get dropped, and the bridge keeps working afterwards.
def test_malformed_tx_is_dropped(mqtt_broker, bridge_setup):
    arm_bus = bridge_setup
    ui, _ = _connected_client(*mqtt_broker)
    try:
        ui.publish(tx_topic(0x131), "not hex!").wait_for_publish(WAIT)
        ui.publish(tx_topic(0x132), "00").wait_for_publish(WAIT)
        frame = arm_bus.recv(timeout=WAIT)
    finally:
        ui.disconnect()
        ui.loop_stop()

    # Messages from one publisher arrive in order, so if the bad one had made
    # it through it would show up first.
    assert frame is not None
    assert frame.arbitration_id == 0x132
