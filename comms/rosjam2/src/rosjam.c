#include "bp_buffer.h"
#include "default_rosjam_config.h"
#include "rosjam.h"
#include "class/cdc/cdc_device.h"
#include "device/usbd.h"
#include "tusb_config.h"
#include "tusb.h"
#include "stdio.h"
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>
#include "cobs.h"
#include "rosjam_internals.h"

cobs_reader_t reader;
uint8_t rx_buf[1024];
uint8_t decode_backing_buf[1024];
bp_buffer_t decode_buf;

double string_to_float(char* string){
	errno = 0;
	char* next = NULL;
	double converted_val = strtod(string, &next);
	if (next == string){
		// Nothing was processed
		return 0;
	}
	if (errno == ERANGE){
		// out of representable range
		return 0;
	}
	return converted_val;
}

int float_to_string(double number, int precision, char* buf, int buf_len){
    int len = snprintf(NULL, 0, "%.*lf", precision, number);
	if (len +1 > buf_len){
		return -1;
	}
    snprintf(buf, len + 1, "%.*lf", precision, number);
	return len+1;
}

int int_to_string(int number, char* buf, int buf_len){
    int len = snprintf(NULL, 0, "%d", number);
	if (len +1 > buf_len){
		return -1;
	}
    snprintf(buf, len + 1, "%d", number);
	return len+1;
}

void setup_simple(){
	tusb_rhport_init_t dev_init = {
    	.role = TUSB_ROLE_DEVICE,
    	.speed = TUSB_SPEED_AUTO
  	};
  	tusb_init(BOARD_TUD_RHPORT, &dev_init);
}

void print_to_usb(char* message){
	send_msg_raw(message,strlen(message));
}

void send_msg_raw(char *message, int message_len){
	if (tud_cdc_n_ready(USB_CDC_ITF)){
		tud_cdc_n_write(USB_CDC_ITF, message, message_len);
		tud_cdc_n_write_flush(USB_CDC_ITF);
	}
}

int has_data(){
	if (tud_cdc_n_ready(USB_CDC_ITF)){
		int available = tud_cdc_n_available(USB_CDC_ITF);
		return available > 0;
	}
	return 0;
}

char read_char(){
	if (has_data()){
		return tud_cdc_n_read_char(USB_CDC_ITF);
	}
	return -1;
}


void process_simple(){
	tud_cdc_n_write_flush(USB_CDC_ITF); //make sure small messages get immediately sent
	tud_task();
}

__weak void packet_rx_cb(){

}

void init_rosjam(){
	
	cobs_setup_stream_reader(&reader);
	init_buffer(&decode_buf, decode_backing_buf, 2048);
}

void decode_packet(bp_buffer_t *buf){
	// Check that payload is contiguous
	// Make contiguous and pass to callback
}

void read_packets(){
	// Read from USB
	tud_cdc_n_read(USB_CDC_ITF, rx_buf, 1024);
	// read_n_cont(bp_buffer_t *buf, uint32_t n, uint8_t **read)
	cobs_result_t result = cobs_stream_decode(&reader, rx_buf, 1024, decode_backing_buf, 2048, 0);
	switch (result) {
		case COBS_DONE:
			// To decode make contiguous as needed
			int32_t to_read = reader.current_frame_size;
			while (to_read > 0){
				uint8_t* read_ptr;
				int32_t block_size = read_n_cont(&decode_buf, to_read, &read_ptr);
				if (block_size == to_read){
					// whole packet is already contiguous
				}
				to_read-=to_read;
			}
			// packet_rx_cb()
			break;
		case COBS_INCOMPLETE_FRAME:
			// loop to get more data
			break;
		case COBS_OUTPUT_FULL:
			// clear all data in decode buffer
			break;
		case COBS_RESET:
			// clear data in decode buffer for the current decode 
			break;
	}
}	

void process(){
	tud_task();
	// read data
	read_packets();

	// send data	
	
}