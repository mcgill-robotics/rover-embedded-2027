
#include "stm32g4xx_hal.h"
#include <stdint.h>
#include <string.h>

#define CAPACITY 10

char buf[CAPACITY];
int read_idx = 0;
int size = 0;
int slice_borrowed = 0;
UART_HandleTypeDef* uart_handle;

void set_uart(UART_HandleTypeDef* uart){
	uart_handle = uart;
}

void fill_buffer(){
	if (slice_borrowed){
		return;
	}
	if (read_idx>CAPACITY/2){
		memmove(buf, buf+read_idx, size-read_idx);
		int new_size = size-read_idx;
		read_idx = 0;
		size = new_size;
	}
	int remaining = CAPACITY-size;
	uint16_t read = 0;
	if (remaining>0){
		HAL_UARTEx_ReceiveToIdle(uart_handle, (uint8_t*) buf+size, CAPACITY-size, &read, 10);
	} else {
		size = 0;
		read_idx = 0;
		HAL_UARTEx_ReceiveToIdle(uart_handle, (uint8_t*) buf, CAPACITY, &read, 10);
	}
	size+=read;
}

int read_buffer_slice(int to_read, char** slice){
	int available = size-read_idx;
	if (available >= to_read){
		slice_borrowed = to_read;
		*slice = buf+read_idx;
		return to_read;
	}
	return 0;
}

void clear_buffer_slice(){
	read_idx+=slice_borrowed;
	slice_borrowed = 0;
}