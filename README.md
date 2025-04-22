# STM32 DLC 文件整理工具

## 项目简介

本工具用于自动化整理 STM32 项目开发中常见的 Middlewares 下的 `.c` 和 `.h` 文件，将它们收集到指定的新目录，并自动修正 `.c` 文件中的头文件引用路径，方便嵌入式开发者统一管理和引用 USB 相关源码。

> **特色功能：**
> - 自动收集 `.c` 文件到 `Core/Src/DLCc`
> - 自动收集 `.h` 文件到 `Core/Inc/DLCh`
> - 自动修正 `.c` 文件中的头文件引用（将 `#include "xxx.h"` 替换为 `#include "DLCh/xxx.h"`，支持排除如 `stm32f4xx.h` 这类头文件）
> - 自动生成 `Core/Inc/all_dlch_includes.h`，一键包含所有 USB 相关头文件
> - 支持无 Python 环境运行（自动下载便携版 Python）

---

## 使用方法

### 1. 运行方式

#### 方式一：直接运行批处理启动器

双击运行 `STM32_DLC收集器启动器.bat.bat`  
无需本地 Python 环境，脚本会自动检测并下载安装便携版 Python。

#### 方式二：手动运行 Python 脚本

手动运行collect_DLC_files.py

```bash
python collect_DLC_files.py
```

---

### 2. 整理结果

- 所有 `.c` 文件将被移动到：`Core/Src/DLCc`
- 所有 `.h` 文件将被移动到：`Core/Inc/DLCh`
- 自动生成 `Core/Inc/all_DLC_includes.h`
    - 内容为：
      ```c
      #include "DLCh/usb_device.h"
      #include "DLCh/usbd_core.h"
      // ...自动枚举所有收集到的头文件
      ```
- 你只需在 `main.c` 中：
    ```c
    #include "all_DLC_includes.h"
    ```
    即可自动包含所有 USB 相关头文件。

---

### 3. 具体使用过程（以STM32 USB虚拟串口为例）

#### 3.1 在 STM32CubeMX/STM32CubeIDE 中新建工程并基本配置

1. **新建工程**  
   打开 STM32CubeMX 或 STM32CubeIDE，新建一个空白工程，选择你的目标芯片型号或开发板。

2. **基础配置**  
   - 进入【Pinout & Configuration】界面，配置好**系统时钟（RCC）**以及**Debug接口（SYS → Serial Wire）**。
   - 确保“配置时钟树”使 USB 工作时钟为 48MHz（如 HSE/HSI 时钟源经 PLL 输出 48MHz 到 USB）。
   - 打开【Configuration】窗口，进入“System Core”中的“RCC”，选择合适的时钟源。
   - 在“Project Manager”中填写工程名、保存路径等基本信息。

3. **USB 配置**
   - 在【Pinout & Configuration】界面，找到 `Connectivity` 分类，点击 `USB_OTG_FS`（或 `USB_OTG_HS`，取决于你的芯片）。
   - 选择“Device Only”模式。  
     > 其他配置保持默认即可，不需要额外设置。

4. **中间件（Middlewares）配置**
   - 进入【Configuration】窗口，找到“Middleware”部分，选择并启用 “USB_DEVICE”。
   - 在弹出配置窗口里，选择“Class For FS IP”为“Communication Device Class (Virtual Port Com)”（即虚拟串口 CDC）。
   - 其他参数可保持默认。

5. **生成代码**
   - 点击“Project -> Generate Code”生成 CubeMX 工程代码（或在 CubeIDE 直接生成）。
   - 生成后，关闭 CubeMX，使用 CubeIDE 打开工程。

#### 3.2 使用本仓库工具进行代码整理

1. 将本仓库的 `collect_DLC_files_launcher.bat` 和 `collect_DLC_files.py` 复制到 CubeMX 生成的工程根目录下（与 Middlewares、USB_DEVICE 等文件夹同级）。
2. **运行批处理启动器**  
   双击 `collect_DLC_files_launcher.bat`，依次完成文件收集、头文件修正与自动生成总头文件。
3. 整理完成后，你会看到：
   - `Core/Src/DLCc` 目录下存放所有 USB 相关 `.c` 文件
   - `Core/Inc/DLCh` 目录下存放所有 USB 相关 `.h` 文件
   - `Core/Inc/all_dlch_includes.h` 汇总所有头文件

#### 3.3 main.c 示例改写

将你的 `main.c` 文件按如下方式进行修改：

```c
/* Includes ------------------------------------------------------------------*/
#include "main.h"
//#include "usb_device.h" // 在 PlatformIO 中需要注释
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "all_dlch_includes.h" // 在 STM32CubeIDE 中需要注释，在 PlatformIO 中不用注释
/* USER CODE END Includes */

int main(void) {

  /* USER CODE BEGIN WHILE */
  while (1) {
    uint8_t data[] = "Hello USB Virtual COM!\r\n";
    CDC_Transmit_FS(data, sizeof(data)-1);
    HAL_Delay(1000);
  /* USER CODE END WHILE */
  }
}
```

- **注意：**  
  - 在 STM32CubeIDE 下，通常直接 `#include "usb_device.h"`，而不要 `#include "all_dlch_includes.h"`。
  - 在 PlatformIO 或其他跨平台环境下，建议注释 `usb_device.h`，使用 `all_dlch_includes.h`，确保能一次包含所有 USB 相关头文件。

---

## 注意事项

- 如果要回到 STM32CubeIDE 原生开发，只需**删除 `DLCc` 和 `DLCh` 两个文件夹及 `all_dlch_includes.h` 文件**，恢复默认的头文件引用方式即可。
- 本工具适合 CubeMX 生成代码后，进行跨平台移植和统一头文件管理的场景。
- 若有特殊自定义需求，请参阅脚本源码或提交 Issue。

- 本工具仅遍历项目根目录下的 `Middlewares` 和 `USB_DEVICE` 文件夹。
- 仅修正简单头文件引用（`#include "xxx.h"`），不会处理复杂路径引用。
- 以 `stm32` 开头的头文件不会被路径修正，避免与官方库冲突。

---
