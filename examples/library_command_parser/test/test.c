#include "command_parser.h"
#include <stdio.h>
#include <stdint.h>

int main(){
	// ordered in little-endian because most machines are little-endian nowadays
	char off_command[5] = {'l', 0,0,0,0};
	char on_command[5] = {'l', 1, 0, 0, 0};
	char speed_command_1000[5] = {'s', 0xE8,0x03,0,0};
	char speed_command_500[5] = {'s', 0xF4, 0x01, 0, 0};
	command_t cmd;
	parse(off_command, 5, &cmd);
	if (cmd.type == LIGHT_STATE && cmd.data == 0){
		printf("OK got Off Light State\n");
	} else {
		printf("ERROR did not get Off Light State\n");
	}
	parse(on_command, 5, &cmd);
	if (cmd.type == LIGHT_STATE && cmd.data == 1){
		printf("OK got On Light State\n");
	} else {
		printf("ERROR did not get On Light State\n");
	}
	parse(speed_command_1000, 5, &cmd);
	if (cmd.type == LIGHT_SPEED && cmd.data == 1000){
		printf("OK got Light Speed 1000\n");
	} else {
		printf("ERROR did not get Light Speed 1000\n");
	}
	parse(speed_command_500, 5, &cmd);
	if (cmd.type == LIGHT_SPEED && cmd.data == 500){
		printf("OK got Light Speed 500\n");
	} else {
		printf("ERROR did not get Light Speed 500\n");
	}
	return 0;
}