#include <stdint.h>
#include <stdbool.h>
#include "mc_interface.h"
#include <string.h>
#include <math.h>
#include "stm32g4xx_hal_fdcan.h"

// Defines
#ifndef CAN_processing_H
#define CAN_processing_H
#endif // CAN_processing_H

#ifndef M_PI
# define M_PI 3.14159265358979323846
#endif

// Defining variables
extern int s_previousDirection;



extern uint8_t ESC_ID;
extern FDCAN_HandleTypeDef hfdcan1;

// Define the bit masks to retrieve the relevent portions of data from the CAN id
#define CAN_SENDER_MASK		  		(0x0400U) // 0b010000000000
#define CAN_SENDER_SHIFT 		    (10U)
#define CAN_ACTION_MASK  			(0x0200U) // 0b001000000000
#define CAN_ACTION_SHIFT    		(9U)
#define CAN_CONFIG_MASK				(0x0100U)	// 0b000100000000
#define CAN_CONFIG_SHIFT			(8U)
#define CAN_MOTORTYPE_MASK			(0x0080U) // 0b000010000000
#define CAN_MOTORTYPE_SHIFT 		(7U)
#define CAN_SPEC_MASK				(0x0070U) // 0b000001110000
#define CAN_SPEC_SHIFT				(4U)
#define CAN_DEVICEID_MASK			(0x000FU)// 0b000000001111


// Enumaeration classes for different possible CAN Message casess
typedef enum {
    MASTER				= 0,
    SLAVE				= 1
} Transmitter;

typedef enum {
    ACTION_RUN			= 0,
    ACTION_READ			= 1
} Action;

typedef enum {
    MULTIPLE_MOTORS		= 0,
    SINGLE_MOTOR		= 1
} MotorConfig;

typedef enum {
    DRIVE_MOTOR			= 0,
    STEERING_MOTOR		= 1
} MotorType;

typedef enum {
    RUN_STOP               	= 0,
	RUN_ACKNOWLEDGE_FAULTS 	= 1,
    RUN_SPEED              	= 2,
    RUN_POSITION           	= 3,
} RunSpec;

typedef enum {
    READ_SPEED            = 0,   /* Motor speed (RPM or rad/s) */
    READ_POSITION         = 1,   /* Rotor / joint position     */
    READ_VOLTAGE          = 2,   /* DC bus voltage             */
    READ_CURRENT          = 3,   /* Phase currents             */
    READ_TEMPERATURE      = 4,   /* Board / FET temperature    */
    READ_CURRENT_STATE    = 5,   /* Fault flags, motor state   */
    READ_PING             = 6,   /* Ping / heartbeat           */
    READ_CONTROL_MODE     = 7,   /* Current control mode       */
    READ_ALL_FAULTS       = 8
} ReadSpec;

typedef enum {
	RF_DRIVE = 0,
	LF_DRIVE = 1,
	LB_DRIVE = 2,
	RB_DRIVE = 3,
	RF_STEER = 4,
	RB_STEER = 5,
	LB_STEER = 6,
	LF_STEER = 7
} MotorID;

// Struct for a CAN message ID
typedef struct {
	Transmitter		messageSender;
	MotorType		motorType;
	MotorConfig		motorConfig;
    Action			commandType;
	ReadSpec 		readSpec;
	RunSpec			runSpec;
	MotorID			motorID;
} ParsedCANID;

//Watchdog for start condition!
typedef struct {
    uint32_t    firstTick;
    uint8_t     attempts;
} StartWatchdog;


/* CAN ID construction  */
/**
 * @brief  Build a complete 11-bit CAN ID from individual fields.
 *
 * This is the single canonical builder used by both sendCANResponse()
 * and the telemetry scheduler.
 */
static inline uint16_t CAN_BuildID(uint8_t sender,
                                   uint8_t action,
                                   uint8_t config,
                                   uint8_t motor_type,
                                   uint8_t spec,
                                   uint8_t device_id)
{
    uint16_t id = 0;
    id |= (uint16_t)(sender     & 0x01U) << CAN_SENDER_SHIFT;
    id |= (uint16_t)(action     & 0x01U) << CAN_ACTION_SHIFT;
    id |= (uint16_t)(config     & 0x01U) << CAN_CONFIG_SHIFT;
    id |= (uint16_t)(motor_type & 0x01U) << CAN_MOTORTYPE_SHIFT;
    id |= (uint16_t)(spec       & 0x07U) << CAN_SPEC_SHIFT;
    id |= (uint16_t)(device_id  & 0x0FU);
    return id;
}

//CAN Interaction prototypes
void CAN_Parse_MSG (FDCAN_RxHeaderTypeDef *rxHeader, uint8_t *rxData);
void Process_Multiple_ESC_Command (ParsedCANID *parsedMessageID, uint8_t *rxData);
void Process_Single_ESC_Command (ParsedCANID *CANMessageID, uint8_t *rxData);
void sendCANResponse(ParsedCANID *CANMessageID, float information);
float SingleExtractFloatFromCAN(uint8_t *data);

// Motor control prototypes
void ControlSingleMotor(float newSpeed);
void runSingleMotorV2(float newSpeed); //TODO remove V part
void IdleSingleMotor(float newSpeed);
void StartSingleMotor(float newSpeed);

bool checkReversing(float speedCmd);
bool safeStopMotor(float currentSpeedRpm, MCI_State_t motorState);
//helper function prototypes

float speedCheck (float targetSpeed);
float clippingCheck(float currentSpeedSetpoint);
int16_t extract_multiple_speeds(const uint8_t *rxData);
uint16_t computeRampTimeMs(float currentSpeedRpm, float targetSpeedRpm, bool isStartup);


