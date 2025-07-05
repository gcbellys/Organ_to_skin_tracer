#!/usr/bin/env python3
"""
从甲状腺网格中提取关键点
提取7个点：重心 + x,y,z坐标的最小最大值点
"""

import trimesh
import numpy as np
import argparse
import os


def extract_key_points(mesh_path, output_path):
    """
    从网格中提取关键点
    
    Args:
        mesh_path: 输入网格文件路径
        output_path: 输出点云文件路径
    """
    print(f"--- 开始提取关键点 ---")
    print(f"加载网格文件: {mesh_path}")
    
    # 加载网格
    mesh = trimesh.load(mesh_path, process=False)
    
    # 获取顶点
    vertices = mesh.vertices
    
    print(f"网格顶点数: {len(vertices)}")
    
    # 1. 计算重心
    centroid = mesh.centroid
    print(f"重心: {centroid}")
    
    # 2. 找到x,y,z坐标的最小最大值点
    x_min_idx = np.argmin(vertices[:, 0])
    x_max_idx = np.argmax(vertices[:, 0])
    y_min_idx = np.argmin(vertices[:, 1])
    y_max_idx = np.argmax(vertices[:, 1])
    z_min_idx = np.argmin(vertices[:, 2])
    z_max_idx = np.argmax(vertices[:, 2])
    
    # 提取关键点
    key_points = [
        centroid,  # 重心
        vertices[x_min_idx],  # x最小值点
        vertices[x_max_idx],  # x最大值点
        vertices[y_min_idx],  # y最小值点
        vertices[y_max_idx],  # y最大值点
        vertices[z_min_idx],  # z最小值点
        vertices[z_max_idx]   # z最大值点
    ]
    
    # 转换为numpy数组
    key_points = np.array(key_points)
    
    # 打印关键点信息
    point_names = ["重心", "X最小值", "X最大值", "Y最小值", "Y最大值", "Z最小值", "Z最大值"]
    for i, (name, point) in enumerate(zip(point_names, key_points)):
        print(f"{name} (点{i+1}): {point}")
    
    # 创建只包含点的OBJ文件
    with open(output_path, 'w') as f:
        f.write("# 甲状腺关键点\n")
        f.write(f"# 提取自: {mesh_path}\n")
        f.write(f"# 总点数: {len(key_points)}\n")
        f.write("# 格式: 重心, X最小值, X最大值, Y最小值, Y最大值, Z最小值, Z最大值\n\n")
        
        for i, point in enumerate(key_points):
            f.write(f"v {point[0]:.6f} {point[1]:.6f} {point[2]:.6f}  # {point_names[i]}\n")
    
    print(f"关键点已保存到: {output_path}")
    print(f"--- 关键点提取完成 ---")
    
    return key_points


def main():
    parser = argparse.ArgumentParser(description='从甲状腺网格中提取关键点')
    parser.add_argument('mesh', help='输入网格文件路径')
    parser.add_argument('output', help='输出点云文件路径')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.mesh):
        print(f"错误: 输入文件不存在: {args.mesh}")
        return
    
    # 创建输出目录
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # 提取关键点
    key_points = extract_key_points(args.mesh, args.output)
    
    print(f"\n提取完成！共提取了 {len(key_points)} 个关键点")


if __name__ == "__main__":
    main() 