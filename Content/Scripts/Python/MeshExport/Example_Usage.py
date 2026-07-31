"""
ImportMeshByCSV 使用示例
这个文件展示了如何在 Unreal Engine 中调用导入工具
"""

import unreal
import ImportMeshByCSV


def create_import_button_in_editor():
    """
    在编辑器中创建导入按钮的示例代码
    通常这会在 Editor Utility Widget 中实现
    """
    unreal.log("=== ImportMeshByCSV 使用示例 ===")
    
    # 方法1：直接调用导入函数
    unreal.log("方法1：直接调用 import_meshes_by_csv()")
    # 这将弹出文件夹选择对话框
    # actors = ImportMeshByCSV.import_meshes_by_csv()
    
    # 方法2：使用测试函数
    unreal.log("方法2：使用测试函数 test_import()")
    # 这也将弹出文件夹选择对话框
    # result = ImportMeshByCSV.test_import()
    
    # 方法3：在 Editor Utility Widget 中调用
    unreal.log("""
方法3：在 Editor Utility Widget 中调用
    
步骤：
1. 在 Content Browser 中右键 -> Blueprints -> Editor Utility Widget
2. 命名为 "MeshImporterWidget"
3. 打开 Widget，添加一个 Button
4. 在 Button 的 On Clicked 事件中添加：
   - Execute Python Script 节点
   - 在 Script Source 中输入：
     import ImportMeshByCSV
     ImportMeshByCSV.import_meshes_by_csv()
5. 保存并运行 Widget
    """)
    
    unreal.log("=== 示例结束 ===")


# 如果直接运行这个脚本，显示使用说明
if __name__ == "__main__":
    create_import_button_in_editor()