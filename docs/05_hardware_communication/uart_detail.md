# UART 详细手册

> UART（Universal Asynchronous Receiver/Transmitter）是最基础的串行通信协议，换句话说就是我们常说的“串口”。
> 它简单、通用，几乎所有单片机都内置 UART 模块，是调试和连接低速外设的首选。
---

## 1. UART 是什么

**UART(通用异步收发器)** 是一种**异步串行**通信协议，数据逐位传输，不需要时钟线，依靠双方约定好的**波特率**来同步。

## 1.1 UART 的特点
- **异步**：没有独立的时钟线，靠起始位和停止位同步。
- **全双工**：可同时发送和接收（两条独立数据线）。
- **点对点**：一个 UART 接口只能连接一个设备（不像 I2C 可以挂多个）。

## 1.2 典型应用
我一般在下面这些场合用它：
- 打印调试信息（`printf` 重定向到串口）
- 连接 GPS、蓝牙模块、WiFi 模块等低速外设
- 单片机与树莓派/工控机之间的简单通信
- 通过 USB 转 TTL 模块与电脑交互

---

## 2. 硬件接线

### 2.1 电平标准

| 电平类型 | 逻辑0 | 逻辑1 | 电压范围 | 常见场景 |
|----------|-------|-------|----------|----------|
| TTL | 0V | 3.3V 或 5V | 0～5V | 单片机之间、模块与单片机 |
| RS-232 | +3～+15V | -3～-15V | ±15V | 老式串口、工控机 |
| RS-485 | 差分 | 差分 | 差分 | 长距离、多节点（需转换） |

**注意**：单片机的 UART 引脚输出 TTL 电平，*不能直接接电脑的 RS-232（会烧）*，必须用 **USB 转 TTL 模块**（CH340、CP2102、FT232 等）。

### 2.2 接线方法

**基本接线**：TX（发送）接 RX（接收），RX 接 TX，GND 共地。
```
单片机 UART1_TX <--> 模块 RX
单片机 UART1_RX <--> 模块 TX
单片机 GND <--> 模块 GND
```
**注意**：如果模块电压和单片机不匹配（比如模块是 5V，单片机是 3.3V），需要加电平转换（电阻分压、专用电平转换芯片）。
**RS-485 转换**：如果需要长距离通信或多节点，可以使用 RS-485 转换器，接线如下：
```
单片机 UART1_TX <--> RS-485 转换器 DI
单片机 UART1_RX <--> RS-485 转换器 RO
单片机 GND <--> RS-485 转换器 GND
RS-485 转换器 A <--> 另一端 A
RS-485 转换器 B <--> 另一端 B
```

---

## 3. 通信参数（双方必须一致!）

| 参数 | 说明 | 常用值 |
|------|------|--------|
| 波特率 | 每秒传多少位 | 9600, 19200, 38400, 115200, 460800 |
| 数据位 | 每个字节几位 | 7 或 8（常用 8） |
| 停止位 | 标志结束的位数 | 1 或 2（常用 1） |
| 校验位 | 简单检错 | 无、奇、偶 |
| 流控制 | 防止丢数据 | 一般不用 |

> tip:调试时大部分情况下用 **115200-8-N-1**
>（115200 波特率，8 数据位，无校验，1 停止位）。稳定，速度快。

---

## 4. 使用场景和案例
插上电脑，Windows 会多一个 COMx，Linux 是 /dev/ttyUSB0。

### 2.3 电平匹配（吃过亏）

- 3.3V 单片机的 TX 输出 3.3V，接 5V 单片机的 RX，一般能识别（5V 单片机认为 >2V 就是高电平）。反过来，5V 单片机的 TX 输出 5V，接 3.3V 单片机的 RX，可能烧引脚。最好加电平转换，或者选 3.3V 的模块。
- 长距离：TTL 抗干扰差，超过 1 米容易乱码。我一般超过 1 米就降波特率（9600），或者改用 RS-485。

---

## 3. 通信参数（双方必须一致）

