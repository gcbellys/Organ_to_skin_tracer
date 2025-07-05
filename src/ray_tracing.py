#!/usr/bin/env python3
"""
射线追踪：从甲状腺关键点出发计算逆射线与皮肤模型的交点
"""

import trimesh
import numpy as np
import argparse
import os
import json
from pathlib import Path


def get_direction_from_angles(alpha_deg, theta_deg):
    """
    根据给定的倾斜角(alpha)和方位角(theta)计算方向向量
    
    Args:
        alpha_deg: 倾斜角(度)
        theta_deg: 方位角(度)
    
    Returns:
        np.ndarray: 方向向量
    """
    alpha_rad = np.deg2rad(alpha_deg)
    theta_rad = np.deg2rad(theta_deg)
    
    # 标准参考系 - 修正：D_base应该是从前方指向后方的单位向量
    D_base = np.array([0, 1, 0])  # 前方(Y+)指向后方(Y-)
    V_up = np.array([0, 0, 1])    # 上方(Z+)
    V_left = np.array([1, 0, 0])  # 左侧(X+)
    
    comp_base = np.cos(alpha_rad)
    perp_magnitude = np.sin(alpha_rad)
    comp_up = perp_magnitude * np.cos(theta_rad)
    comp_left = perp_magnitude * np.sin(theta_rad)
    
    final_direction = (D_base * comp_base) + (V_up * comp_up) + (V_left * comp_left)
    return final_direction


def calculate_inverse_angles(alpha_deg, theta_deg):
    """
    计算逆射线的角度
    
    Args:
        alpha_deg: 原始倾斜角(度)
        theta_deg: 原始方位角(度)
    
    Returns:
        tuple: (alpha1, theta1) 逆射线的角度
    """
    # 对于从前方射入的情况，我们需要修正计算
    # 如果原始角度是正面射入(α=0, θ=0)，那么逆射线应该也是正面射入
    if alpha_deg == 0 and theta_deg == 0:
        return 0, 0
    
    # 其他情况：逆射线就是反向
    alpha1 = 180 - alpha_deg
    
    # theta1 = theta + 180 (方位角旋转180度)
    theta1 = (theta_deg + 180) % 360
    
    return alpha1, theta1


