from pathlib import Path

# --- Base Directories ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
PROCESSED_DATA_DIR = OUTPUT_DIR / "processed_data"
RESULTS_DIR = OUTPUT_DIR / "results"

def get_paths(organ_name):
    """
    Generates a standardized dictionary of paths for a given organ.
    This is the central function for all path management.
    """
    paths = {
        # Raw data
        "raw_dir": DATA_DIR / organ_name,
        "raw_model": DATA_DIR / organ_name / f"{organ_name}_raw.obj",
        
        # Processed data
        "processed_dir": PROCESSED_DATA_DIR / organ_name,
        "processed_model": PROCESSED_DATA_DIR / organ_name / f"{organ_name}_processed.obj",
    }
    
    # --- Special cases for organs with keypoints or unique files ---
    
    if organ_name == "skin":
        paths["transform_params"] = PROCESSED_DATA_DIR / organ_name / "transform_params.json"

    if organ_name == "heart":
        paths["raw_keypoints_json"] = DATA_DIR / organ_name / "keypoints_original.json"
        paths["raw_keypoints_obj"] = DATA_DIR / organ_name / "keypoints_raw.obj"
        paths["processed_keypoints"] = PROCESSED_DATA_DIR / organ_name / "keypoints_processed.obj"
        paths["keypoints_mapping"] = PROCESSED_DATA_DIR / organ_name / "keypoints_mapping.json"
        
    if organ_name == "thyroid":
        # Assuming keypoints are extracted during processing, not raw data
        paths["processed_keypoints"] = PROCESSED_DATA_DIR / organ_name / "keypoints_processed.obj"

    return paths

# --- Global Access to Skin Transform Parameters ---
# This is a critical path used by all organ processing scripts.
SKIN_TRANSFORM_PARAMS_PATH = get_paths("skin")["transform_params"]

# --- Default Ray-Tracing Parameters ---
DEFAULT_ALPHA_DEG = 30.0
DEFAULT_THETA_DEG = 0.0 