| 参数 | 说明 | 常用值 |
|------|------|--------|
| 波特率 | 每秒传多少位 | 9600, 19200, 38400, 115200, 460800 |
| 数据位 | 每个字节几位 | 7 或 8（常用 8） |
| 停止位 | 标志结束的位数 | 1 或 2（常用 1） |
| 校验位 | 简单检错 | 无、奇、偶 |
| 流控制 | 防止丢数据 | 一般不用 |

调试时我几乎都用 **115200-8-N-1**（115200 波特率，8 数据位，无校验，1 停止位）。稳定，速度快。

---

## 4. 代码实例（实测能跑）

### 4.1 STM32 标准外设库（Standard Peripheral Library）

下面以 STM32F103 系列为例，使用 USART1。

**初始化**：
```c
#include "stm32f10x.h"

void USART1_Init(void) {
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    
    // 使能时钟
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1 | RCC_APB2Periph_GPIOA, ENABLE);
    
    // 配置 TX (PA9) 复用推挽输出，RX (PA10) 浮空输入
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    
    // 配置 UART 参数
    USART_InitStructure.USART_BaudRate = 115200;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;
    USART_Init(USART1, &USART_InitStructure);
    
    // 使能 USART1
    USART_Cmd(USART1, ENABLE);
}
```

**发送字节**：
```c
void USART1_SendByte(uint8_t byte) {
    while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET); // 等待发送缓冲区空
    USART_SendData(USART1, byte);
}
``` 

**接收字节**：
```c
uint8_t USART1_ReceiveByte(void) {
    while (USART_GetFlagStatus(USART1, USART_FLAG_RXNE) == RESET); // 等待接收缓冲区有数据
    return USART_ReceiveData(USART1);
}
```

**发送字符串**：
```c
void USART1_SendString(const char* str) {
    while (*str) {
        USART1_SendByte(*str++);
    }
}
```

**中断方式接收（需要配置 NVIC）**：
```c
// 在初始化函数中增加中断配置
NVIC_InitTypeDef NVIC_InitStructure;
NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
NVIC_Init(&NVIC_InitStructure);
USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);  // 使能接收中断

// 中断服务函数
void USART1_IRQHandler(void) {
    if (USART_GetITStatus(USART1, USART_IT_RXNE) != RESET) {
        uint8_t rx_data = USART_ReceiveData(USART1);
        // 处理接收到的数据
        process_byte(rx_data);
    }
}
```

**重定向 printf**：
```c
#include <stdio.h>

int fputc(int ch, FILE *f) {
    USART1_SendByte((uint8_t)ch);
    return ch;
}
```

### 4.2 HAL 库（Hardware Abstraction Layer）
使用 STM32CubeMX 生成代码后，HAL 库的 UART 初始化和使用更加简洁，推荐新项目使用 HAL 库。

```c
#include "stm32f1xx_hal.h"
UART_HandleTypeDef huart1;
void MX_USART1_UART_Init(void) {
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart1);
}
```

发送和接收函数也更简单：
```c
HAL_UART_Transmit(&huart1, (uint8_t*)"Hello", 5, HAL_MAX_DELAY);
uint8_t rx_buffer[10];
HAL_UART_Receive(&huart1, rx_buffer, 10, HAL_MAX_DELAY);
```

### 4.3 Linux Python
``` python
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.write(b'Hello\r\n')
data = ser.readline()
print(data)
ser.close()
```

---

## 5. 常见问题和解决方法

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 无法通信 | 波特率不匹配 | 确认双方波特率一致 |
| 完全没数据 | 接线错误 | 检查 TX/RX 是否交叉|
| 无法通信 | 电平不匹配 | 确认电压兼容，必要时加电平转换 |
| 收到的全是乱码 | 波特率过高 | 降低波特率（如 9600） |
| 数据乱码 | 长距离干扰 | 使用屏蔽线，或改用 RS-485 |

---
<p align="center">— uart有待补充~ —</p>