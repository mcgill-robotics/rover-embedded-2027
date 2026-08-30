#ifndef TINYUBX_H
#define TINYUBX_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stdint.h>

// Byte-at-a-time parser for u-blox's UBX binary protocol, decoding only the NAV-PVT message (position, velocity, time). 
// - Frame layout: [SYNC1][SYNC2][class][id][len_lo][len_hi][payload...][ck_a][ck_b]
// - ck_a/ck_b are an 8-bit running checksum over class
// - ubx_nav_pvt_t mirrors the NAV-PVT payload byte-for-byte

#define UBX_MAX_PAYLOAD 128

#define UBX_SYNC1 0xB5
#define UBX_SYNC2 0x62

#define UBX_CLASS_NAV 0x01
#define UBX_NAV_PVT   0x07

typedef enum {
    UBX_STATE_SYNC1 = 0,
    UBX_STATE_SYNC2,
    UBX_STATE_CLASS,
    UBX_STATE_ID,
    UBX_STATE_LEN1,
    UBX_STATE_LEN2,
    UBX_STATE_PAYLOAD,
    UBX_STATE_CK_A,
    UBX_STATE_CK_B,
} ubx_state_t;

typedef struct {
    ubx_state_t state;
    uint8_t  msg_class;
    uint8_t  msg_id;
    uint16_t length;          // Payload length declared by the frame header
    uint16_t count;           // Payload bytes consumed so far
    bool     oversized;       // length > UBX_MAX_PAYLOAD, bytes counted but not stored
    uint8_t  ck_a, ck_b;
    uint8_t  payload[UBX_MAX_PAYLOAD];
    uint32_t frames_ok;       // Passed checksum and fit in payload[]
    uint32_t frames_crc_err;  // Failed the ck_a/ck_b check
    uint32_t frames_oversize; // Declared length exceeded UBX_MAX_PAYLOAD
} ubx_parser_t;

typedef struct __attribute__((packed)) {
    uint32_t iTOW;    // ms
    uint16_t year;    // UTC
    uint8_t  month;   // UTC 1-12
    uint8_t  day;     // UTC 1-31
    uint8_t  hour;    // UTC 0-23
    uint8_t  min;     // UTC 0-59
    uint8_t  sec;     // UTC 0-60
    uint8_t  valid;
    uint32_t tAcc;    // ns
    int32_t  nano;    // ns -1e9-1e9
    uint8_t  fixType; // 0=no fix, 1=dead reckoning, 2=2D, 3=3D, 4=GNSS+DR, 5=time only
    uint8_t  flags;   // bit 0 = gnssFixOK (fix considered valid by the receiver)
    uint8_t  flags2;
    uint8_t  numSV;
    int32_t  lon;     // deg * 1e-7
    int32_t  lat;     // deg * 1e-7
    int32_t  height;  // mm above ellipsoid
    int32_t  hMSL;    // mm above MSL
    uint32_t hAcc;    // mm
    uint32_t vAcc;    // mm
    int32_t  velN;    // mm/s
    int32_t  velE;    // mm/s
    int32_t  velD;    // mm/s
    int32_t  gSpeed;  // mm/s 2D ground speed
    int32_t  headMot; // deg * 1e-5, heading of motion
    uint32_t sAcc;    // mm/s
    uint32_t headAcc; // deg * 1e-5
    uint16_t pDOP;
    uint16_t flags3;
    uint8_t  reserved0[4];
    int32_t  headVeh; // deg * 1e-5, heading of vehicle
    int16_t  magDec;  // deg * 1e-2
    uint16_t magAcc;  // deg * 1e-2
} ubx_nav_pvt_t;

// Feeds one byte into the parser, returns true only on a checksum-valid
// NAV-PVT frame of exactly sizeof(ubx_nav_pvt_t) bytes, with *data filled in.
bool ubx_process(ubx_parser_t *p, ubx_nav_pvt_t *data, uint8_t byte);

#ifdef __cplusplus
}
#endif

#endif