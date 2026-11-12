# Design Document

RX flow

1. Read into a circular buffer (in contiguous bits)

2. Process through Cobs

3. Output to another circular buffer (contiguous bits)

4. Byte by Byte decode of header

5. Callback to request memory to store payload

6. Callback to write the data to the passed memory 

TX flow

1. Write is called

2. Packet is in a fixed size temp buffer

3. Packet is COBS encoded into a circular buffer

4. Writes read from the circular buffer and output from there (packet boundaries do not matter here, if a packet gets corrupted from overwriting then COBS should detect the issue and resynchronize)

Multiplexing Module?
