# src/main.py
import datetime
from config import RESULTS_DIR, DEFAULT_ALPHA_DEG, DEFAULT_THETA_DEG
from data_loader import load_data, validate_setup
from geometry_utils import transform_scene, get_direction_from_angles, calculate_intersections
from io_utils import save_experiment_results

def run_single_experiment(alpha_deg, theta_deg):
    """执行一次完整的实验：加载、计算、保存。"""
    
    print(f"\n--- 开始实验: alpha={alpha_deg}, theta={theta_deg} ---")
    
    # 1. 加载和校验
    skin_mesh, thyroid_points = load_data()
    if not validate_setup(skin_mesh, thyroid_points):
        return # 如果数据有问题，则停止本次实验

    # 2. 坐标系变换
    skin_mesh, thyroid_points = transform_scene(skin_mesh, thyroid_points)
    
    # 3. 计算射线方向
    # 计算从体外射向体内的入射方向（基于解剖学参考系）
    incoming_direction = get_direction_from_angles(alpha_deg, theta_deg)
    # 确定逆向射线的方向（从器官射向皮肤）
    ray_direction = -incoming_direction
    
    # 4. 执行射线追踪
    intersection_points, source_points = calculate_intersections(
        skin_mesh, thyroid_points, ray_direction
    )
    
    # 5. 创建元数据并保存结果
    metadata = {
        "timestamp": datetime.datetime.now().isoformat(),
        "parameters": {
            "alpha_deg": alpha_deg,
            "theta_deg": theta_deg
        },
        "input_files": {
            "skin": "skin.obj",
            "thyroid_points_source": "thyroid.obj"
        },
        "results_summary": {
            "total_source_points": thyroid_points.n_points,
            "rays_that_hit": len(intersection_points),
        },
        "source_to_intersection_map": [
            {"source_coord": src.tolist(), "intersection_coord": inter.tolist()}
            for src, inter in zip(source_points, intersection_points)
        ]
    }
    
    # 创建本次实验的输出目录
    experiment_dir = RESULTS_DIR / f"alpha_{alpha_deg}_theta_{theta_deg}"
    save_experiment_results(experiment_dir, intersection_points, metadata)
    
    print(f"--- 实验结束: alpha={alpha_deg}, theta={theta_deg} ---")

if __name__ == '__main__':
    # --- 运行一次默认参数的实验 ---
    run_single_experiment(DEFAULT_ALPHA_DEG, DEFAULT_THETA_DEG)
    
    # --- 或者运行一系列实验 ---
    print("\n\n--- 开始批量实验 ---")
    for alpha in [15, 30, 45]:
        for theta in [0, 90, 180, 270]:
            run_single_experiment(alpha, theta) 