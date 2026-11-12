#include <gtest/gtest.h>
#include "command_parser.h"
#include <stdio.h>
#include <stdint.h>

// Demonstrate some basic assertions.
TEST(CommandTest, BasicAssertions) {
  // ordered in little-endian because most machines are little-endian nowadays
	unsigned char off_command[5] = {'l', 0,0,0,0};
	unsigned char on_command[5] = {'l', 1, 0, 0, 0};
	unsigned char speed_command_1000[5]  ={'s', 0xE8, 0x03,0,0};
	unsigned char speed_command_500[5]  ={'s', 0xF4, 0x01, 0, 0};
	command_t cmd;
	parse(off_command, 5, &cmd);
	// Command 1
	EXPECT_EQ(cmd.type, LIGHT_STATE);
	EXPECT_EQ(cmd.data, 0);
	// Command 2
	parse(on_command, 5, &cmd);
	EXPECT_EQ(cmd.type, LIGHT_STATE);
	EXPECT_EQ(cmd.data, 1);
	// Command 3
	parse(speed_command_1000, 5, &cmd);
	EXPECT_EQ(cmd.type, LIGHT_SPEED);
	EXPECT_EQ(cmd.data, 1000);
	// Command 4
	parse(speed_command_500, 5, &cmd);
	EXPECT_EQ(cmd.type, LIGHT_SPEED);
	EXPECT_EQ(cmd.data, 500);
}
