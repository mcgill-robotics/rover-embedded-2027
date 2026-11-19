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

RX_TOPIC_PREFIX = "arm/can/rx"
TX_TOPIC_PREFIX = "arm/can/tx"

TX_TOPIC_FILTER = f"{TX_TOPIC_PREFIX}/+"
RX_TOPIC_FILTER = f"{RX_TOPIC_PREFIX}/+"

def rx_topic(arb_id: int) -> str:
    "This is a helper function, returning a consistent topic name."
    "0x7F -> prefix/07F"
    return f"{RX_TOPIC_PREFIX}/{arb_id:03X}"

def tx_topic(arb_id: int) -> str:
    "Same deal"
    return f"{TX_TOPIC_PREFIX}/{arb_id:03X}"

def topic_arb_id(topic: str) -> int:
    "The counterspell to the above two, 'arm/can/tx/131' -> 0x131."
    return int(topic.rsplit("/", 1)[-1], 16)


"Moving on to the actual contract code"

