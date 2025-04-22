import os
import shutil
from pathlib import Path

def collect_ch_files_to_flat_dirs(project_root, out_src, out_inc):
    # 可自定义：只遍历这些顶级目录
    SEARCH_DIRS = [
        "Middlewares",
        "USB_DEVICE"
    ]

    # 创建目标文件夹（如果不存在则创建）
    Path(out_src).mkdir(parents=True, exist_ok=True)
    Path(out_inc).mkdir(parents=True, exist_ok=True)

    for folder in SEARCH_DIRS:
        folder_path = os.path.join(project_root, folder)
        # 跳过不存在的目录
        if not os.path.exists(folder_path):
            continue
        # 递归遍历该目录下所有文件
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                lower = file.lower()
                src_path = os.path.join(root, file)
                # 如果是.c文件，复制到 out_src（目标src文件夹）
                if lower.endswith('.c'):
                    dst = os.path.join(out_src, file)
                    # 若目标已存在同名文件，直接覆盖
                    shutil.copy2(src_path, dst)
                    print(f"Copy {src_path} -> {dst}")
                # 如果是.h文件，复制到 out_inc（目标inc文件夹）
                elif lower.endswith('.h'):
                    dst = os.path.join(out_inc, file)
                    # 若目标已存在同名文件，直接覆盖
                    shutil.copy2(src_path, dst)
                    print(f"Copy {src_path} -> {dst}")

if __name__ == "__main__":
    # 获取当前脚本所在的根目录
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # 指定收集到的.c文件和.h文件存放的目录
    OUT_SRC = os.path.join(PROJECT_ROOT, 'Additional', 'src')
    OUT_INC = os.path.join(PROJECT_ROOT, 'Additional', 'inc')
    # 执行文件收集
    collect_ch_files_to_flat_dirs(PROJECT_ROOT, OUT_SRC, OUT_INC)
    print("Done! 所有.c文件已在 Additional/src，所有.h文件已在 Additional/inc。")