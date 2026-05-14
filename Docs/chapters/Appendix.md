# 附录

## 附录A：STM32 控制层源代码目录

STM32 控制层源代码采用 Rust 语言开发，基于 Embassy 异步运行时框架，按 Cargo crate 组织为 firmware（固件）、bsw（基础软件）、app（应用）、service（服务）四层。完整源代码详见项目代码仓库[@greenhouse2026src]。表中路径以 `Src/Stm32_Control/` 为根目录。

::: {custom-style="表题"}
表 A-1 STM32 控制层主要源代码文件
:::

| 文件路径 | 功能说明 |
|:---|:---|
| `firmware/src/bin/main.rs` | 固件入口，系统时钟配置与任务派发 |
| `firmware/src/bin/shared.rs` | 全局状态单例 `GLOBAL_STATE` 定义 |
| `firmware/src/bin/domains/dispatcher.rs` | 迟滞调度器，自动控制模式核心逻辑 |
| `firmware/src/bin/domains/sht30.rs` | SHT30 温湿度传感器域任务 |
| `firmware/src/bin/domains/bh1750.rs` | BH1750 光照传感器域任务 |
| `firmware/src/bin/domains/soil_moisture.rs` | 土壤湿度 ADC 采集域任务 |
| `firmware/src/bin/domains/ventilation_fan.rs` | 通风风扇 PID 闭环控制域任务 |
| `firmware/src/bin/domains/ws2812.rs` | WS2812B 补光灯驱动域任务 |
| `firmware/src/bin/domains/mg995.rs` | MG995 遮阳舵机控制域任务 |
| `firmware/src/bin/domains/water_pump.rs` | 水泵开关控制域任务 |
| `firmware/src/bin/domains/humidifier.rs` | 加湿器开关控制域任务 |
| `firmware/src/bin/domains/can_rx.rs` | CAN 接收路由处理任务 |
| `firmware/src/bin/domains/can_tx.rs` | CAN 遥测上报发送任务 |
| `crates/bsw/src/pid.rs` | 离散位置式 PID 控制器 |
| `crates/bsw/src/motor_ctrl.rs` | 风扇电机闭环控制封装 |
| `crates/bsw/src/can_proto.rs` | CAN 协议编解码模块 |
| `crates/bsw/src/sht30.rs` | SHT30 I2C 驱动 |
| `crates/bsw/src/bh1750.rs` | BH1750 I2C 驱动 |
| `crates/bsw/src/ws2812.rs` | WS2812B DMA 驱动 |

## 附录B：ESP32 交互层源代码目录

ESP32 交互层源代码采用 C/C++ 语言开发，基于 FreeRTOS 和 LVGL 框架，按分层架构组织。完整源代码详见项目代码仓库[@greenhouse2026src]。表中路径以 `Src/Esp32_Interaction/` 为根目录。

::: {custom-style="表题"}
表 B-1 ESP32 交互层主要源代码文件
:::

| 文件路径 | 功能说明 |
|:---|:---|
| `src/main.cpp` | 固件入口，FreeRTOS 任务创建与启动 |
| `src/App/CAN/can_app.cpp` | CAN 应用层调度 |
| `src/App/LVGL/lvgl_app.cpp` | LVGL 应用层调度 |
| `src/BSP/Os_Service/os_service.cpp` | FreeRTOS 操作系统服务封装 |
| `src/Service/SensorState/sensor_state.c` | 多节点数字孪生状态管理 |
| `src/Service/DeepSeekAPI/deepseek_api.cpp` | DeepSeek 大语言模型 API 集成 |
| `src/Service/VoiceAssistant/voice_assistant_service.cpp` | 语音助手服务（录音→识别→推理→合成→播放） |
| `src/Service/VoiceAssistant/voice_assistant_bridge.cpp` | 语音助手 C/C++ 桥接层 |
| `src/Service/CanService/CanNetworkService/can_network_service.c` | CAN 总线网络服务 |
| `src/Service/CanService/CAN/can_protocol.c` | CAN 协议编解码 |
| `src/Service/GUI/gui_manager.cpp` | LVGL 界面管理器 |
| `src/Service/GUI/SmartGreenhouse/custom/custom.c` | 自定义业务逻辑 |
| `src/Service/WifiService/wifi_service.cpp` | WiFi 网络连接管理 |
| `src/Service/NetworkService/http_client.cpp` | HTTPS 客户端封装 |
| `src/Service/BaiduApi/baidu_api.cpp` | 百度语音 API（STT/TTS）集成 |
| `src/Service/LedService/led_service.cpp` | LED 状态指示服务 |
| `src/Service/Utils/utils.cpp` | 通用工具函数 |
| `src/ECUAL/Display/display_hal.cpp` | 显示硬件抽象层 |
| `src/ECUAL/INMP441/inmp441_driver.cpp` | INMP441 麦克风驱动 |
| `src/ECUAL/MAX98357AETE/max98357a_driver.cpp` | MAX98357A 功放驱动 |
| `src/MCAL/I2S/i2s_hal.cpp` | I2S 总线硬件抽象层 |
| `src/MCAL/NetworkAbstraction/wifi_hal.cpp` | WiFi 硬件抽象层 |
| `src/Config/board_config.h` | 硬件引脚配置 |
| `src/Config/app_config.h` | 应用层参数配置 |

## 附录C：硬件设计文件

本系统硬件设计使用嘉立创 EDA 专业版（EasyEDA Pro）完成，工程文件如下：

::: {custom-style="表题"}
表 C-1 硬件设计文件
:::

| 文件路径 | 说明 |
|:---|:---|
| `Src/Intelligent_Greenhouse.epro2` | 嘉立创 EDA 工程文件（含原理图与 PCB 设计） |

硬件设计文件随项目源代码一同发布，可从项目代码仓库获取[@greenhouse2026src]。

## 附录D：项目代码仓库

本课题全部源代码（含 STM32 控制层、ESP32 交互层及硬件设计文件）已发布至 GitHub，仓库地址及版本信息如下：

仓库地址：`https://github.com/yhy-lk/Intelligent_Greenhouse`

发布版本：v1.0.0（`https://github.com/yhy-lk/Intelligent_Greenhouse/releases/tag/v1.0.0`）

> 注：正文中的代码引用均标注了对应源文件路径，读者可据此在上述仓库中定位完整源码。
