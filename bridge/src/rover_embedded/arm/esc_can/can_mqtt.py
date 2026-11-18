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

"""
