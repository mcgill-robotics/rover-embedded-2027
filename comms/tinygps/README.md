# TinyGPS STM32 Port

C/C++ GPS library port of TinyGPS for STM32G4 (HAL). Supports both UXB-NAV-PVT and standard NMEA GPS protocols.

---

## Data Structures

### `gps_data_t`

Holds a complete position snapshot.

| Field | Type | Unit | Description |
| ----- | ---- | ---- | ----------- |
| `lat` | `double` | degrees | Latitude (positive = North) |
| `lon` | `double` | degrees | Longitude (positive = East) |
| `alt` | `double` | metres | Altitude above mean sea level |
| `gSpeed` | `double` | m/s | Ground speed |
| `headMot` | `double` | degrees | Heading of motion (0 = North) |
| `numSV` | `int` | - | Number of satellites used |
| `fixType` | `int` | - | Fix type (0 = none, 1 = dead reckoning, 2 = 2D, 3 = 3D) |

### `gps_t`

Internal GPS state. Declare one per physical receiver. Do not access fields directly, use the API functions below.

---

## API

### `gps_init`

```c
void gps_init(gps_t *g, int type, UART_HandleTypeDef *huart, bool use_ekf);
```

Initializes the GPS instance and reconfigures the UART baud rate automatically:

- `GPS_UBX` uses 115200 baud (new M10G-5883 is pre-configured for this baud rate)
- `GPS_NMEA` uses 9600 baud (old GPS uses slower baud rate)

Call this after `HAL_Init()` and peripheral init, before starting UART interrupts.

`use_ekf = true` enables the Kalman filter.

---

### `gps_process`

```c
bool gps_process(gps_t *g, uint8_t byte);
```

Feeds one byte into the parser. Returns `true` when a complete, valid frame with a fix has been parsed. Not interrupt-safe with itself: don't call it concurrently for the same `gps_t` from both an ISR and the main loop. See [Feeding bytes to the parser](#feeding-bytes-to-the-parser) below for the two ways to call it.

---

### `gps_read_snapshot`

```c
bool gps_read_snapshot(gps_t *g, gps_data_t *out);
```

Reads the latest position snapshot from the main loop. Returns `true` if a new frame is available since the last call. Thread-safe since it disables IRQs during copy.

---

### `gps_read_combined`

```c
bool gps_read_combined(gps_t *a, gps_t *b, gps_data_t *out);
```

Fuses two GPS receivers into one `gps_data_t`. Weighted average by `numSV` for position, altitude, speed, and heading. `fixType` uses the pessimistic (lower) value. `numSV` is summed.

Fallback behavior:

- If only one receiver has a new frame, it returns that one unmodified.
- If neither has a new frame, it returns `false`.

---

## Kalman Filter

The EKF models position as static (`F = I`) with a direct measurement (`H = I`).
It is seeded automatically on the first valid fix, so no warm-up drift occurs.

**Process noise (`Q_VAL`)** controls the smoothing/tracking trade-off:

| Value | Behaviour |
| ----- | --------- |
| `1e-12` | Heavy smoothing. Best static accuracy, slow to track fast motion. |
| `1e-10` | Default. Good balance for slow-moving rovers. |
| `1e-8` | Light smoothing. Tracks fast motion, minimal noise reduction. |

Change `Q_VAL` in `tinygps.cpp` → `apply_ekf()`.

**Measurement noise (`R`)** is built automatically from the receiver's reported
horizontal accuracy: `hAcc` for UBX, or an accuracy estimate derived from HDOP
for NMEA (HDOP is not itself a distance, so it's scaled by a fixed 5 m-per-HDOP-unit
assumption to approximate one). No manual tuning needed.

---

## Integration in `main.c`

### Feeding bytes to the parser

`gps_process()` just needs one byte at a time; it doesn't care where they come from.
Two common ways to feed it, trading ISR overhead against RAM:

#### Byte-at-a-time (simplest)

`HAL_UART_Receive_IT` re-arms for a single byte every time it fires, running
`gps_process()` once per byte directly inside the UART RX interrupt. Easiest to
wire up, but at 115200 baud that's an interrupt roughly every 87 µs.

#### 1. Declare variables

```c
gps_t gps_1;
static uint8_t gps_1_byte;
```

#### 2. Initialize

```c
gps_init(&gps_1, GPS_UBX, &huart4, true);
HAL_UART_Receive_IT(gps_1.huart, &gps_1_byte, 1);
```

#### 3. Feed bytes

```c
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart == gps_1.huart) {
        gps_process(&gps_1, gps_1_byte);
        HAL_UART_Receive_IT(gps_1.huart, &gps_1_byte, 1);
    }
}
```

#### 4. Read in the main loop

```c
gps_data_t data;
if (gps_read_snapshot(&gps_1, &data)) {
    // use data.lat, data.lon, data.alt, etc.
}
```

