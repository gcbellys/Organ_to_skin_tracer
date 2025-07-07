# 坐标系修正备忘录：处理 empties_location.json

本文档记录了将 `data/empties_location.json` 中的原始坐标点，转换为与主模型 `data/skin.obj` 坐标系对齐的 `Heart_keypoints_raw.obj` 文件的完整流程。

当处理来自不同来源（尤其是手动标记）的坐标数据时，很可能会遇到类似问题。

---

### 修正流程

我们对原始数据进行了三步核心操作：

#### 步骤 1: 从 JSON 转换为 OBJ 格式

*   **初始状态**: 原始数据存储在 `empties_location.json` 中，格式为 `{"名称": [x, y, z]}`。
*   **操作**: 编写脚本读取此 JSON 文件，并将每一组 `[x, y, z]` 坐标转换为 OBJ 文件中的一行顶点数据 `v x y z`。
*   **结果**: 生成 `Heart_keypoints_raw.obj` 文件。

#### 步骤 2: 交换 Y 轴与 Z 轴

*   **问题诊断**: 将生成的 `Heart_keypoints_raw.obj` 与 `skin.obj` 对比分析，发现坐标轴定义不匹配。心脏关键点的 Y 坐标（本应代表高度）值很小，而 Z 坐标（本应代表深度）值很大（约130），与 `skin.obj` 的范围 (Y: ~171, Z: ~0) 完全不符。
*   **修正操作**: 我们对 `Heart_keypoints_raw.obj` 进行了处理，将每个顶点的 Y 坐标和 Z 坐标进行了互换。
    *   变换逻辑: `v x y_old z_old` -> `v x z_old y_old`

#### 步骤 3: 反转 Z 轴方向

*   **问题诊断**: 交换坐标轴后，发现 Z 轴（前后方向）的正负定义仍然是相反的。
*   **修正操作**: 我们对上一步生成的文件再次处理，将每个顶点的 Z 坐标值取反。
    *   变换逻辑: `v x y z_old` -> `v x y -z_old`

---

经过以上三个步骤，`Heart_keypoints_raw.obj` 中的坐标数据最终与 `skin.obj` 的坐标系完全对齐，可以用于后续的对齐和射线追踪等操作。 