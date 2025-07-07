# Organ-to-Skin Tracer

一个专业的、可扩展的器官到皮肤射线追踪项目，用于计算从体内器官特征点到皮肤表面的射线交点。

## 🎯 项目概述

本项目实现了一套完整的、基于人体解剖学的3D模型处理和射线追踪工作流程。其核心优势在于清晰的文件结构和标准化的处理脚本，可以轻松扩展以支持多种器官。通过定义倾斜角(α)和方位角(θ)两个参数，可以精确控制射线的入射方向，实现系统性的射线追踪分析。

## 📁 项目结构

项目采用以器官为中心的模块化目录结构，清晰且易于扩展。

```
Organ-to-Skin-Tracer/
├── 📁 data/                    # 原始数据输入目录
│   ├── 📁 skin/
│   │   └── skin_raw.obj
│   ├── 📁 heart/
│   │   ├── heart_raw.obj
│   │   └── keypoints_original.json
│   ├── 📁 liver/
│   │   └── liver_raw.obj
│   ├── 📁 lung/
│   │   └── lung_raw.obj
│   ├── 📁 thyroid/
│   │   └── thyroid_raw.obj
│   ├── 📁 pancreas/           # (空) 为新器官预留
│   └── 📁 kidney/             # (空) 为新器官预留
│
├── 📁 output/                 # 所有生成文件的输出目录
│   ├── 📁 processed_data/     # 标准化处理后的模型
│   │   ├── 📁 skin/
│   │   │   ├── skin_processed.obj
│   │   │   └── transform_params.json
│   │   └── 📁 heart/
│   │       ├── heart_processed.obj
│   │       └── keypoints_processed.obj
│   │
│   └── 📁 results/            # 射线追踪实验结果
│       └── 📁 heart_to_skin/
│           └── 📁 alpha_0.0_theta_0.0/
│               ├── intersections.obj
│               └── ray_trace_result.json
│
├── 📁 src/                    # 核心源代码
│   ├── config.py             # 路径和参数配置中心
│   ├── ray_tracing.py        # 射线追踪主脚本
│   └── ...
│
├── 📁 data_process/           # 数据预处理模块
│   └── process.py            # 统一的模型处理脚本
│
├── 📁 docs/                   # 项目文档
│   └── coordinate_correction_notes.md
│
├── requirements.txt          # Python依赖
└── README.md                 # 本文件
```

## 🚀 工作流程

项目的标准工作流程分为两步：**数据处理** 和 **射线追踪**。

### 步骤 1: 数据处理

所有模型在使用前都必须经过标准化处理，以确保它们在同一个坐标空间内。我们使用统一的 `data_process/process.py` 脚本来完成此操作。

**1.1. 处理皮肤模型 (仅需运行一次)**

皮肤是所有对齐的基准。此命令会生成后续步骤必需的变换参数文件。
```bash
python3 data_process/process.py skin
```

**1.2. 处理所有其他器官**

您可以一次性处理所有可用的器官：
```bash
python3 data_process/process.py --all
```
或者，单独处理一个特定的器官：
```bash
python3 data_process/process.py heart
python3 data_process/process.py liver
```

### 步骤 2: 射线追踪实验

数据处理完成后，您可以运行射线追踪实验。

```bash
python3 src/ray_tracing.py --source <源器官> --target <目标器官> --alpha <倾斜角> --theta <方位角>
```

**示例:**

计算从心脏关键点到皮肤正前方的投影：
```bash
# --source 指定了射线的起点器官
# --target 指定了射线的目标模型 (默认为 skin)
# --alpha 0 代表从正前方入射
python3 src/ray_tracing.py --source heart --target skin --alpha 0 --theta 0
```

结果将保存在 `output/results/heart_to_skin/alpha_0.0_theta_0.0/` 目录下。

## 🧮 坐标系说明

项目使用基于人体解剖学的球面坐标系来定义射线方向：

- **倾斜角 α (alpha)**：0°-180°
  - `0°`: 从正前方垂直入射 (Z+ 方向)
  - `90°`: 从侧面、上方或下方入射
- **方位角 θ (theta)**：0°-360°
  - `0°`: 朝上方倾斜 (Y+ 方向)
  - `90°`: 朝左侧倾斜 (X- 方向)
  - `180°`: 朝下方倾斜 (Y- 方向)
  - `270°`: 朝右侧倾斜 (X+ 方向)

## 🔧 核心模块说明

### `src/config.py`
项目的路径管理中心。通过 `get_paths(organ_name)` 函数，动态生成所有与特定器官相关的文件路径，实现了代码与文件结构的解耦。

### `data_process/process.py`
统一的、现代化的数据处理脚本。取代了所有旧的零散脚本。
- **功能**:
  - `python3 process.py skin`: 计算并保存皮肤模型的变换参数。
  - `python3 process.py <organ_name>`: 加载皮肤的变换参数，并将其应用到指定器官上。
  - `python3 process.py --all`: 自动发现并处理所有器官。

### `src/ray_tracing.py`
核心射线追踪脚本。
- **特点**:
  - **接口简洁**: 通过器官名称 (`--source`, `--target`)而非繁琐的文件路径来指定输入。
  - **智能路径**: 内部使用 `config.py` 自动解析所需文件（如处理后的模型、关键点、名称映射文件等）。
  - **结果丰富**: 输出的JSON文件包含源点/交点坐标、解剖学名称、距离和面ID。

## 🤝 如何添加新器官

以添加"胰腺 (pancreas)"为例：

1.  **添加原始数据**: 在 `data/pancreas/` 目录下放入 `pancreas_raw.obj` 文件。
2.  **运行处理脚本**:
    ```bash
    python3 data_process/process.py pancreas
    ```
3.  **运行射线追踪**: (假设胰腺的关键点是其本身)
    ```bash
    python3 src/ray_tracing.py --source pancreas --alpha 0 --theta 0
    ```

项目结构的设计使得添加新器官无需修改任何现有代码。

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