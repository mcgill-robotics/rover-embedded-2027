import serial

PORT = "COM7"

with serial.Serial(PORT, 115200) as conn:
	while True:
		command = input()
		if len(command) < 2:
			print("Bad command")
			continue
		
		number_str = command[1:]

		try:
			number = int(number_str)
		except:
			print("Bad command")
			continue

		if conn.writable():
			conn.write(command[0].encode("ascii"))
			conn.write(number.to_bytes(4, 'little'))
