# **硬件&软件工程知识库**<br>Index-Table

 · 项目驱动的笔记集合，方便快速查资料、复盘设计、团队内复用。

+ **作者**：&emsp;&emsp;&emsp;Clowol · 机器人/嵌入式方向研究生  
+ **维护状态**：&emsp;随课题项目持续更新  
+ **交流**：&emsp;&emsp;&emsp;[GitHub Issues](https://github.com/Clowol/Project-Index-Table/issues) · [z171074547@gmail.com](mailto:z171074547@gmail.com)

***

## 📌 为什么搞这个库

做科研和项目时遇到的几个实际痛点：
- 引脚定义、参考电路、驱动代码这些信息散落在数据手册、实验记录和聊天记录里，每次重查很烦。
- 自己踩过的坑，如果不记下来，过段时间又踩一遍，团队里其他人也会重复踩。
- 需要一个**有结构、能检索、带实测依据**的笔记库，而不是一堆零散的文档。

因此我构建了这个知识库，目标是：
- **对自己**：&emsp;设计→测试→归档，后面再做类似项目能直接复用。
- **对团队**：&emsp;少走弯路，快速上手。
- **对外展示**：体现工程文档习惯和问题解决能力。
(内容不一定全，但真实、可复现，有问题**反馈**thanks。)
---

## 🧭 内容导航

- ### 硬件类
| 编号 | 分类 | 典型内容 | 状态 |
|------|------|----------|------|
| 01 | [传感器](./docs/01_hardware_sensors/) | IMU、温湿度、距离、电流 | 持续扩充 |
| 02 | [微控制器](./docs/02_hardware_microcontrollers/) | STM32 | 基础 |
| 03 | [执行器](./docs/03_hardware_actuators/) | 直流电机、舵机、步进电机驱动 | 整理中 |
| 04 | [电源管理](./docs/04_hardware_power/) | LDO、DCDC、电池保护、低功耗设计 | 初始 |
| 05 | [通信接口/模块](./docs/05_hardware_communication/) | UART、I2C、CAN、WiFi、BLE、LoRa | 整理中 |
| 06 | [测试与调试](./docs/06_hardware_test_debug/) | 逻辑分析仪、示波器使用、焊接技巧 | 经验型 |
| 99 | [其他](./docs/99_misc/) | 接插件、线材、散热、外壳选型 | 随缘 |

- ### 软件/工具类
| 编号 | 分类 | 典型内容 | 状态 |
|------|------|----------|------|
| 07 | [操作系统/中间件](./docs/07_software_os_middleware/) | ROS2、FreeRTOS、Linux 常用命令 |整理中 |
| 08 | [开发工具](./docs/08_software_dev_tools/) | Git、Docker、VS Code、CMake、Jupyter |整理中 |
| 09 | [编程语言/库](./docs/09_software_languages_libs/) | Python 数据类、C++ STL、OpenCV、Eigen |整理中 |

### 🔍 使用示例

- **查找 Git 常用命令**：&emsp;进入 `08_software_dev_tools/` 查看 `git_handbook.md`
- **学习 ROS2 节点通信**：进入 `07_software_os_middleware/` 查看 `ros2_basics.md`


> 每个条目均包含：**关键参数表**、**典型电路（含注意事项）**、**驱动代码示例（实测可用）**、**踩坑记录**、**关联项目**。

---

## 📝 笔记格式

我用了统一的模板（[点此查看](./templates/hardware_template.md)），保证每篇：

- **实测过**；
- **有依据**；
- **能复现**；
- **能关联**；

---

## 🛠️ 怎么维护
- **边做边记**：每完成一个项目阶段，把新用到的硬件整理入库。
- **同门反馈**：师弟师妹用的时候发现坑或者有疑问，直接在对应条目提 Issue 或 PR，我补进去。

---

## 🙏 致谢

感谢实验室导师的指导以及课题组成员的实测反馈。<br>
如果你觉得这个知识库对你有帮助，欢迎 **Star♥** 或提出改进建议。



<!-- 链接<a href="https://github.com/tool-open/tool-open">GitHub</a> -->
<!-- 内联容器<span style="color: red;">内莱鸟</span> -->
<!-- 强调<em>强调文本</em> -->
<!-- 粗体<b>粗体文本</b> -->
<!-- 斜体<i>斜体文本</i> -->
<!-- 高亮<mark>高亮文本</mark> -->
<!-- 删除线<s>删除线文本</s> -->

<!--<p>段落</p>-->
<!-- <details>
  <summary>HTML 速查表</summary>
  <p>行内元素</p>
  <p>区块元素</p>
</details> -->
<!--无序列表<ul><li>列表项1</li><li>列表项2</li></ul>-->
<!--有序列表<ol><li>第一项</li><li>第二项</li></ol>>