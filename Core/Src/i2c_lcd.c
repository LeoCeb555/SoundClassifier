/*
 * Portions of this LCD I2C driver are adapted from code by
 * Aleksander Alekseev (Copyright (c) 2018).
 * Source: stm32-i2c-lcd-1602 repository
 * URL: https://github.com/afiskon/stm32-i2c-lcd-1602.git
 *
 * Original code licensed under the MIT License.
 * See LICENSES/stm32-i2c-lcd-1602-MIT.txt for the full license text.
 *
 * Modifications were made for this project's STM32-based
 * 20x4 I2C LCD implementation.
 */

#include "i2c_lcd.h"

#define PIN_RS    (1 << 0)
#define PIN_EN    (1 << 2)
#define BACKLIGHT (1 << 3)
#define LCD_DELAY_MS 5
#define LCD_ADDR (0x27 << 1)

void I2C_Scan() {
    char info[] = "Scanning I2C bus...\r\n";
    HAL_UART_Transmit(&huart2, (uint8_t*)info, strlen(info), HAL_MAX_DELAY);

    HAL_StatusTypeDef res;
    for(uint16_t i = 0; i < 128; i++) {
        res = HAL_I2C_IsDeviceReady(&hi2c1, i << 1, 1, 10);
        if(res == HAL_OK) {
            char msg[64];
            snprintf(msg, sizeof(msg), "0x%02X", i);
            HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
        } else {
            HAL_UART_Transmit(&huart2, (uint8_t*)".", 1, HAL_MAX_DELAY);
        }
    }

    HAL_UART_Transmit(&huart2, (uint8_t*)"\r\n", 2, HAL_MAX_DELAY);
}

HAL_StatusTypeDef LCD_SendInternal(uint8_t lcd_addr, uint8_t data, uint8_t flags) {
    HAL_StatusTypeDef res;
    for(;;) {
        res = HAL_I2C_IsDeviceReady(&hi2c1, lcd_addr, 1, HAL_MAX_DELAY);
        if(res == HAL_OK)
            break;
    }

    uint8_t up = data & 0xF0;
    uint8_t lo = (data << 4) & 0xF0;

    uint8_t data_arr[4];
    data_arr[0] = up|flags|BACKLIGHT|PIN_EN;
    data_arr[1] = up|flags|BACKLIGHT;
    data_arr[2] = lo|flags|BACKLIGHT|PIN_EN;
    data_arr[3] = lo|flags|BACKLIGHT;

    res = HAL_I2C_Master_Transmit(&hi2c1, lcd_addr, data_arr, sizeof(data_arr), HAL_MAX_DELAY);
    HAL_Delay(LCD_DELAY_MS);
    return res;
}

void LCD_SendCommand(uint8_t lcd_addr, uint8_t cmd) {
    LCD_SendInternal(lcd_addr, cmd, 0);
}

void LCD_SendData(uint8_t lcd_addr, uint8_t data) {
    LCD_SendInternal(lcd_addr, data, PIN_RS);
}

void LCD_Init(uint8_t lcd_addr) {
    // 4-bit mode, 2 lines, 5x7 format
    LCD_SendCommand(lcd_addr, 0b00110000);
    // display & cursor home (keep this!)
    LCD_SendCommand(lcd_addr, 0b00000010);
    // display on, right shift, underline off, blink off
    LCD_SendCommand(lcd_addr, 0b00001100);
    // clear display (optional here)
    LCD_SendCommand(lcd_addr, 0b00000001);
}

void LCD_SendString(uint8_t lcd_addr, const char *str) {
    while(*str) {
        LCD_SendData(lcd_addr, (uint8_t)(*str));
        str++;
    }
}

void LCD_SetCursor(uint8_t row, uint8_t col)
{
    uint8_t row_offsets[] = {0x00, 0x40, 0x14, 0x54};

    LCD_SendCommand(
        LCD_ADDR,
        0x80 | (row_offsets[row] + col)
    );
}

void LCD_ClearLine(uint8_t row){
	LCD_SetCursor(row, 0);
	LCD_SendString(LCD_ADDR, "                    ");
}

void LCD_ClearScreen(){
	LCD_ClearLine(0);
	LCD_ClearLine(1);
	LCD_ClearLine(2);
	LCD_ClearLine(3);
}

void LCD_SetupMenu(int flag){

	LCD_ClearScreen();

	  if(!flag){
		  LCD_SetCursor(0, 3);
		  LCD_SendString(LCD_ADDR, "Mode: Classify");
		  LCD_SetCursor(2, 7);
		  LCD_SendString(LCD_ADDR, "Sound:");
	  }
	  else{
		  LCD_SetCursor(0, 3);
		  LCD_SendString(LCD_ADDR, "Mode: Collect");
	  }
}

void init() {
    I2C_Scan();
    LCD_Init(LCD_ADDR);

    LCD_SetCursor(1, 2);
    LCD_SendString(LCD_ADDR, "Classifier being");

    LCD_SetCursor(2, 7);
    LCD_SendString(LCD_ADDR, "setup");
}

void loop() {
    HAL_Delay(100);
}