---

#### Buffered, processed in the main loop (recommended)

`HAL_UARTEx_ReceiveToIdle_IT` captures a whole burst into a buffer and interrupts
once per line-idle (or buffer-full), not once per byte. The ISR just records how
many bytes arrived and hands off the buffer; per-byte parsing runs in the main loop.

Two buffers swap ping-pong style so the UART can keep receiving into one while the
main loop works through the other.

#### 1. Declare variables

```c
#define GPS_BUFFER_SIZE (UBX_MAX_PAYLOAD)   // one full UBX payload's worth of bytes

gps_t gps;
static uint8_t gps_buffers[2][GPS_BUFFER_SIZE];
static int buffer_sizes[2];
static volatile int gps_index = 0;   // buffer currently armed for reception
static int gps_ready[2] = {0, 0};    // buffers holding unprocessed bytes
```

#### 2. Initialize

```c
gps_init(&gps, GPS_UBX, &huart3, true);
HAL_UARTEx_ReceiveToIdle_IT(gps.huart, gps_buffers[gps_index], GPS_BUFFER_SIZE);
```

#### 3. Capture bytes in the background

The RX-event callback fires on idle-line or buffer-full: it marks the filled
buffer ready, flips to the other one, and re-arms reception immediately. Also
re-arm on `HAL_UART_ErrorCallback`, or a framing/overrun error leaves reception dead.

```c
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size) {
    if (huart == gps.huart) {
        buffer_sizes[gps_index] = Size;
        gps_ready[gps_index] = 1;
        gps_index = (gps_index == 0) ? 1 : 0;
        HAL_UARTEx_ReceiveToIdle_IT(gps.huart, gps_buffers[gps_index], GPS_BUFFER_SIZE);
    }
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart) {
    if (huart == gps.huart) {
        HAL_UARTEx_ReceiveToIdle_IT(gps.huart, gps_buffers[gps_index], GPS_BUFFER_SIZE);
    }
}
```

#### 4. Parse and read in the main loop

`gps_index` points at the buffer the UART is *currently* filling, so parse the other one.

```c
while (1) {
    if (gps_ready[0] || gps_ready[1]) {
        int filled_index = (gps_index == 0) ? 1 : 0;
        if (gps_ready[filled_index]) {
            uint8_t *buf = gps_buffers[filled_index];
            for (int i = 0; i < buffer_sizes[filled_index]; i++) gps_process(&gps, buf[i]);
            gps_ready[filled_index] = 0;
        }
    }

    gps_data_t data;
    if (gps_read_snapshot(&gps, &data)) {
        // use data.lat, data.lon, data.alt, etc.
    }
}
```

---

#### Dual GPS

Add a second UART peripheral in CubeMX first, then regenerate. Apply the same
buffered pattern independently to each receiver, keyed off `huart` in the shared
callbacks:

```c
gps_t gps_1, gps_2;
static uint8_t gps_1_buffers[2][GPS_BUFFER_SIZE], gps_2_buffers[2][GPS_BUFFER_SIZE];
static int gps_1_sizes[2], gps_2_sizes[2];
static volatile int gps_1_index = 0, gps_2_index = 0;
static int gps_1_ready[2] = {0, 0}, gps_2_ready[2] = {0, 0};

gps_init(&gps_1, GPS_UBX, &huart3, true);
gps_init(&gps_2, GPS_UBX, &huart4, true);
HAL_UARTEx_ReceiveToIdle_IT(gps_1.huart, gps_1_buffers[gps_1_index], GPS_BUFFER_SIZE);
HAL_UARTEx_ReceiveToIdle_IT(gps_2.huart, gps_2_buffers[gps_2_index], GPS_BUFFER_SIZE);

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size) {
    if (huart == gps_1.huart) {
        gps_1_sizes[gps_1_index] = Size;
        gps_1_ready[gps_1_index] = 1;
        gps_1_index = (gps_1_index == 0) ? 1 : 0;
        HAL_UARTEx_ReceiveToIdle_IT(gps_1.huart, gps_1_buffers[gps_1_index], GPS_BUFFER_SIZE);
    } else if (huart == gps_2.huart) {
        gps_2_sizes[gps_2_index] = Size;
        gps_2_ready[gps_2_index] = 1;
        gps_2_index = (gps_2_index == 0) ? 1 : 0;
        HAL_UARTEx_ReceiveToIdle_IT(gps_2.huart, gps_2_buffers[gps_2_index], GPS_BUFFER_SIZE);
    }
}
```

Drain each receiver's ready buffer into `gps_process()` the same way as the single-GPS case, then fuse them:

```c
gps_data_t data;
if (gps_read_combined(&gps_1, &gps_2, &data)) {
    // Use data.numSV, data.lat, data.lon, data.headMot
}
```
