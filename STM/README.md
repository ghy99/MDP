For stm CODE [note not updated]

Please contact @gyanroh on telegram for more details on anything, everything, whatever you need

THIS FUNCTION IS IMPORTANT. takes in the uart connection, esp for the starting one
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	/* to prevent unused argument(s) compilation warning */
	UNUSED(huart);
	// for debug
	//HAL_UART_Receive_IT (&huart3, aRxBuffer, 1);
	// for real task
	HAL_UART_Receive_IT (&huart3, aRxBuffer, 5);
}

}


however this is also important as it will do subsequent enter of uart
HAL_UART_Receive_IT(&huart3, (uint8_t *) aRxBuffer, 5);  //in main task need to add loop, will exec everytime u loop. 



aRxBuffer is a self defined buffer that will REFRESH WITH NEW DATA everytime you flash into it. Forgot whether it has an newline or return char at the back




Ensure you have ur definitions for FREE RTOS!! THIS IS IMPORTANT/
EG
/* Definitions for defaultTask */
osThreadId_t defaultTaskHandle;
const osThreadAttr_t defaultTask_attributes = {
  .name = "defaultTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for motorTask */
osThreadId_t motorTaskHandle;
const osThreadAttr_t motorTask_attributes = {
  .name = "motorTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityLow,
};
/* Definitions for oledTask */
osThreadId_t oledTaskHandle;
const osThreadAttr_t oledTask_attributes = {
  .name = "oledTask",
  .stack_size = 128 * 4,
  .priority = (osPriority_t) osPriorityLow,
};
