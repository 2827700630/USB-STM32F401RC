# STM32 DLC 文件整理工具

## 项目简介

本工具用于自动化整理 STM32 项目开发中 Middlewares 下的 `.c` 和 `.h` 文件，将它们收集到指定的新目录，并自动修正 `.c` 文件中的头文件引用路径，便于统一管理源码，并在 PlatformIO 中极为实用。

在 STM32CubeIDE 或 CubeMX 中使用 Middlewares 组件时，库代码默认分散在根目录下，不便于 platformio 编译。使用本工具可自动收集并整理代码，便于在 platformio 或其他跨平台环境统一管理和引用。

**主要功能：**
- 自动收集 `.c` 文件到 `Core/Src/DLCc`
- 自动收集 `.h` 文件到 `Core/Inc/DLCh`
- 自动修正 `.c` 文件中的头文件引用（如 `#include "xxx.h"` 替换为 `#include "DLCh/xxx.h"`，支持排除如 `stm32f4xx.h` 这类头文件）
- 自动生成 `Core/Inc/all_dlch_includes.h`，一键包含所有 USB 相关头文件
- 支持无 Python 环境运行（自动下载便携版 Python）

---

## 使用方法

### 1. 运行方式

#### 推荐方式一：双击批处理启动器

- 直接双击 `collect_DLC_files_launcher.bat`  
  无需本地 Python 环境，脚本会自动检测并下载安装便携版 Python。

#### 方式二：手动运行 Python 脚本

```bash
python collect_DLC_files.py
```

### 2. 脚本说明

核心脚本为 `collect_DLC_files.py`，支持源码收集、头文件路径修正和统一包含头文件的自动生成。

#### 工作原理

- **遍历范围**  
  默认遍历项目根目录下的 `Middlewares` 和 `USB_DEVICE`（可自定义）。
- **文件分类**  
  - 所有 `.c` 文件复制到 `Core/Src/DLCc/`
  - 所有 `.h` 文件复制到 `Core/Inc/DLCh/`
- **头文件路径修正**  
  复制 `.c` 文件时自动将 `#include "xxx.h"` 替换为 `#include "DLCh/xxx.h"`，以适配新结构。
  - 以 `stm32` 开头的头文件不会被修正，避免破坏官方库引用。
- **自动生成统一头文件**  
  在 `Core/Inc/` 目录自动生成 `all_dlch_includes.h`，内容为所有收集到头文件的 `#include "DLCh/xxx.h"`。

#### 自定义遍历目录

如需修改遍历目录，编辑脚本顶部的 `SEARCH_DIRS` 列表，例如：

```python
SEARCH_DIRS = [
    "Middlewares",
    "USB_DEVICE",
    "Drivers"   # 增加 Drivers 目录
]
```

---

### 3. 整理结果

- `.c` 文件移动至：`Core/Src/DLCc`
- `.h` 文件移动至：`Core/Inc/DLCh`
- 自动生成 `Core/Inc/all_dlch_includes.h`，内容如：

  ```c
  #include "DLCh/usb_device.h"
  #include "DLCh/usbd_core.h"
  // ...自动枚举所有头文件
  ```

- 只需在 `main.c` 中：

  ```c
  #include "all_dlch_includes.h"
  ```

  即可一次性包含所有 USB 相关头文件。

---

### 4. 典型使用流程（以 STM32 USB 虚拟串口为例）

#### 4.1 使用 STM32CubeMX/IDE 新建工程

1. **新建工程**：选择目标芯片或板卡
2. **配置 Pinout & 时钟**：配置系统时钟和 Debug 接口
3. **配置 USB**：在 Connectivity 分类里启用 `USB_OTG_FS`（或 HS），选择 Device Only
4. **配置 Middlewares**：启用 `USB_DEVICE`，Class 选择 CDC（虚拟串口）
5. **生成代码**：点击 Generate Code

#### 4.2 整理 DLC 文件

1. 将 `collect_DLC_files_launcher.bat` 和 `collect_DLC_files.py` 和 `platformio.ini` 复制到工程根目录
2. 运行批处理启动器，自动完成文件收集、头文件修正、头文件总生成
3. 整理完成后：
   - `Core/Src/DLCc`：存放所有 USB 相关 `.c` 文件
   - `Core/Inc/DLCh`：存放所有 USB 相关 `.h` 文件
   - `Core/Inc/all_dlch_includes.h`：汇总所有头文件
4. 使用VSCode打开工程文件夹

#### 4.3 main.c 示例改写

```c
/* Includes ------------------------------------------------------------------*/
#include "main.h"
//#include "usb_device.h" // 在 PlatformIO 中建议注释
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "all_dlch_includes.h" // 在 STM32CubeIDE 中建议注释，在 PlatformIO 中启用
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

> - 在 STM32CubeIDE 下通常只 `#include "usb_device.h"`
> - 在 PlatformIO 下建议用 `#include "all_dlch_includes.h"`，避免头文件遗漏
> - 烧录后，使用串口助手可以看到STM32发来的消息

---

## 注意事项

- 如需回到 STM32CubeIDE 原生开发，只需删除 `DLCc`、`DLCh` 文件夹及 `all_dlch_includes.h`，恢复默认头文件引用
- 工具适用于 CubeMX 代码生成后，跨平台移植和头文件管理
- 若有特殊需求请查阅脚本源码或提交 Issue

**补充说明：**
- 工具仅遍历根目录下 `Middlewares` 和 `USB_DEVICE` 文件夹
- 仅修正简单 `#include "xxx.h"`，不会处理复杂路径
- 以 `stm32` 开头的头文件不会被路径修正，避免与官方库冲突

---