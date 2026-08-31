import rover_embedded.drive.esc_can.drive_can_communication as drive_can

if __name__ == "__main__":

    # Example usage
    # print(can.interface.detect_available_configs())
    station = drive_can.CANStation(interface="slcan", channel="COM6", bitrate=500000) #channel must be 0 as zig

    # Create an ESCs class
    escInterface = drive_can.ESCInterface(station)

    # Create Drive interface for high-level drive control
    drive = drive_can.DriveInterface(escInterface)


    ## CODE BELOW HERE
    # drive.stop_motor(NodeID.LF_DRIVE)

    # drive.run_motor(NodeID.LF_DRIVE, 1500)
    # drive.read_all_faults(NodeID.LF_DRIVE)
    # drive.stop_motor(NodeID.LF_DIVE)

    
    station.recv_msg(0.01)
    station.close()
