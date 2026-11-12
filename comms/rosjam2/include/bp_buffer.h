#ifndef BP_BUFFER_H
#define BP_BUFFER_H

#include <stdint.h>
typedef struct BPBuffer {
	uint8_t* read;
	uint8_t* write;
	uint8_t* invalid;
	int32_t size;
	int32_t capacity;
	uint8_t* backing_buf;
} bp_buffer_t;

typedef enum bp_status {
	READ_OK,
	READ_NOT_CONTIGUOUS,
	WRITE_OK,
	WRITE_FULL
} bp_status_t;

/**
Initialize the buffer
*/
void init_buffer(bp_buffer_t* buf, uint8_t* backing_buf, int32_t capacity);

/**
Acquire the read pointer for a contiguous block.
Returns the length of the contigious block (This may be smaller than n)
Note: despite the name this only peeks from the buffer, `use consume_n_cont`
to allow it to be overwritten.
*/
int32_t read_n_cont(bp_buffer_t* buf, int32_t n, uint8_t** read);

/**
Mark a n-bytes from the buffer as consumed and free to be overwritten.
*/
void consume_n(bp_buffer_t* buf, int32_t n);

/**
Tries to write a contiguous block to the buffer
 */
bp_status_t write_n_cont(bp_buffer_t* buf, uint8_t* src, int32_t src_len);


#endif