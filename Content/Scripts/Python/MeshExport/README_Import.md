# UE 场景模型导入工具

## 概述

`ImportMeshByCSV.py` 是一个与 `ExplortSelectedMesh.py` 配套的导入工具，用于将导出的场景模型数据重新导入到 Unreal Engine 场景中。

## 功能特性

1. **CSV 数据解析**：读取由导出工具生成的 CSV 文件
2. **模型导入**：自动导入关联的 FBX 模型文件
3. **场景还原**：根据 CSV 中的数据精确还原 Actor 的位置、旋转和缩放
4. **错误处理**：完善的错误处理和日志记录

## 文件格式

CSV 文件包含以下列：
- `actorName`: Actor 名称
- `meshName`: 网格体名称（对应 .fbx 文件名）
- `locationx`, `locationy`, `locationz`: 位置坐标（导出时除以100，导入时乘以100）
- `rotationx`, `rotationy`, `rotationz`: 旋转角度（roll, pitch, yaw）
- `scalex`, `scaley`, `scalez`: 缩放比例

## 使用方法

### 1. 在 Python 脚本中调用

```python
import ImportMeshByCSV

# 导入场景 - 会自动弹出文件夹选择对话框
actors = ImportMeshByCSV.import_meshes_by_csv()
```

### 2. 在 Unreal Engine 蓝图/编辑器工具中调用

1. 创建一个 Editor Utility Widget
2. 添加一个执行按钮，连接到 Python 脚本：
   ```python
   import ImportMeshByCSV
   ImportMeshByCSV.import_meshes_by_csv()
   ```

### 3. 操作流程

1. 点击导入按钮
2. 弹出文件夹选择对话框
3. 选择包含 CSV 和 FBX 文件的文件夹
4. 工具自动识别文件夹中的 CSV 文件
5. 开始导入过程

## 导入流程

1. **读取 CSV**：解析 CSV 文件中的每一行数据
2. **查找/导入模型**：
   - 首先在项目内容中查找同名静态网格体
   - 如果不存在，尝试从同目录下的 .fbx 文件导入
   - 如果 FBX 文件也不存在，在项目中搜索近似名称的网格体
3. **创建 Actor**：根据 CSV 数据创建静态网格体 Actor
4. **设置变换**：应用位置、旋转和缩放

## 错误处理

- 如果 CSV 文件不存在，会记录错误并返回空列表
- 如果某个模型无法加载，会跳过该行并继续处理后续行
- 所有操作都有详细的日志记录，可在 Unreal 输出日志中查看

## 示例

假设导出工具生成了以下文件：
```
ExportFolder/
├── PointCloudData.csv
├── Cube.fbx
├── Sphere.fbx
└── Cylinder.fbx
```

导入操作：
1. 调用 `import_meshes_by_csv()` 函数
2. 在弹出的对话框中选择 `ExportFolder` 文件夹
3. 工具自动识别并处理 `PointCloudData.csv` 文件

## 注意事项

1. **单位转换**：位置坐标会在导入时乘以100（导出时除以了100）
2. **资产路径**：导入的 FBX 文件会保存在 `/Game/Imported/` 目录下
3. **名称冲突**：如果 Actor 名称已存在，新创建的 Actor 会自动添加后缀
4. **性能考虑**：大量模型导入时可能会有性能影响，建议分批导入

## 调试

- 使用 `test_import()` 函数进行测试
- 查看 Unreal 输出日志中的 `[ImportMesh]` 前缀日志
- 使用 `get_imported_assets_count()` 获取导入统计（待实现）