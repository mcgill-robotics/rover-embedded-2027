import rover_embedded.drive.esc_can.drive_can_communication as drive_can
import time
if __name__ == "__main__":

    # Example usage
    # print(can.interface.detect_available_configs())
    station = drive_can.CANStation(interface="slcan", channel="/dev/ttyACM0", bitrate=500000) #channel must be 0 as zig

    # Create an ESCs class
    escInterface = drive_can.ESCInterface(station)

    # Create Drive interface for high-level drive control
    drive = drive_can.DriveInterface(escInterface)


    ## CODE BELOW HERE
    # drive.stop_motor(drive_can.NodeID.LF_DRIVE)
    
    
    drive.run_motor(drive_can.NodeID.LB_DRIVE, 200)
    time.sleep(1)
    speed = 0
    while speed != 2000:
        # drive.read_speed(drive_can.NodeID.LB_DRIVE)
        # speed = None
        # while speed is None:
        #     speed = station.recv_msg(1)
        # speed = speed[2]
        drive.run_motor(drive_can.NodeID.LB_DRIVE, 2000)
        time.sleep(1)

    # drive.read_all_faults(drive_can.NodeID.LF_DRIVE)
    drive.stop_motor(drive_can.NodeID.LB_DRIVE)
    
    
    # drive.ping_motor(drive_can.NodeID.LB_DRIVE)
    station.recv_msg(0.1)
    station.close()
