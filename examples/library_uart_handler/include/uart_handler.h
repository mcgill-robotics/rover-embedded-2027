#ifndef UART_HANDLER
#define UART_HANDLER

#include "stm32g4xx_hal.h"
void set_uart(UART_HandleTypeDef* uart);

void fill_buffer();

int read_buffer_slice(int to_read, char** slice);

void clear_buffer_slice();

#endif