def ray_trace_from_points(key_points_path, skin_mesh_path, alpha_deg, theta_deg, output_dir):
    """
    从关键点进行射线追踪
    
    Args:
        key_points_path: 甲状腺关键点文件路径
        skin_mesh_path: 皮肤模型文件路径
        alpha_deg: 倾斜角(度)
        theta_deg: 方位角(度)
        output_dir: 输出目录
    """
    print(f"--- 开始射线追踪 ---")
    print(f"关键点文件: {key_points_path}")
    print(f"皮肤模型: {skin_mesh_path}")
    print(f"原始角度: α={alpha_deg}°, θ={theta_deg}°")
    
    # 加载甲状腺关键点
    print(f"\n加载甲状腺关键点...")
    key_points = []
    with open(key_points_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                key_points.append([x, y, z])
    
    key_points = np.array(key_points)
    print(f"加载了 {len(key_points)} 个关键点")
    
    # 加载皮肤模型
    print(f"加载皮肤模型...")
    skin_mesh = trimesh.load(skin_mesh_path, process=False)
    print(f"皮肤模型顶点数: {len(skin_mesh.vertices)}")
    
    # 计算逆射线角度
    alpha1, theta1 = calculate_inverse_angles(alpha_deg, theta_deg)
    print(f"逆射线角度: α1={alpha1}°, θ1={theta1}°")
    
    # 计算逆射线方向 - 从皮肤前方射向甲状腺
    ray_direction = get_direction_from_angles(alpha1, theta1)
    print(f"逆射线方向向量: {ray_direction}")
    
    # 验证射线方向：从前方射入应该是Y轴正方向
    if alpha_deg == 0 and theta_deg == 0:
        expected_direction = np.array([0, 1, 0])  # 从前方(Y+)射向后方(Y-)
        print(f"期望的正面射入方向: {expected_direction}")
        print(f"实际计算方向: {ray_direction}")
        if not np.allclose(ray_direction, expected_direction):
            print("警告：方向计算可能有问题！")
    
    # 进行射线追踪
    print(f"\n开始射线追踪...")
    intersections = []
    point_names = ["重心", "X最小值", "X最大值", "Y最小值", "Y最大值", "Z最小值", "Z最大值"]
    
    for i, (point, name) in enumerate(zip(key_points, point_names)):
        print(f"  处理点 {i+1}: {name} {point}")
        
        # 计算射线与皮肤模型的交点
        locations, index_ray, index_tri = skin_mesh.ray.intersects_location(
            ray_origins=[point],
            ray_directions=[ray_direction]
        )
        
        if len(locations) > 0:
            # 取第一个交点（最近的点）
            intersection = locations[0]
            intersections.append({
                'point_index': i,
                'point_name': name,
                'source_point': point.tolist(),
                'intersection_point': intersection.tolist(),
                'distance': np.linalg.norm(intersection - point)
            })
            print(f"    找到交点: {intersection}, 距离: {np.linalg.norm(intersection - point):.6f}")
        else:
            print(f"    未找到交点")
            intersections.append({
                'point_index': i,
                'point_name': name,
                'source_point': point.tolist(),
                'intersection_point': None,
                'distance': None
            })
    
    # 保存结果
    print(f"\n保存结果...")
    
    # 创建按角度命名的子目录
    angle_subdir = f"alpha_{int(alpha_deg)}_theta_{int(theta_deg)}"
    result_dir = os.path.join(output_dir, angle_subdir)
    os.makedirs(result_dir, exist_ok=True)
    
    # 保存JSON格式的详细结果
    result_data = {
        'original_angles': {'alpha': alpha_deg, 'theta': theta_deg},
        'inverse_angles': {'alpha1': alpha1, 'theta1': theta1},
        'ray_direction': ray_direction.tolist(),
        'intersections': intersections,
        'total_points': len(key_points),
        'successful_intersections': len([x for x in intersections if x['intersection_point'] is not None])
    }
    
    json_path = os.path.join(result_dir, 'ray_trace_result.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    # 保存交点坐标为OBJ文件
    valid_intersections = [x for x in intersections if x['intersection_point'] is not None]
    if valid_intersections:
        obj_path = os.path.join(result_dir, 'intersections.obj')
        with open(obj_path, 'w') as f:
            f.write(f"# 射线追踪交点\n")
            f.write(f"# 原始角度: α={alpha_deg}°, θ={theta_deg}°\n")
            f.write(f"# 逆射线角度: α1={alpha1}°, θ1={theta1}°\n")
            f.write(f"# 总点数: {len(valid_intersections)}\n\n")
            
            for intersection in valid_intersections:
                point = intersection['intersection_point']
                name = intersection['point_name']
                f.write(f"v {point[0]:.6f} {point[1]:.6f} {point[2]:.6f}  # {name}\n")
    
    # 保存源点和交点的对应关系
    if valid_intersections:
        pairs_path = os.path.join(result_dir, 'ray_pairs.obj')
        with open(pairs_path, 'w') as f:
            f.write(f"# 射线源点和交点对\n")
            f.write(f"# 原始角度: α={alpha_deg}°, θ={theta_deg}°\n\n")
            
            for intersection in valid_intersections:
                source = intersection['source_point']
                target = intersection['intersection_point']
                name = intersection['point_name']
                f.write(f"# {name}\n")
                f.write(f"v {source[0]:.6f} {source[1]:.6f} {source[2]:.6f}  # 源点\n")
                f.write(f"v {target[0]:.6f} {target[1]:.6f} {target[2]:.6f}  # 交点\n\n")
    
    print(f"结果已保存到: {result_dir}")
    print(f"  JSON结果: {json_path}")
    if valid_intersections:
        print(f"  交点OBJ: {obj_path}")
        print(f"  射线对OBJ: {pairs_path}")
    
    print(f"--- 射线追踪完成 ---")
    print(f"成功找到 {len(valid_intersections)}/{len(key_points)} 个交点")
    
    return result_data


def main():
    parser = argparse.ArgumentParser(description='从甲状腺关键点进行射线追踪')
    parser.add_argument('key_points', help='甲状腺关键点文件路径')
    parser.add_argument('skin_mesh', help='皮肤模型文件路径')
    parser.add_argument('alpha', type=float, help='倾斜角(度)')
    parser.add_argument('theta', type=float, help='方位角(度)')
    parser.add_argument('output_dir', help='输出目录')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.key_points):
        print(f"错误: 关键点文件不存在: {args.key_points}")
        return
    
    if not os.path.exists(args.skin_mesh):
        print(f"错误: 皮肤模型文件不存在: {args.skin_mesh}")
        return
    
    # 进行射线追踪
    result = ray_trace_from_points(
        args.key_points,
        args.skin_mesh,
        args.alpha,
        args.theta,
        args.output_dir
    )


if __name__ == "__main__":
    main() 