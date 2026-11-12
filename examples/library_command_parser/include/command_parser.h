
#ifndef COMMAND_PARSER_H
#define COMMAND_PARSER_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum command_type_t {
	LIGHT_STATE,
	LIGHT_SPEED,
	NONE
} command_type_t;

typedef struct command_t {
	command_type_t type;
	int data;
} command_t;

int parse(unsigned char* message, int available, command_t* command);

#ifdef __cplusplus
}
#endif

#endif