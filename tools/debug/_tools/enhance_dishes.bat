@echo off
chcp 65001 >nul
echo ========================================
echo 菜肴图片批量增强工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查PIL/Pillow库
echo 检查依赖库...
python -c "from PIL import Image" >nul 2>&1
if errorlevel 1 (
    echo 正在安装Pillow库...
    pip install pillow
    if errorlevel 1 (
        echo 安装失败，请手动运行: pip install pillow
        pause
        exit /b 1
    )
    echo Pillow库安装成功!
) else (
    echo ✓ Pillow库已安装
)

echo.
echo 开始处理图片...
echo.

REM 运行增强脚本
python simple_enhance_dishes.py

echo.
pause