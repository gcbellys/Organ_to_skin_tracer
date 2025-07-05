# Organ-to-Skin Tracer

一个专业的器官到皮肤射线追踪项目，用于计算从器官特征点到皮肤表面的射线交点。

## 🎯 项目概述

本项目实现了基于人体解剖学的球面坐标系射线追踪算法，主要用于医学影像分析中的器官-皮肤射线追踪研究。通过定义倾斜角(α)和方位角(θ)两个参数，可以精确控制射线的入射方向，实现系统性的射线追踪分析。

## 📁 项目结构

```
Organ-to-Skin-Tracer/
├── 📁 data/                    # 输入数据目录
│   ├── skin.obj               # 皮肤模型文件
│   ├── thyroid.obj            # 甲状腺模型文件
│   └── skin.mtl               # 材质文件
├── 📁 src/                    # 核心源代码
│   ├── config.py              # 配置管理
│   ├── main.py                # 主程序入口
│   ├── ray_tracing.py         # 射线追踪核心算法
│   ├── geometry_utils.py      # 几何计算工具
│   ├── data_loader.py         # 数据加载模块
│   ├── io_utils.py            # 文件IO工具
│   └── extract_key_points.py  # 特征点提取
├── 📁 data_process/           # 数据预处理模块
│   ├── process_all_data.py    # 一键数据处理
│   ├── preprocess_obj_with_params.py  # 皮肤模型预处理
│   └── apply_transform_to_thyroid.py  # 甲状腺点云对齐
├── 📁 output/                 # 输出结果目录
│   ├── preprocessed/          # 预处理结果
│   └── results/               # 实验结果
├── run_complete_workflow.py   # 一键式完整工作流程
├── requirements.txt           # Python依赖
├── environment.yml            # Conda环境配置
├── README.md                  # 项目说明
└── GUIDE.md                   # 坐标系详细指南
```

## 🚀 快速开始

### 环境设置

#### 方法一：使用Conda（推荐）
```bash
# 自动设置环境
conda env create -f environment.yml
conda activate organ-skin-tracer
```

#### 方法二：使用pip
```bash
pip install -r requirements.txt
```

### 一键运行完整流程
```bash
python run_complete_workflow.py
```

这将自动执行：
1. 数据预处理和对齐
2. 甲状腺特征点提取
3. 射线追踪实验
4. 结果保存和展示

## 📖 详细使用方法

### 1. 数据准备

将您的模型文件放置在 `data/` 目录下：
- `skin.obj` - 皮肤模型
- `thyroid.obj` - 甲状腺模型

### 2. 分步执行

#### 数据处理
```bash
cd data_process
python process_all_data.py
```

#### 特征点提取
```bash
cd src
python extract_key_points.py ../data/thyroid.obj ../output/preprocessed/thyroid_points.obj
```

#### 射线追踪实验
```bash
# 运行默认参数实验
python main.py

# 或使用射线追踪模块（支持自定义参数）
python ray_tracing.py ../output/preprocessed/thyroid_points.obj ../data/skin.obj 30 0 ../output/results
```

### 3. 自定义参数实验

```bash
python src/ray_tracing.py <甲状腺关键点文件> <皮肤模型文件> <倾斜角> <方位角> <输出目录>
```

示例：
```bash
# 从前方30度倾斜角，0度方位角进行射线追踪
python src/ray_tracing.py output/preprocessed/thyroid_points.obj data/skin.obj 30 0 output/results

# 从左侧45度倾斜角，90度方位角进行射线追踪
python src/ray_tracing.py output/preprocessed/thyroid_points.obj data/skin.obj 45 90 output/results
```

## 🧮 坐标系说明

项目使用基于人体解剖学的球面坐标系来定义射线方向：

### 角度参数
- **倾斜角 α (alpha)**：0°-180°
  - 0°：从正前方垂直入射
  - 45°：从前方偏离45度
  - 90°：与正前方垂直（如从上方、左方等）
- **方位角 θ (theta)**：0°-360°
  - 0°：朝上方倾斜
  - 90°：朝左侧倾斜
  - 180°：朝下方倾斜
  - 270°：朝右侧倾斜

### 常见角度组合示例

| α (倾斜角) | θ (方位角) | 射线方向描述 |
|-----------|-----------|-------------|
| 0°        | 任意      | 从正前方垂直入射 |
| 45°       | 0°        | 从前方偏上45度入射 |
| 45°       | 90°       | 从前方偏左45度入射 |
| 45°       | 180°      | 从前方偏下45度入射 |
| 45°       | 270°      | 从前方偏右45度入射 |
| 90°       | 0°        | 从正上方垂直入射 |
| 90°       | 90°       | 从正左方垂直入射 |
| 90°       | 180°      | 从正下方垂直入射 |
| 90°       | 270°      | 从正右方垂直入射 |

详细说明请参考 [GUIDE.md](GUIDE.md)。

## 📊 输出格式

### 实验结果目录结构
```
output/results/
├── alpha_30_theta_0/          # 按角度命名的实验目录
│   ├── intersection_points.ply # 射线交点坐标（PLY格式）
│   ├── metadata.json          # 实验元数据
│   ├── ray_trace_result.json  # 详细追踪结果
│   ├── intersections.obj      # 交点坐标（OBJ格式）
│   └── ray_pairs.obj          # 源点-交点对
└── alpha_45_theta_90/
    └── ...
```

### 元数据格式
```json
{
    "timestamp": "2024-01-01T12:00:00",
    "parameters": {
        "alpha_deg": 30.0,
        "theta_deg": 0.0
    },
    "input_files": {
        "skin": "skin.obj",
        "thyroid_points_source": "thyroid.obj"
    },
    "results_summary": {
        "total_source_points": 7,
        "rays_that_hit": 5
    },
    "source_to_intersection_map": [
        {
            "source_coord": [x1, y1, z1],
            "intersection_coord": [x2, y2, z2]
        }
    ]
}
```

## 🔧 核心模块说明

### config.py
- 集中管理所有路径和默认参数
- 使用 pathlib 提供跨平台路径操作

### geometry_utils.py
- `get_direction_from_angles()`：角度到方向向量转换
- `transform_scene()`：场景坐标系变换
- `calculate_intersections()`：射线追踪计算

### ray_tracing.py
- 独立的射线追踪模块
- 支持命令行参数
- 详细的交点和距离计算

### data_loader.py
- 智能数据加载（优先使用处理后的模型）
- 数据健全性检查

### io_utils.py
- 保存实验结果为PLY格式
- 保存实验元数据为JSON格式

## 🎯 项目特色

- **解剖学导向**：基于人体解剖学的坐标系设计
- **模块化设计**：高内聚低耦合，易于维护和扩展
- **实验可追溯**：每次实验都有完整的元数据记录
- **参数化实验**：支持批量运行不同参数组合
- **跨平台兼容**：使用 pathlib 确保跨平台兼容性
- **一键式流程**：提供完整的工作流程脚本

## 📋 依赖要求

- Python 3.7+
- trimesh
- numpy
- pyvista
- pathlib

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

---

**注意**：本项目主要用于医学影像分析研究，请确保遵守相关法律法规和伦理要求。 