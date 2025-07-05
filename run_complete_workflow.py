#!/usr/bin/env python3
"""
完整的工作流程：数据处理 + 射线追踪
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"执行: {description}")
    print(f"命令: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ 成功!")
        if result.stdout:
            print("输出:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 失败!")
        print(f"错误: {e}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False

def main():
    print("🚀 开始完整工作流程")
    print("="*50)
    
    # 检查输入文件
    skin_input = "data/skin.obj"
    thyroid_input = "data/thyroid_point_cloud.ply"
    
    if not os.path.exists(skin_input):
        print(f"❌ 错误: 找不到皮肤模型文件 {skin_input}")
        return
    
    if not os.path.exists(thyroid_input):
        print(f"❌ 错误: 找不到甲状腺点云文件 {thyroid_input}")
        return
    
    # 阶段1: 数据处理
    print("\n📁 阶段1: 数据处理")
    print("处理皮肤模型和甲状腺点云，确保对齐...")
    
    if not run_command("cd data_process && python process_all_data.py", "处理所有数据"):
        return
    
    # 阶段2: 特征点提取
    print("\n🔧 阶段2: 特征点提取")
    print("从处理后的甲状腺点云中提取特征点...")
    
    if not run_command("cd src && python preprocess.py", "提取甲状腺特征点"):
        return
    
    # 阶段3: 射线追踪实验
    print("\n🧪 阶段3: 射线追踪实验")
    print("执行射线追踪实验...")
    
    if not run_command("cd src && python main.py", "执行射线追踪实验"):
        return
    
    # 阶段4: 显示结果
    print("\n📊 阶段4: 查看结果")
    results_dir = Path("output/results")
    if results_dir.exists():
        print("✅ 实验结果已生成:")
        for exp_dir in results_dir.iterdir():
            if exp_dir.is_dir():
                print(f"  📁 {exp_dir.name}/")
                for file in exp_dir.iterdir():
                    print(f"    📄 {file.name}")
    else:
        print("❌ 未找到结果目录")
    
    print("\n🎉 完整工作流程完成!")
    print("\n📁 生成的文件:")
    print("  📄 output/preprocessed/skin_processed_withparams.obj - 处理后的皮肤模型")
    print("  📄 output/preprocessed/thyroid_processed.ply - 处理后的甲状腺点云")
    print("  📄 output/preprocessed/thyroid_points.ply - 甲状腺特征点")
    print("  📄 output/results/ - 射线追踪实验结果")

if __name__ == "__main__":
    main() 