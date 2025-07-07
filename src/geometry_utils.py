# src/geometry_utils.py
import numpy as np

def get_direction_from_angles(alpha_deg, theta_deg):
    """
    根据给定的倾斜角(alpha)和方位角(theta)计算最终的入射方向向量。

    解剖学坐标系 (修正后):
    - 基准方向 (D_base): 从正前方射入 (0, 0, 1) - Z轴正方向
    - 上方 (V_up): 指向头顶 (0, 1, 0) - Y轴正方向
    - 左侧 (V_left): 指向左侧 (-1, 0, 0) - X轴负方向

    参数:
    alpha_deg (float): 倾斜角(度)，与正前方基准方向的夹角。
                      0° = 正前方，90° = 与前方垂直，180° = 正后方
    theta_deg (float): 方位角(度)，围绕基准方向的旋转角度。
                       0° = 朝上，90° = 朝左，180° = 朝下，270° = 朝右

    返回:
    np.ndarray: 计算出的三维单位方向向量。
    """
    # 将角度从度转换为弧度，以便三角函数计算
    alpha_rad = np.deg2rad(alpha_deg)
    theta_rad = np.deg2rad(theta_deg)
    
    # 修正后的标准参考系
    D_base = np.array([0, 0, 1])   # 基准方向：从正前方射入 (Z轴正方向)
    V_up = np.array([0, 1, 0])     # 上方：指向头顶 (Y轴正方向)
    V_left = np.array([-1, 0, 0])  # 左侧：指向左侧 (X轴负方向)

    # 使用球面坐标系的数学原理
    # 最终向量是三个基准向量的线性组合
    # 它的"向前"分量由 cos(alpha) 决定
    comp_base = np.cos(alpha_rad)
    
    # 它的"偏离"分量 (在垂直于D_base的平面上) 的总大小由 sin(alpha) 决定
    perp_magnitude = np.sin(alpha_rad)
    
    # 将偏离分量再次分解到"上下"和"左右"两个方向上
    comp_up = perp_magnitude * np.cos(theta_rad)
    comp_left = perp_magnitude * np.sin(theta_rad)
    
    # 通过加权求和，合成最终的方向向量
    final_direction = (D_base * comp_base) + \
                      (V_up * comp_up) + \
                      (V_left * comp_left)
    
    # 归一化确保向量长度为1 (处理浮点数精度问题)
    norm = np.linalg.norm(final_direction)
    if norm > 1e-9: # 避免除以零
        final_direction = final_direction / norm
    
    return final_direction

def get_direction_from_angles_old(alpha_deg, theta_deg):
    """
    原始版本的函数（保留用于对比）
    根据给定的倾斜角(alpha)和方位角(theta)计算最终的入射方向向量。

    该函数基于一个标准的解剖学参考系：
    - 基准方向 (D_base): 从正前方射入 (0, -1, 0)
    - 上方 (V_up): 指向头顶 (0, 0, 1)

    参数:
    alpha_deg (float): 倾斜角(度)，与正前方基准方向的夹角。
    theta_deg (float): 方位角(度)，围绕基准方向的旋转角度。
                       0度代表朝上，90度代表朝左。

    返回:
    np.ndarray: 计算出的三维单位方向向量。
    """
    # 将角度从度转换为弧度，以便三角函数计算
    alpha_rad = np.deg2rad(alpha_deg)
    theta_rad = np.deg2rad(theta_deg)
    
    # 定义标准参考系
    D_base = np.array([0, -1, 0])  # 基准方向：从正前方射入
    V_up = np.array([0, 0, 1])     # 上方：指向头顶
    V_left = np.cross(D_base, V_up) # 左侧：通过叉乘计算

    # 最终向量是三个基准向量的线性组合
    # 它的"向前"分量由 cos(alpha) 决定
    comp_base = np.cos(alpha_rad)
    
    # 它的"偏离"分量 (在垂直于D_base的平面上) 的总大小由 sin(alpha) 决定
    perp_magnitude = np.sin(alpha_rad)
    
    # 将偏离分量再次分解到"上下"和"左右"两个方向上
    comp_up = perp_magnitude * np.cos(theta_rad)
    comp_left = perp_magnitude * np.sin(theta_rad)
    
    # 通过加权求和，合成最终的方向向量
    final_direction = (D_base * comp_base) + \
                      (V_up * comp_up) + \
                      (V_left * comp_left)
    
    # 归一化确保向量长度为1
    final_direction = final_direction / np.linalg.norm(final_direction)
    
    return final_direction

def transform_scene(skin_mesh, thyroid_points):
    """将场景中心移动到原点。"""
    translation_vector = -np.array(skin_mesh.center)
    skin_mesh.translate(translation_vector, inplace=True)
    thyroid_points.translate(translation_vector, inplace=True)
    return skin_mesh, thyroid_points

def calculate_intersections(skin_mesh, organ_points, ray_direction):
    """对一组点执行射线追踪，返回交点和命中的原始点。"""
    intersection_points = []
    source_points_that_hit = []
    for point in organ_points.points:
        intersections, _ = skin_mesh.ray_trace(point, ray_direction)
        if len(intersections) > 0:
            intersection_points.append(intersections[0])
            source_points_that_hit.append(point)
    return np.array(intersection_points), np.array(source_points_that_hit) 