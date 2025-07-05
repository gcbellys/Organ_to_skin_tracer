# 项目结构说明

## 📁 目录结构

```
Organ-to-Skin-Tracer/
├── 📁 data/                    # 输入数据目录
│   ├── skin.obj               # 皮肤模型文件 (OBJ格式)
│   ├── thyroid.obj            # 甲状腺模型文件 (OBJ格式)
│   └── skin.mtl               # 皮肤模型材质文件
├── 📁 src/                    # 核心源代码目录
│   ├── config.py              # 配置管理模块
│   ├── main.py                # 主程序入口
│   ├── ray_tracing.py         # 射线追踪核心算法
│   ├── geometry_utils.py      # 几何计算工具
│   ├── data_loader.py         # 数据加载模块
│   ├── io_utils.py            # 文件IO工具
│   └── extract_key_points.py  # 特征点提取模块
├── 📁 data_process/           # 数据预处理模块
│   ├── process_all_data.py    # 一键数据处理脚本
│   ├── preprocess_obj_with_params.py  # 皮肤模型预处理
│   └── apply_transform_to_thyroid.py  # 甲状腺点云对齐
├── 📁 output/                 # 输出结果目录
│   ├── preprocessed/          # 预处理结果
│   │   ├── skin_processed_withparams.obj      # 处理后的皮肤模型
│   │   ├── thyroid_processed.obj              # 处理后的甲状腺模型
│   │   ├── thyroid_key_points.obj             # 甲状腺特征点
│   │   └── skin_processed_withparams_transform_params.json  # 变换参数
│   └── results/               # 实验结果
│       ├── alpha_0_theta_0/   # 实验1结果
│       └── alpha_45_theta_90/ # 实验2结果
├── run_complete_workflow.py   # 一键式完整工作流程
├── requirements.txt           # Python依赖列表
├── environment.yml            # Conda环境配置
├── README.md                  # 项目主要说明文档
├── GUIDE.md                   # 坐标系详细指南
└── PROJECT_STRUCTURE.md       # 本文件 - 项目结构说明
```

## 📄 核心文件说明

### 配置文件
- **`requirements.txt`**: Python包依赖列表
- **`environment.yml`**: Conda环境配置文件
- **`src/config.py`**: 项目路径和参数配置

### 主要脚本
- **`run_complete_workflow.py`**: 一键运行完整工作流程
- **`src/main.py`**: 主程序入口，支持批量实验
- **`src/ray_tracing.py`**: 独立的射线追踪模块，支持命令行参数

### 核心模块
- **`src/geometry_utils.py`**: 几何计算核心，包含角度转换和射线追踪算法
- **`src/data_loader.py`**: 数据加载和验证
- **`src/io_utils.py`**: 结果保存和文件IO
- **`src/extract_key_points.py`**: 从甲状腺模型提取7个关键特征点

### 数据预处理
- **`data_process/process_all_data.py`**: 一键处理所有数据
- **`data_process/preprocess_obj_with_params.py`**: 皮肤模型预处理
- **`data_process/apply_transform_to_thyroid.py`**: 甲状腺点云对齐

## 🎯 工作流程

### 1. 数据准备阶段
```
data/
├── skin.obj      # 原始皮肤模型
└── thyroid.obj   # 原始甲状腺模型
```

### 2. 数据预处理阶段
```
output/preprocessed/
├── skin_processed_withparams.obj      # 处理后的皮肤模型
├── thyroid_processed.obj              # 对齐后的甲状腺模型
├── thyroid_key_points.obj             # 提取的特征点
└── skin_processed_withparams_transform_params.json  # 变换参数
```

### 3. 实验执行阶段
```
output/results/
├── alpha_30_theta_0/          # 实验1: α=30°, θ=0°
│   ├── intersection_points.ply # 射线交点
│   ├── metadata.json          # 实验元数据
│   ├── ray_trace_result.json  # 详细结果
│   ├── intersections.obj      # 交点OBJ格式
│   └── ray_pairs.obj          # 源点-交点对
└── alpha_45_theta_90/         # 实验2: α=45°, θ=90°
    └── ...
```

## 🔧 模块依赖关系

```
run_complete_workflow.py
    ├── data_process/process_all_data.py
    ├── src/extract_key_points.py
    └── src/main.py
            ├── src/config.py
            ├── src/data_loader.py
            ├── src/geometry_utils.py
            └── src/io_utils.py

src/ray_tracing.py (独立模块)
    ├── src/config.py
    ├── src/geometry_utils.py
    └── trimesh, numpy (外部依赖)
```

## 📊 输出文件格式

### PLY文件
- 包含射线与皮肤表面的交点坐标
- 支持3D可视化软件查看

### JSON文件
- 实验元数据，包含参数、时间戳、结果统计
- 源点到交点的映射关系

### OBJ文件
- 交点坐标的OBJ格式
- 射线源点和交点的对应关系

## 🚀 快速使用路径

1. **新手用户**: `python run_complete_workflow.py`
2. **自定义实验**: `python src/ray_tracing.py <参数>`
3. **批量实验**: `python src/main.py`
4. **数据处理**: `python data_process/process_all_data.py`
5. **特征点提取**: `python src/extract_key_points.py <参数>` 