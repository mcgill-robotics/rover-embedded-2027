#include "bp_buffer.h"
#include <stdint.h>
#include <string.h>
#include <sys/_intsup.h>

/**
Initialize the buffer
*/
void init_buffer(bp_buffer_t* buf, uint8_t* backing_buf, int32_t capacity){
	buf->backing_buf = backing_buf;
	buf->capacity = capacity;
	buf->invalid = backing_buf+capacity;
	buf->read = backing_buf+capacity;
	buf->write = backing_buf+capacity;
	buf->size = 0;
}

/**
Acquire the read pointer for a contiguous block.
Returns the length of the contigious block (This may be smaller than n)
Note: despite the name this only peeks from the buffer, `use consume_n_cont`
to allow it to be overwritten.
*/
int32_t read_n_cont(bp_buffer_t* buf, int32_t n, uint8_t** read){
	*read = buf->read;
	if (buf->read+n < buf->invalid){
		return n;
	} else {
		return buf->invalid-buf->read;
	}
}

/**
Mark a n-bytes from the buffer as consumed and free to be overwritten.
*/
void consume_n(bp_buffer_t* buf, int32_t n){
	if (buf->read+n < buf->invalid){
		buf->read= buf->read + n;
	} else {
		uint32_t diff = (buf->read+n)-buf->invalid;
		buf->read = buf->backing_buf+diff;
	}
}

/**
Tries to write a contiguous block to the buffer
 */
bp_status_t write_n_cont(bp_buffer_t* buf, uint8_t* src, int32_t src_len){ 
	// check if enough space is free
	if (buf->capacity-buf->size > src_len){
		uint8_t* end = buf->backing_buf+buf->capacity;
		if (end - buf->write > src_len){
			// ok to write at current write pointer
			memcpy(buf->write, src, src_len);
			buf->write=buf->write+src_len;
			return WRITE_OK;
		} else {
			// check for space at front
			if (buf->read-buf->backing_buf>src_len){
				buf->invalid = buf->write;
				buf->write = buf->backing_buf+src_len;
				memcpy(buf->backing_buf, src, src_len);
				return WRITE_OK;
			}else {
				return WRITE_FULL;
			}
		}
	} else {
		return WRITE_FULL;
	}
}
