import unreal
import csv
import os
import tkinter as tk
from tkinter import filedialog


def import_meshes_by_csv():
    """
    根据 CSV 文件导入模型到 UE 场景中
    使用文件对话框选择 CSV 文件所在文件夹
    
    Returns:
        list: 成功导入的 Actor 列表
    """
    
    # 使用文件对话框选择文件夹
    try:
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        root.attributes('-topmost', True)  # 对话框置顶
        
        # 打开文件夹选择对话框
        import_dir = filedialog.askdirectory(
            title="选择包含 CSV 和 FBX 文件的文件夹"
        )
        
        root.destroy()
        
        if not import_dir:
            unreal.log("[ImportMesh] 文件夹选择已取消")
            return []
        
        unreal.log(f"[ImportMesh] 选择的文件夹: {import_dir}")
        
    except Exception as e:
        unreal.log_error(f"[ImportMesh] 文件对话框错误: {str(e)}")
        return []
    
    # 在文件夹中查找 CSV 文件
    csv_files = []
    for file in os.listdir(import_dir):
        if file.lower().endswith('.csv'):
            csv_files.append(file)
    
    if not csv_files:
        unreal.log_error(f"[ImportMesh] 在文件夹中未找到 CSV 文件: {import_dir}")
        return []
    
    # 如果有多个 CSV 文件，使用第一个
    csv_file = csv_files[0]
    
    # 构建 CSV 文件路径
    csv_path = os.path.join(import_dir, csv_file)
    
    unreal.log(f"[ImportMesh] 找到 CSV 文件: {csv_file}")
    unreal.log(f"[ImportMesh] 开始从 CSV 文件导入: {csv_path}")
    
    # 读取 CSV 文件
    actors_created = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # 检查 CSV 文件格式
            expected_columns = ['actorName', 'meshName', 'locationx', 'locationy', 'locationz', 
                               'rotationx', 'rotationy', 'rotationz', 'scalex', 'scaley', 'scalez']
            
            if csv_reader.fieldnames != expected_columns:
                unreal.log_warning(f"[ImportMesh] CSV 文件列名不匹配。期望: {expected_columns}，实际: {csv_reader.fieldnames}")
            
            # 遍历 CSV 中的每一行
            for row_idx, row in enumerate(csv_reader):
                try:
                    # 解析 CSV 数据
                    actor_name = row['actorName']
                    mesh_name = row['meshName']
                    
                    # 解析位置（注意：导出时除以了100，导入时需要乘以100）
                    location_x = float(row['locationx']) * 100
                    location_y = float(row['locationy']) * 100
                    location_z = float(row['locationz']) * 100
                    
                    # 解析旋转
                    rotation_x = float(row['rotationx'])  # roll
                    rotation_y = float(row['rotationy'])  # pitch
                    rotation_z = float(row['rotationz'])  # yaw
                    
                    # 解析缩放
                    scale_x = float(row['scalex'])
                    scale_y = float(row['scaley'])
                    scale_z = float(row['scalez'])
                    
                    # 查找或加载 FBX 文件
                    fbx_path = os.path.join(import_dir, f"{mesh_name}.fbx")
                    
                    # 首先检查是否已存在对应的静态网格体资产
                    # 尝试在项目内容中查找
                    mesh_asset = None
                    
                    # 构建可能的资产路径
                    possible_paths = [
                        f"/Game/Imported/{mesh_name}",
                        f"/Game/ImportedMeshes/{mesh_name}",
                        f"/Game/{mesh_name}"
                    ]
                    
                    for asset_path in possible_paths:
                        asset_data = unreal.EditorAssetLibrary.find_asset_data(asset_path)
                        if asset_data:
                            mesh_asset = unreal.EditorAssetLibrary.load_asset(asset_path)
                            break
                    
                    # 如果没找到，尝试从 FBX 文件导入
                    if not mesh_asset and os.path.exists(fbx_path):
                        mesh_asset = import_fbx_as_static_mesh(fbx_path, mesh_name)
                    
                    # 如果 FBX 导入失败或不存在，尝试在项目中搜索同名网格体
                    if not mesh_asset:
                        mesh_asset = find_static_mesh_by_name(mesh_name)
                    
                    if not mesh_asset:
                        unreal.log_warning(f"[ImportMesh] 第 {row_idx+1} 行: 无法找到或导入网格体 '{mesh_name}'，跳过此 Actor")
                        continue
                    
                    # 创建 Actor
                    actor = create_static_mesh_actor(
                        mesh_asset=mesh_asset,
                        actor_name=actor_name,
                        location=(location_x, location_y, location_z),
                        rotation=(rotation_x, rotation_y, rotation_z),
                        scale=(scale_x, scale_y, scale_z)
                    )
                    
                    if actor:
                        actors_created.append(actor)
                        unreal.log(f"[ImportMesh] 成功创建 Actor: {actor_name}")
                    else:
                        unreal.log_warning(f"[ImportMesh] 第 {row_idx+1} 行: 创建 Actor '{actor_name}' 失败")
                        
                except Exception as e:
                    unreal.log_error(f"[ImportMesh] 第 {row_idx+1} 行处理失败: {str(e)}")
                    continue
        
        unreal.log(f"[ImportMesh] 导入完成，成功创建 {len(actors_created)} 个 Actor")
        return actors_created
        
    except Exception as e:
        unreal.log_error(f"[ImportMesh] 读取 CSV 文件失败: {str(e)}")
        return []


