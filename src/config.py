from pathlib import Path

# --- 路径定义 ---
# Pathlib 提供了面向对象的、跨平台的路径操作
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# 预处理文件的路径
PREPROCESSED_DIR = OUTPUT_DIR / "preprocessed"
THYROID_POINTS_PATH = PREPROCESSED_DIR / "thyroid_processed.ply"
SKIN_PROCESSED_PATH = PREPROCESSED_DIR / "skin_processed_withparams.obj"
TRANSFORM_PARAMS_PATH = PREPROCESSED_DIR / "skin_processed_withparams_transform_params.json"

# 最终结果的根路径
RESULTS_DIR = OUTPUT_DIR / "results"

# --- 默认参数定义 ---
DEFAULT_ALPHA_DEG = 30.0
DEFAULT_THETA_DEG = 0.0 