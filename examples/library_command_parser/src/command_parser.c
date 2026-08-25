#include "command_parser.h"
#include "string.h"
#include <stdint.h>
/**
 * Returns bytes read
 */
int parse(char* message, int available, command_t* command){
	if (available<5){
		return 0;
	}
	switch (*message)
	{
	case 'l':
		command -> type = LIGHT_STATE;
		command -> data = *((uint32_t*) (message+1)); // read an int from next 4 bytes
		break;
	case 's':
		command -> type = LIGHT_SPEED;
		command -> data = *((uint32_t*) (message+1)); // read an int from next 4 bytes
		break;
	default:
		command -> type = NONE;
		command -> data = 0;
		break;
	}
	return 2;
}