def import_fbx_as_static_mesh(fbx_path, mesh_name):
    """
    导入 FBX 文件为静态网格体资产
    
    Args:
        fbx_path (str): FBX 文件路径
        mesh_name (str): 网格体名称
    
    Returns:
        unreal.StaticMesh: 导入的静态网格体资产，失败返回 None
    """
    try:
        unreal.log(f"[ImportMesh] 正在导入 FBX 文件: {fbx_path}")
        
        # 创建导入任务
        import_task = unreal.AssetImportTask()
        import_task.filename = fbx_path
        import_task.destination_path = "/Game/Imported/"  # 导入到项目中的路径
        import_task.destination_name = mesh_name
        import_task.replace_existing = True
        import_task.automated = True
        import_task.save = True
        
        # 配置导入选项
        import_options = unreal.FbxImportUI()
        import_options.import_mesh = True
        import_options.import_as_skeletal = False
        import_options.static_mesh_import_data = unreal.FbxStaticMeshImportData()
        import_options.static_mesh_import_data.import_uniform_scale = 1.0
        import_options.static_mesh_import_data.import_translation = unreal.Vector(0, 0, 0)
        import_options.static_mesh_import_data.import_rotation = unreal.Rotator(0, 0, 0)
        
        import_task.options = import_options
        
        # 执行导入
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])
        
        # 获取导入的资产
        imported_assets = import_task.imported_object_paths
        if imported_assets and len(imported_assets) > 0:
            asset_path = imported_assets[0]
            return unreal.EditorAssetLibrary.load_asset(asset_path)
        else:
            unreal.log_warning(f"[ImportMesh] FBX 导入未返回资产: {fbx_path}")
            return None
            
    except Exception as e:
        unreal.log_error(f"[ImportMesh] 导入 FBX 文件失败 {fbx_path}: {str(e)}")
        return None


def create_static_mesh_actor(mesh_asset, actor_name, location, rotation, scale):
    """
    创建静态网格体 Actor
    
    Args:
        mesh_asset (unreal.StaticMesh): 静态网格体资产
        actor_name (str): Actor 名称
        location (tuple): (x, y, z) 位置
        rotation (tuple): (roll, pitch, yaw) 旋转
        scale (tuple): (x, y, z) 缩放
    
    Returns:
        unreal.Actor: 创建的 Actor，失败返回 None
    """
    try:
        # 获取当前编辑器世界
        world = unreal.EditorLevelLibrary.get_editor_world()
        
        if not world:
            unreal.log_error("[ImportMesh] 无法获取编辑器世界")
            return None
        
        # 创建静态网格体 Actor
        actor_class = unreal.StaticMeshActor.static_class()
        actor_location = unreal.Vector(location[0], location[1], location[2])
        actor_rotation = unreal.Rotator(rotation[0], rotation[1], rotation[2])
        
        # 使用更可靠的 Actor 创建方法
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class,
            actor_location,
            actor_rotation
        )
        
        if not actor:
            unreal.log_error(f"[ImportMesh] 创建 Actor '{actor_name}' 失败")
            return None
        
        # 设置 Actor 名称
        actor.set_actor_label(actor_name)
        
        # 获取静态网格体组件并设置网格体
        static_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
        if static_mesh_component:
            static_mesh_component.set_static_mesh(mesh_asset)
        else:
            unreal.log_warning(f"[ImportMesh] Actor '{actor_name}' 没有静态网格体组件")
            # 尝试添加组件
            static_mesh_component = unreal.StaticMeshComponent()
            actor.add_instance_component(static_mesh_component)
            static_mesh_component.set_static_mesh(mesh_asset)
            static_mesh_component.register_component()
        
        # 设置缩放
        actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))
        
        # 确保 Actor 被正确注册
        actor.register_all_components()
        
        return actor
        
    except Exception as e:
        unreal.log_error(f"[ImportMesh] 创建 Actor '{actor_name}' 失败: {str(e)}")
        return None


def find_static_mesh_by_name(mesh_name):
    """
    在项目中通过名称查找静态网格体
    
    Args:
        mesh_name (str): 网格体名称
    
    Returns:
        unreal.StaticMesh: 找到的静态网格体，失败返回 None
    """
    try:
        # 使用资产注册表搜索
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        
        # 搜索所有静态网格体
        asset_data_list = asset_registry.get_assets_by_class("StaticMesh", True)
        
        for asset_data in asset_data_list:
            if asset_data.asset_name == mesh_name:
                return unreal.EditorAssetLibrary.load_asset(asset_data.object_path)
        
        # 如果没有精确匹配，尝试模糊搜索
        for asset_data in asset_data_list:
            if mesh_name.lower() in asset_data.asset_name.lower():
                unreal.log(f"[ImportMesh] 找到近似匹配的网格体: {asset_data.asset_name}")
                return unreal.EditorAssetLibrary.load_asset(asset_data.object_path)
        
        return None
        
    except Exception as e:
        unreal.log_error(f"[ImportMesh] 搜索网格体 '{mesh_name}' 失败: {str(e)}")
        return None


def get_imported_assets_count():
    """
    获取已导入的资产数量（用于蓝图调试）
    
    Returns:
        int: 已导入的资产数量
    """
    # 这里可以添加统计逻辑，暂时返回0
    return 0


# 测试函数
def test_import():
    """
    测试导入功能
    """
    unreal.log("[ImportMesh] 开始测试导入...")
    result = import_meshes_by_csv()
    unreal.log(f"[ImportMesh] 测试导入完成，创建了 {len(result)} 个 Actor")
    return result


# 主执行块
if __name__ == "__main__":
    # 当脚本直接运行时，执行测试
    test_import()