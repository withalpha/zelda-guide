"""
简单版菜肴图片批量增强工具
使用PIL库对图片进行基本增强，无需复杂依赖
"""

import os
import sys
from PIL import Image, ImageEnhance, ImageFilter
import shutil
from datetime import datetime

def check_dependencies():
    """检查依赖库"""
    try:
        from PIL import Image
        print("✓ PIL/Pillow 库已安装")
        return True
    except ImportError:
        print("✗ 缺少 PIL/Pillow 库")
        print("请安装: pip install pillow")
        return False

def create_backup(original_dir, backup_dir):
    """创建原始图片备份"""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    print(f"正在备份原始图片到: {backup_dir}")
    
    count = 0
    for filename in os.listdir(original_dir):
        if filename.lower().endswith('.png'):
            src = os.path.join(original_dir, filename)
            dst = os.path.join(backup_dir, filename)
            shutil.copy2(src, dst)
            count += 1
    
    print(f"已备份 {count} 张图片")
    return count

def enhance_image_simple(image_path, output_path, enhancement_level=2):
    """
    简单增强单张图片
    
    Args:
        image_path: 输入图片路径
        output_path: 输出图片路径
        enhancement_level: 增强级别 (1-3)
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 根据增强级别应用不同的处理
        if enhancement_level == 1:
            # 轻度增强
            # 锐化
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
            
            # 对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
        elif enhancement_level == 2:
            # 中度增强 (推荐)
            # 先应用轻微降噪
            img = img.filter(ImageFilter.SMOOTH_MORE)
            
            # 锐化
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            
            # 对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # 亮度
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.05)
            
            # 色彩饱和度
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            
        elif enhancement_level == 3:
            # 强力增强
            # 降噪
            img = img.filter(ImageFilter.SMOOTH_MORE)
            
            # 边缘增强
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            
            # 锐化
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.5)
            
            # 对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            
            # 亮度
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
            
            # 色彩饱和度
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.15)
        
        # 保存图片，优化PNG压缩
        img.save(output_path, 'PNG', optimize=True)
        return True
        
    except Exception as e:
        print(f"处理图片时出错: {e}")
        return False

def batch_enhance_images(input_dir, enhancement_level=2, backup=True):
    """
    批量增强图片
    
    Args:
        input_dir: 输入目录
        enhancement_level: 增强级别 (1-3)
        backup: 是否备份原始图片
    """
    # 检查目录
    if not os.path.exists(input_dir):
        print(f"错误: 目录不存在 - {input_dir}")
        return 0, 0
    
    # 获取所有PNG图片
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    image_files.sort()
    
    if not image_files:
        print("错误: 目录中没有PNG图片")
        return 0, 0
    
    print(f"找到 {len(image_files)} 张PNG图片")
    
    # 创建备份
    backup_dir = None
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(os.path.dirname(input_dir), f'dishes_backup_{timestamp}')
        create_backup(input_dir, backup_dir)
    
    # 处理图片
    print(f"\n开始处理图片，增强级别: {enhancement_level}")
    print("-" * 50)
    
    success_count = 0
    fail_count = 0
    
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, filename)
        output_path = input_path  # 覆盖原文件
        
        print(f"[{i:3d}/{len(image_files):3d}] 处理: {filename}", end="")
        
        if enhance_image_simple(input_path, output_path, enhancement_level):
            print(" ✓ 完成")
            success_count += 1
        else:
            print(" ✗ 失败")
            fail_count += 1
    
    # 显示结果
    print("\n" + "=" * 50)
    print("处理完成!")
    print(f"总图片数: {len(image_files)}")
    print(f"成功处理: {success_count}")
    print(f"处理失败: {fail_count}")
    
    if backup and backup_dir:
        print(f"\n原始图片已备份到: {backup_dir}")
        print("如果对效果不满意，可以从备份目录恢复原始图片")
    
    return success_count, fail_count

def main():
    """主函数"""
    print("=" * 60)
    print("菜肴图片批量增强工具 (简单版)")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 设置路径
    input_dir = r"images\cooking\dishes"
    
    # 如果相对路径不存在，尝试绝对路径
    if not os.path.exists(input_dir):
        input_dir = r"c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\cooking\dishes"
    
    print(f"\n图片目录: {input_dir}")
    
    # 检查目录
    if not os.path.exists(input_dir):
        print(f"错误: 目录不存在 - {input_dir}")
        print("请确保路径正确")
        return
    
    # 显示增强选项
    print("\n请选择增强级别:")
    print("  1. 轻度增强 - 基本锐化和对比度调整")
    print("  2. 中度增强 - 推荐，综合增强 (降噪+锐化+对比度)")
    print("  3. 强力增强 - 最大清晰度，可能过度处理")
    
    try:
        choice = input("请输入选择 (1-3, 默认2): ").strip()
        if choice == '':
            choice = '2'
        enhancement_level = int(choice)
        
        if enhancement_level < 1 or enhancement_level > 3:
            print("输入无效，使用默认值2")
            enhancement_level = 2
    except ValueError:
        print("输入无效，使用默认值2")
        enhancement_level = 2
    
    # 询问是否备份
    backup_choice = input("是否备份原始图片? (y/n, 默认y): ").strip().lower()
    backup = backup_choice != 'n'
    
    print("\n" + "=" * 60)
    
    # 开始处理
    success, fail = batch_enhance_images(input_dir, enhancement_level, backup)
    
    print("\n" + "=" * 60)
    print("提示:")
    print("1. 处理后的图片已覆盖原文件")
    print("2. 如果对效果不满意，可以从备份目录恢复")
    print("3. 可以重新运行脚本选择不同的增强级别")
    print("4. 对于个别图片，可以使用图片编辑软件手动调整")

if __name__ == "__main__":
    main()