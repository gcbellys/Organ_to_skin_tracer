# src/io_utils.py
import pyvista as pv
import numpy as np
import json
import os
from datetime import datetime

def save_experiment_results(output_dir, intersection_points, metadata):
    """将交点保存为PLY，元数据保存为JSON。"""
    # 确保实验结果文件夹存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 保存PLY文件
    if intersection_points.any():
        intersection_cloud = pv.PolyData(intersection_points)
        ply_path = output_dir / "intersection_points.ply"
        intersection_cloud.save(ply_path, binary=True)
        print(f"交点已保存至: {ply_path}")
    
    # 2. 保存JSON文件
    json_path = output_dir / "metadata.json"
    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"元数据已保存至: {json_path}") 