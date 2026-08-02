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

#ifndef I2C_LCD
#define I2C_LCD

#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include "main.h"

extern I2C_HandleTypeDef hi2c1;
extern UART_HandleTypeDef huart2;

void I2C_Scan();
HAL_StatusTypeDef LCD_SendInternal(uint8_t lcd_addr, uint8_t data, uint8_t flags);
void LCD_SendCommand(uint8_t lcd_addr, uint8_t cmd);
void LCD_SendData(uint8_t lcd_addr, uint8_t data);
void LCD_Init(uint8_t lcd_addr);
void LCD_SendString(uint8_t lcd_addr, const char *str);
void LCD_SetCursor(uint8_t row, uint8_t col);
void LCD_ClearLine(uint8_t row);
void LCD_ClearScreen();
void LCD_SetupMenu(int flag);
void init();
void loop();

#endif
