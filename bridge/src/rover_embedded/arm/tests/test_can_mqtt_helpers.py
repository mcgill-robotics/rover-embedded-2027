""" 
Hello peeps, this is a test file to make sure the basic things in my can_mqtt.py file work.
"""

import pytest

# Importing all the needed constants and functions.
from rover_embedded.arm.esc_can.can_mqtt import (
        RX_TOPIC_FILTER,
        TX_TOPIC_FILTER,
        rx_topic,
        topic_arb_id,
        tx_topic,
        )

# Defining my test data and labelling it clearly.
@pytest.mark.parametrize(
    "arb_id, expected_suffix",
    [
        (0x000, "000"),
        (0x07F, "07F"),   
        (0x131, "131"),
        (0x7FF, "7FF"),  
    ],
)

# Testing the topic formatting functions.
def test_topics_format_arb_id_as_three_digit_uppercase_hex(arb_id, expected_suffix):
    assert rx_topic(arb_id) == f"arm/can/rx/{expected_suffix}"
    assert tx_topic(arb_id) == f"arm/can/tx/{expected_suffix}"

# Testing consistent behavior between the tx and rx formatting functions.
def test_rx_and_tx_topics_differ_only_by_direction():
    assert rx_topic(0x131).replace("/rx/", "/tx/") == tx_topic(0x131)

# This makes sure that converting an ID to a topic and then back to an ID 
# keeps the original ID.
@pytest.mark.parametrize("arb_id", [0x000, 0x001, 0x07F, 0x131, 0x7FF])
def test_topic_arb_id_reverses_rx_and_tx_topic(arb_id):
    assert topic_arb_id(rx_topic(arb_id)) == arb_id
    assert topic_arb_id(tx_topic(arb_id)) == arb_id

# This does the above test but for every possible 11-bit ID.
def test_round_trip_holds_for_every_11_bit_id():
    for arb_id in range(0x800):
        assert topic_arb_id(tx_topic(arb_id)) == arb_id

# It's in the name.
def test_topic_arb_id_accepts_lowercase_hex():
    assert topic_arb_id("arm/can/tx/07f") == 0x07F

# This makes sure that the topic filters are applied correctly. 
def test_wildcard_filters_match_the_helper_topics_prefix():
    assert TX_TOPIC_FILTER == "arm/can/tx/+"
    assert RX_TOPIC_FILTER == "arm/can/rx/+"
    assert tx_topic(0x131).startswith(TX_TOPIC_FILTER[:-1])
    assert rx_topic(0x131).startswith(RX_TOPIC_FILTER[:-1])

