#include "main.h"

void Toggle_LED(){
	HAL_GPIO_TogglePin(USER_LED_GPIO_Port, USER_LED_Pin);
}