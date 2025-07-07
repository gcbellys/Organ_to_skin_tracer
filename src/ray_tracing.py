#!/usr/bin/env python3
"""
射线追踪主模块
该模块负责执行从器官关键点到皮肤模型的射线追踪实验。
它接受倾斜角(alpha)和方位角(theta)作为输入，以控制射线方向。
结果会按照README.md中定义的结构进行保存。
"""

import trimesh
import numpy as np
import argparse
import os
import json
from datetime import datetime
from pathlib import Path
import sys

# 导入项目内的工具模块
from geometry_utils import get_direction_from_angles
from config import get_paths

def load_key_points(file_path):
    """从OBJ文件中加载顶点作为关键点。"""
    points = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                points.append([float(p) for p in parts[1:4]])
    return np.array(points)

def run_ray_tracing(source_organ_name, target_organ_name, alpha_deg, theta_deg):
    """
    执行从源器官关键点到目标器官模型的射线追踪。
    """
    print("--- 开始射线追踪实验 ---")
    
    # 1. Get all necessary paths using the new config system
    source_paths = get_paths(source_organ_name)
    target_paths = get_paths(target_organ_name)

    key_points_path = source_paths.get("processed_keypoints")
    if not key_points_path or not os.path.exists(str(key_points_path)):
        print(f"未找到预处理的关键点，将使用源器官模型本身作为点云: {source_paths['processed_model']}")
        key_points_path = source_paths['processed_model']

    skin_mesh_path = target_paths["processed_model"]
    mapping_path = source_paths.get("keypoints_mapping")

    print(f"加载目标模型: {skin_mesh_path}")
    skin_mesh = trimesh.load(skin_mesh_path, force='mesh')
    
    print(f"加载源关键点: {key_points_path}")
    source_points = load_key_points(key_points_path)
    print(f"加载了 {len(source_points)} 个关键点。")

    point_names = []
    if mapping_path and os.path.exists(str(mapping_path)):
        print(f"加载名称映射文件: {mapping_path}")
        with open(mapping_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        point_names = list(mapping.keys())
        if len(point_names) != len(source_points):
            point_names = [f"Point_{i+1}" for i in range(len(source_points))]
    else:
        point_names = [f"Point_{i+1}" for i in range(len(source_points))]

    ray_direction = get_direction_from_angles(alpha_deg, theta_deg)
    locations, index_ray, index_tri = skin_mesh.ray.intersects_location(
        ray_origins=source_points,
        ray_directions=np.tile(ray_direction, (len(source_points), 1))
    )
    
    results = []
    hit_map = {i: [] for i in range(len(source_points))}
    for loc, ray_idx, tri_idx in zip(locations, index_ray, index_tri):
        hit_map[ray_idx].append((loc, tri_idx))

    for i in range(len(source_points)):
        result_entry = {
            "source_point_index": i, "source_point_name": point_names[i],
            "source_coord": source_points[i].tolist(), "hit": False,
            "intersection_coord": None, "face_id": None, "distance": None
        }
        if i in hit_map and hit_map[i]:
            locations_only = np.array([item[0] for item in hit_map[i]])
            distances = np.linalg.norm(locations_only - source_points[i], axis=1)
            closest_hit_index = np.argmin(distances)
            result_entry.update({
                "intersection_coord": locations_only[closest_hit_index].tolist(),
                "face_id": int(hit_map[i][closest_hit_index][1]),
                "distance": distances[closest_hit_index], "hit": True
            })
        results.append(result_entry)
        
    return results, ray_direction

def save_results(output_path, results, params, ray_direction, skin_mesh_path, key_points_path, mapping_path=None):
    """
    按照项目规范保存所有结果。
    """
    # 确保输出目录存在
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # 1. 准备元数据
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'parameters': params,
        'ray_direction_vector': ray_direction.tolist(),
        'input_files': {
            'skin_mesh': str(Path(skin_mesh_path).name),
            'key_points': str(Path(key_points_path).name)
        },
        'results_summary': {
            'total_source_points': len(results),
            'rays_that_hit': sum(1 for r in results if r['hit'])
        },
        'intersections': results  # 包含所有信息的完整列表
    }

    if mapping_path:
        metadata['input_files']['point_mapping'] = str(Path(mapping_path).name)
    
    # 2. 保存元数据 JSON 文件
    json_path = Path(output_path) / "ray_trace_result.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"  - 元数据已保存: {json_path}")
    
    # 提取有效的交点
    valid_intersections = [r for r in results if r['hit']]

    # 3. 保存交点 OBJ 文件
    if valid_intersections:
        obj_path = Path(output_path) / "intersections.obj"
        with open(obj_path, 'w', encoding='utf-8') as f:
            f.write(f"# 射线交点 from alpha={params['alpha_deg']}, theta={params['theta_deg']}\n")
            for r in valid_intersections:
                p = r['intersection_coord']
                f.write(f"v {p[0]:.6f} {p[1]:.6f} {p[2]:.6f} # name: {r['source_point_name']}, face_id: {r['face_id']}\n")
        print(f"  - 交点OBJ已保存: {obj_path}")

    # 4. 保存源点-交点对 OBJ 文件
    if valid_intersections:
        pairs_path = Path(output_path) / "ray_pairs.obj"
        with open(pairs_path, 'w', encoding='utf-8') as f:
            f.write(f"# 源点-交点对 from alpha={params['alpha_deg']}, theta={params['theta_deg']}\n")
            vertex_counter = 1
            for r in valid_intersections:
                s = r['source_coord']
                t = r['intersection_coord']
                f.write(f"# Pair for: {r['source_point_name']}\n")
                f.write(f"v {s[0]:.6f} {s[1]:.6f} {s[2]:.6f} # Source\n")
                f.write(f"v {t[0]:.6f} {t[1]:.6f} {t[2]:.6f} # Target\n")
                f.write(f"l {vertex_counter} {vertex_counter + 1}\n")
                vertex_counter += 2
        print(f"  - 射线对OBJ已保存: {pairs_path}")
    
    print("--- 结果保存完毕 ---")


