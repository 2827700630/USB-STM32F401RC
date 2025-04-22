@echo off
chcp 65001 > nul
title STM32 DLC收集器启动器
color 0B

echo             /\_____/\
echo            /  o   o  \
echo           ( ==  w  == )
echo            )         (
echo           (           )
echo          ( (  )   (  ) )
echo         (__(__)___(__)__)
echo             雪豹  编写
 

echo [信息] 正在准备STM32 DLC自动整理工具...

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 检测到已安装的Python环境，开始执行文件整理脚本...
    python collect_DLC_files.py
) else (
    :: 如果没有安装Python,使用内置的便携版Python
    echo 未检测到Python，开始准备便携版Python环境...
    if not exist "python_portable" (
        echo 第一次运行，将下载并解压便携版Python，请稍候...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip' -OutFile 'python.zip'}"
        md python_portable
        powershell -Command "& {Expand-Archive -Path 'python.zip' -DestinationPath 'python_portable' -Force}"
        del python.zip
    )
    echo 便携Python环境准备完毕!
    echo 正在执行文件整理脚本...
    .\python_portable\python.exe collect_DLC_files.py
)

:: 如果发生错误则暂停
if errorlevel 1 (
    echo 文件整理失败!
    echo 请检查网络连接或联系技术支持。
    pause
    exit /b 1
)

:: 正常退出
echo 文件整理完毕，按任意键退出...
pause
exit /b 0