# src/data_loader.py
import pyvista as pv
from config import DATA_DIR, THYROID_POINTS_PATH, SKIN_PROCESSED_PATH

def load_data():
    """加载所有需要的模型文件。"""
    # 优先使用处理后的皮肤模型，如果不存在则使用原始模型
    try:
        skin_mesh = pv.read(SKIN_PROCESSED_PATH)
        print(f"使用处理后的皮肤模型: {SKIN_PROCESSED_PATH}")
    except FileNotFoundError:
        skin_mesh = pv.read(DATA_DIR / "skin.obj")
        print(f"使用原始皮肤模型: {DATA_DIR / 'skin.obj'}")
    
    thyroid_points = pv.read(THYROID_POINTS_PATH)
    return skin_mesh, thyroid_points

def validate_setup(skin_mesh, thyroid_points):
    """健全性检查，确保所有点在模型内部。"""
    selection = skin_mesh.select_enclosed_points(thyroid_points.points, tolerance=0.0)
    if selection['SelectedPoints'].sum() < thyroid_points.n_points:
        print("警告: 部分或全部特征点位于皮肤模型之外！")
        return False
    print("健全性检查通过：所有特征点均在皮肤模型内部。")
    return True 