def main():
    parser = argparse.ArgumentParser(
        description="从源器官向目标模型执行参数化射线追踪。"
    )
    parser.add_argument("--source", required=True, help="源器官的名称 (e.g., 'heart', 'thyroid').")
    parser.add_argument("--target", default="skin", help="目标器官的名称 (默认为 'skin').")
    parser.add_argument("--alpha", type=float, required=True, help="射线的倾斜角 (alpha)，单位：度。")
    parser.add_argument("--theta", type=float, required=True, help="射线的方位角 (theta)，单位：度。")
    parser.add_argument("--output_dir", default=None, help="保存结果的自定义目录。默认为 'output/results/<source>_to_<target>/'")

    args = parser.parse_args()

    # Correctly call run_ray_tracing with organ names
    results, ray_direction = run_ray_tracing(
        args.source,
        args.target,
        args.alpha,
        args.theta
    )

    if not results:
        print("射线追踪未生成任何结果。")
        return

    # --- Prepare paths for saving results ---
    source_paths = get_paths(args.source)
    target_paths = get_paths(args.target)
    
    key_points_path = source_paths.get("processed_keypoints")
    if not key_points_path or not os.path.exists(str(key_points_path)):
        key_points_path = source_paths['processed_model']
        
    skin_mesh_path = target_paths['processed_model']
    mapping_file = source_paths.get('keypoints_mapping')

    if args.output_dir:
        output_base_dir = args.output_dir
    else:
        output_base_dir = os.path.join(BASE_DIR, "output", "results", f"{args.source}_to_{args.target}")
        
    output_path_str = os.path.join(output_base_dir, f"alpha_{args.alpha}_theta_{args.theta}")
    
    save_results(
        output_path_str,
        results,
        {"alpha_deg": args.alpha, "theta_deg": args.theta},
        ray_direction,
        skin_mesh_path,
        key_points_path,
        mapping_file
    )

if __name__ == "__main__":
    # Add path to src for imports
    sys.path.append(str(Path(__file__).resolve().parent))
    from config import BASE_DIR
    main() 