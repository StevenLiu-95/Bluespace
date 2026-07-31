import unreal
import os
import csv
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Union, Dict, Tuple, Set

def generate_output_file_path(output_dir, filename, format="csv", use_timestamp=False):
    # 桌面路径
    desktop_path = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )
    
    try:
        if not output_dir:
            unreal.log_error("Invalid Folder Path!!!")
            return

        output_dir = os.path.normpath(output_dir).replace("\\", "/")
        os.makedirs(output_dir, exist_ok=True)
        if not os.path.exists(output_dir):
            unreal.log_warning(f"目录不存在，尝试创建: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
            unreal.log(f"已创建目录: {output_dir}")
        
        if not os.access(output_dir, os.W_OK):
            error_msg = f"没有写入权限: {output_dir}"
            unreal.log_error(error_msg)
            raise PermissionError(error_msg)
            
        timestamp = ""
        if use_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S") + "_"
        
        output_path = os.path.join(output_dir, f"{timestamp}{filename}.{format}")
        return output_path
    
    except PermissionError as e:
        unreal.log_error(f"权限错误: {str(e)}")
        return False

def save_data_to_csv(data, output_path, headers=[], auto_num=False):
    try:
        if os.path.exists(output_path):
            try:
                # 尝试以追加模式打开文件来测试是否可访问
                with open(output_path, 'a') as test_file:
                    pass
            except IOError as e:
                error_msg = f"文件被其他程序锁定: {output_path} - {str(e)}"
                unreal.log_error(error_msg)
                raise
        
        if data:
            # processed_data = []
            # for row in data:
            #     processed_row = []
            #     for item in row:
            #         if isinstance(item, unreal.Name):
            #             processed_row.append(str(item))
            #         elif hasattr(item, '__str__'):
            #             processed_row.append(str(item))
            #         else:
            #             processed_row.append(item)
            #     processed_data.append(processed_row)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if headers:
                    if auto_num:
                        headers.insert(0, "No.")
                    writer.writerow(headers)
                
                # 写入数据并自动添加序号
                for index, row in enumerate(data, 1):  # 从1开始计数
                    if auto_num:
                        if isinstance(row, dict):
                            # 如果是字典，创建新字典并添加序号
                            new_row = {"No.": index}
                            new_row.update(row)
                            # 确保列顺序正确
                            if headers:
                                ordered_row = [new_row.get(header, "") for header in headers]
                            else:
                                ordered_row = list(new_row.values())
                            writer.writerow(ordered_row)
                        else:
                            # 如果是列表，直接在前面添加序号
                            writer.writerow([index] + list(row))
                    else:
                        if isinstance(row, dict) and headers:
                            filtered_row = [row.get(header, "") for header in headers]
                            writer.writerow(filtered_row)
                        else:
                            writer.writerow(row)
                            
            unreal.log(f"已保存到: {output_path}")
        else:
            unreal.log_warning(f"data: {data}")
    
    except Exception as e:
        unreal.log_error(f"写入CSV文件失败: {str(e)}")
        return False



def filter_duplicates_by_column(data, column_identifier):
    """
    通用重复项筛选器，支持多种数据类型
    参数:
    - data: 可以是字典列表、字符串列表、或其他可迭代对象
    - column_identifier: 根据数据类型自动适配
    """
    # 检测数据类型
    if not data:
        unreal.log_warning("输入数据为空")
        return None
    
    first_item = data[0]
    
    if isinstance(first_item, dict):
        # 字典列表 - 支持列名和列索引
        unreal.log("检测到字典列表数据")
        duplicates = _filter_dict_duplicates(data, column_identifier)
    
    elif isinstance(first_item, (list, tuple)):
        # 列表的列表 - 支持列索引
        unreal.log("检测到列表的列表数据")
        duplicates = _filter_list_duplicates(data, column_identifier)
    
    else:
        unreal.log_error(f"不支持的数据类型: {type(first_item)}")
        return None
    
    unreal.log(f"找到 {len(duplicates)} 个重复项")
    return duplicates
    
def _filter_dict_duplicates(data, column_identifier):
    """处理字典列表数据"""
    first_item = data[0]
    if isinstance(column_identifier, str):
        column_key = column_identifier
    elif isinstance(column_identifier, int):
        column_key = list(first_item.keys())[column_identifier]
    else:
        unreal.log_error("不支持的列标识符类型")
        return []
    
    # 手动查找重复项
    value_count = defaultdict(list)
    for item in data:
        value = item.get(column_key)
        value_count[value].append(item)
    
    # 返回有重复的值
    duplicates = []
    for value, items in value_count.items():
        if len(items) > 1:
            duplicates.extend(items)
    
    return duplicates

def _filter_list_duplicates(data, column_identifier):
    """处理列表的列表数据"""
    if not isinstance(column_identifier, int):
        unreal.log_error("列表数据需要整数列索引")
        return []
    
    # 手动查找重复项
    value_count = defaultdict(list)
    for item in data:
        if column_identifier < len(item):
            value = item[column_identifier]
            value_count[value].append(item)
    
    # 返回有重复的值
    duplicates = []
    for value, items in value_count.items():
        if len(items) > 1:
            duplicates.extend(items)
    
    return duplicates



def get_mapping_by_csv(csv_file_path, ref_index, value_index):
    if not csv_file_path:
        return None
    
    # 读取CSV文件并建立映射
    new_mapping = {}
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= (ref_index + 1):
                ref = row[ref_index].strip()
                value = row[value_index].strip()
                new_mapping[ref] = value
    unreal.log(f"从CSV加载了 {len(new_mapping)} 个映射")
    return new_mapping



def get_current_level_name():
    # # Get the LevelEditorSubsystem
    # level_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

    # # Get the current level object
    # current_level = level_editor_subsystem.get_current_level()

    # # Get the full package name (e.g., /Game/Maps/MyLevelName)
    # level_package_name = current_level.get_package().get_name()
    # level_name = level_package_name.split("/")[-1]

    world = unreal.EditorLevelLibrary.get_editor_world()
    if world:
        # Get the name of the persistent level
        level_name = world.get_name()
    # unreal.log(f"level_name: {level_name}")
    return level_name

def get_project_name():
    # project_path = unreal.Paths.get_project_file_path()
    # unreal.log(f"project_path: {project_path}")
    project_dir_path = unreal.Paths.project_dir()
    project_name = os.path.basename(os.path.normpath(project_dir_path))
    # unreal.log(f"project_name = {project_name}")
    return project_name

def get_system_path(unreal_path):
    unreal_path = str(unreal_path)
    if not unreal_path.startswith("/Game/"):
        print(f"<{unreal_path}> is not a valid unreal path")
        return ""
    content_dir = unreal.Paths.project_content_dir()
    # file_path = unreal_path.replace('/Game/','')
    # file_path = content_dir + file_path
    # file_path = file_path.replace('/','\\')
    file_path = unreal_path.replace("/Game/", content_dir)
    file_path += ".uasset"
    return os.path.abspath(file_path)



def statistic_actor_desc_info(actor_descs):
    data = []
    for actor_desc in actor_descs:
        data.append({
            'label':actor_desc.label,
            'name':actor_desc.name,
            'guid':actor_desc.guid,
            'actor_package':actor_desc.actor_package,
            'actor_path':actor_desc.actor_path,
            'soft_object_path':actor_desc.class_
        })
    return data

def get_landscape_streaming_proxy_info(actor_descs):
    landscape_streaming_proxy_files_name = []
    for actor_desc in actor_descs:
        file_path = get_system_path(actor_desc.actor_package)
        if not os.path.exists(file_path):
            continue
        file_size = os.path.getsize(file_path)
        landscape_streaming_proxy_files_name.append({
            'label':actor_desc.label,
            'path':file_path,
            'size_kb': round(file_size / 1024, 2),
        })
    return landscape_streaming_proxy_files_name


def statistic_level_actors_out_region(actor_descs):
    data = []
    ignore_keywords = [
        "LandscapeRegion_",
        "LandscapeStreamingProxy_",
        # "InstancedFoliageActor_",
    ]
    for actor_desc in actor_descs:
    # for i in range(2000):
    #     actor_desc = actor_descs[i]
        if not actor_desc:
            continue
        actor_label = str(actor_desc.label)
        # bbmax = actor_desc.bounds.max
        # bbmin = actor_desc.bounds.min
        center, dimension = actor_desc.bounds.get_box_center_size()
        # area = dimension.x * dimension.z
        tile_size = 25400
        if dimension.x < tile_size or dimension.z < tile_size:
            continue
        
        bIgnored = False
        for keyword in ignore_keywords:
            if keyword in actor_label:
                bIgnored = True
                break
        if bIgnored:
            continue

        row_data = {
            "ActorLabel": actor_label,
            "Grid": actor_desc.runtime_grid,
            "BoundSize": str(dimension)
        }
        data.append(row_data)
    return data



def statistic_level_actors_assets_reference_info(output_dir):
    # ================= 配置区 =================
    exclude_keywords = ["LandscapeNaniteMesh", "HLOD"]  # 排除关键词
    search_depth = 4  # 控制分组层级（"/" 分隔）
    # ==========================================

    mesh_comp_classes = [
        unreal.StaticMeshComponent,
        unreal.InstancedStaticMeshComponent,
        unreal.HierarchicalInstancedStaticMeshComponent
    ]

    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    mesh_groups = defaultdict(list)   # {分组路径: [(资产名, 资产路径), ...]}
    mesh_counts = Counter()           # {(资产名, 资产路径): 引用次数}

    # 收集并分组
    for actor in actors:
        for comp_cls in mesh_comp_classes:
            comps = actor.get_components_by_class(comp_cls)
            for comp in comps:
                try:
                    mesh_asset = comp.static_mesh
                except Exception:
                    mesh_asset = None
                if mesh_asset:
                    asset_path = mesh_asset.get_path_name()
                    asset_name = mesh_asset.get_name()

                    # 排除关键词
                    if any(k.lower() in asset_path.lower() or k.lower() in asset_name.lower()
                        for k in exclude_keywords):
                        continue

                    # 按搜索深度裁剪路径
                    path_parts = asset_path.split("/")
                    package_path = "/".join(path_parts[:min(search_depth, len(path_parts) - 1)])

                    key = (asset_name, asset_path)
                    if key not in mesh_groups[package_path]:
                        mesh_groups[package_path].append(key)

                    mesh_counts[key] += 1  # 统计引用次数

    data = []
    headers = ["分组路径(资产数量, 总引用次数)", "资产名称", "资产路径", "引用次数"]
    data.append(headers)
    for package_path, assets in sorted(mesh_groups.items()):
        # 计算该分组总引用次数
        total_group_refs = sum(mesh_counts[(name, path)] for name, path in assets)
        group_title = f"{package_path} ({len(assets)} 个资产, 共 {total_group_refs} 次引用)"
        for asset_name, asset_path in sorted(assets):
            count = mesh_counts[(asset_name, asset_path)]
            data.append([group_title, asset_name, asset_path, count])
    
    filename = f"StaticMeshList_Grouped_Depth{search_depth}_WithCount_Summary"
    output_path = generate_output_file_path(output_dir, filename)
    save_data_to_csv(data, output_path)

def get_all_level_actors_staticmesh_components():
    exclude_keywords = ["Landscape", "HLOD"]  # 排除关键词
    mesh_comp_classes = [
        unreal.StaticMeshComponent,
        unreal.InstancedStaticMeshComponent,
        unreal.HierarchicalInstancedStaticMeshComponent
    ]
    target_actor_comps = []
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in actors:
        for comp_cls in mesh_comp_classes:
            comps = actor.get_components_by_class(comp_cls)
            for comp in comps:
                try:
                    mesh_asset = comp.static_mesh
                except Exception:
                    mesh_asset = None
                if mesh_asset:
                    asset_path = mesh_asset.get_path_name()
                    asset_name = mesh_asset.get_name()

                    # 排除关键词
                    if any(k.lower() in asset_path.lower() or k.lower() in asset_name.lower()
                        for k in exclude_keywords):
                        continue
                    target_actor_comps.append([actor,comp])
    return target_actor_comps

def statistic_level_actors_staticmesh_reference_info(target_actor_comps=None):
    data = []
    if not target_actor_comps:
        target_actor_comps = get_all_level_actors_staticmesh_components()
    for actor, comp in target_actor_comps:
        actor_name = actor.get_actor_label()
        actor_path = actor.get_folder_path()
        mesh_asset = comp.static_mesh
        asset_name = mesh_asset.get_name()
        asset_path = mesh_asset.get_path_name()
        # data.append([actor_name, actor_path, asset_name, asset_path])
        data.append({
            'ActorName': actor_name, 
            'ActorPath': actor_path, 
            'AssetName': asset_name, 
            'AssetPath': asset_path,
        })
    return data

def statistic_level_actors_material_reference_info(target_actor_comps=None):
    data = []
    if not target_actor_comps:
        target_actor_comps = get_all_level_actors_staticmesh_components()
    for actor, comp in target_actor_comps:
        actor_name = actor.get_actor_label()
        actor_path = actor.get_folder_path()
        mesh_asset = comp.static_mesh
        asset_name = mesh_asset.get_name()
        asset_path = mesh_asset.get_path_name()
        material_insts = comp.get_materials()
        if material_insts:
            for i, mat_inst in enumerate(material_insts):
                mat_inst_name = mat_inst.get_name() if mat_inst else "None"
                mat_inst_path = mat_inst.get_package().get_name() if mat_inst else "None"
                master_mat = mat_inst.get_base_material() if mat_inst else None
                master_mat_path = master_mat.get_package().get_name() if master_mat else "None"
                # data.append([actor_name, actor_path, asset_name, asset_path, mat_inst_name, mat_inst_path, master_mat_path])
                data.append({
                    'ActorName': actor_name, 
                    'ActorPath': actor_path, 
                    'AssetName': asset_name, 
                    'AssetPath': asset_path,
                    'MatInstName': mat_inst_name, 
                    "MatInstPath": mat_inst_path, 
                    "MasterMat": master_mat_path
                })
    return data



def statistic_large_files(directory, min_size_kb=500):
    """
    查找指定目录中大于指定大小的文件
    
    参数:
        directory: 要搜索的目录路径
        min_size_kb: 最小文件大小（KB），默认为500KB
    
    返回:
        大于指定大小的文件路径列表
    """
    large_files_data = []
    min_size_bytes = min_size_kb * 1024  # 转换为字节
    
    # 遍历目录中的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = file.split('.')[0]
            try:
                # 获取文件大小
                file_size = os.path.getsize(file_path)
                
                # 检查文件大小是否大于阈值
                if file_size > min_size_bytes:
                    large_files_data.append({
                        'path': file_path,
                        'name': file_name,
                        'size_bytes': file_size,
                        'size_kb': round(file_size / 1024, 2),
                        'size_mb': round(file_size / (1024 * 1024), 2)
                    })
                    
            except (OSError, PermissionError) as e:
                print(f"无法访问文件 {file_path}: {e}")
    
    return large_files_data

def match_info_and_statistic_missing_data(original_file, current_file, column_header):
    if isinstance(column_header, int):
        b_dictionary = False
    elif isinstance(column_header, str):
        b_dictionary = True
    else:
        print(f"The column_header parameter input <{column_header}> is invalid")
        return
    
    current_file_values = set()
    with open(current_file, 'r', encoding='utf-8') as f:
        if b_dictionary:
            reader = csv.DictReader(f)
            if column_header not in reader.fieldnames:
                print(f"错误: {current_file} 中不存在列 '{column_header}'")
                return
        else:
            reader = csv.Reader(f)
        for row in reader:
            if row[column_header]:  # 跳过空值
                current_file_values.add(row[column_header].strip())
    
    missing_data = []
    with open(original_file, 'r', encoding='utf-8') as f:
        if b_dictionary:
            reader = csv.DictReader(f)
            if column_header not in reader.fieldnames:
                print(f"错误: {original_file} 中不存在列 '{column_header}'")
                return
        else:
            reader = csv.Reader(f)
        for row in reader:
            target_value = row[column_header].strip()
            target_value = get_system_path(target_value)
            if target_value and target_value not in current_file_values:
                missing_data.append(row)

    if not missing_data:
            print("所有数据在current_file中都存在")
            return
    else:
        return missing_data

def delete_target_files_by_csv_reference(csv_file_path, column_header=None):
    if not os.path.exists(csv_file_path) or not os.path.isfile(csv_file_path) or not csv_file_path.lower().endswith(".csv"):
        print(f"请检查csv参考文件是否有效: {csv_file_path}")

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        if column_header:
            if column_header not in reader.fieldnames:
                print(f"错误: {csv_file_path} 中不存在列 '{column_header}'")
                return
            reader = csv.DictReader(f)
        else:
            column_header = 0
            reader = csv.reader(f)

        deleted_count = 0
        for row in reader:
            file_path = row[column_header]
            file_path = get_system_path(file_path)
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                    deleted_count += 1
                else:
                    print(f"文件不存在或不是普通文件: {file_path}")
            except Exception as e:
                print(f"删除失败 {file_path}: {e}")
        print(f"成功删除 {deleted_count} 个文件")



def statistic_unique_values(
    data: Union[List[List], List[Dict]], 
    column_identifier: Union[int, str, List[int], List[str]], 
    has_header: bool = False,
    ignore_empty: bool = True,
    case_sensitive: bool = True
) -> List[List]:
    """
    通用的unique值统计函数，支持列表和字典格式
    
    参数:
        data: 数据，可以是二维列表或字典列表
        column_identifier: 列标识符，可以是索引或键名
        has_header: 是否包含表头（仅对列表格式有效）
        ignore_empty: 是否忽略空值
        case_sensitive: 是否区分大小写
    
    返回:
        统计结果，二维列表格式
    """
    if not data:
        return []
    
    # 判断数据类型
    if (not has_header and isinstance(data[0], dict)) or (has_header and isinstance(data[1], dict)):
        if has_header:
            data.pop(0)
        # 字典格式数据
        if isinstance(column_identifier, int) or (isinstance(column_identifier, list) and isinstance(column_identifier[0], int)):
            # 如果是数字索引，需要转换为键名
            if data:
                keys = list(data[0].keys())
                if isinstance(column_identifier, int):
                    if column_identifier < len(keys):
                        column_keys = keys[column_identifier]
                    else:
                        raise ValueError(f"索引 {column_identifier} 超出范围（最大索引：{len(keys)-1}）")
                else:
                    column_keys = [keys[idx] if idx < len(keys) else None for idx in column_identifier]
                    column_keys = [key for key in column_keys if key is not None]
            else:
                column_keys = column_identifier if isinstance(column_identifier, list) else [column_identifier]
        else:
            column_keys = column_identifier
        
        return _statistic_unique_values_dict(
            data, 
            column_keys, 
            has_header=False,  # 字典格式不需要has_header
            ignore_empty=ignore_empty,
            case_sensitive=case_sensitive
        )
    else:
        # 列表格式数据
        return _statistic_unique_values_list(
            data, 
            column_identifier, 
            has_header=has_header,
            ignore_empty=ignore_empty,
            case_sensitive=case_sensitive
        )

def _statistic_unique_values_list(
    data: List[List], 
    column_indices: Union[int, List[int]], 
    has_header: bool = False,
    ignore_empty: bool = True,
    case_sensitive: bool = True
) -> List[List]:
    """
    使用CSV风格统计指定列的unique值数量
    
    参数:
        data: 二维列表数据
        column_indices: 列索引（可以是单个整数或整数列表）
        has_header: 数据是否包含表头行
        ignore_empty: 是否忽略空字符串
        case_sensitive: 是否区分大小写
    
    返回:
        字典，键为列索引，值为unique值统计结果
    """
    if not data:
        return {}
    
    # 如果需要跳过表头
    start_index = 1 if has_header else 0
    
    # 确保column_indices是列表形式
    if isinstance(column_indices, int):
        column_indices = [column_indices]
    
    # 检查数据是否为空
    if start_index >= len(data):
        return {idx: {'total_values': 0, 'unique_count': 0, 'unique_values': {}, 'most_common': []} 
                for idx in column_indices}
    
    # 验证列索引是否有效
    num_columns = len(data[start_index])
    for col_idx in column_indices:
        if col_idx >= num_columns:
            raise ValueError(f"列索引 {col_idx} 超出范围（最大列数：{num_columns-1}）")
    
    result = []
    
    for col_idx in column_indices:
        # 提取指定列的所有值
        column_values = []
        empty_count = 0
        
        for i in range(start_index, len(data)):
            row = data[i]
            # 确保行有足够的列
            if len(row) <= col_idx:
                # 列数不足的行，视为空值
                value = ""
            else:
                value = row[col_idx]
            
            # 处理空值
            if value is None or str(value).strip() == "" or str(value).strip() == "None":
                if ignore_empty:
                    empty_count += 1
                    continue
                else:
                    value = "" if value is None else str(value)
            
            # 处理大小写敏感性
            if not case_sensitive and isinstance(value, str):
                value = value.lower()
            
            column_values.append(value)
        
        # 统计unique值
        value_counter = Counter(column_values)
        total_values = len(column_values)
        
        # 按出现次数降序排序
        sorted_items = sorted(value_counter.items(), key=lambda x: x[1], reverse=True)
        unique_values = dict(sorted_items)

        # result[col_idx] = {
        #     'total_values': total_values+empty_count,
        #     'non_empty_values': total_values,
        #     'empty_values': empty_count,
        #     'unique_count': len(unique_values),
        #     'unique_values': unique_values,
        #     'unique_list': list(unique_values.keys())
        # }
        head_name = data[0][col_idx] if has_header else str(col_idx)

        result.append([head_name,
            f"调用数量总计: {total_values+empty_count},\n"+
            f"有效数量: {total_values},\n"+
            f"None数量: {empty_count},\n"+
            f"引用资产总计: {len(unique_values)}"
        ])

        for value, count in sorted_items:
            result.append(["", value, count])

    return result

def _statistic_unique_values_dict(
    data: List[Dict], 
    column_keys: Union[str, List[str]], 
    has_header: bool = False,
    ignore_empty: bool = True,
    case_sensitive: bool = True
) -> List[List]:
    """
    统计字典列表中指定键的unique值数量
    
    参数:
        data: 字典列表数据
        column_keys: 键名（可以是单个字符串或字符串列表）
        has_header: 是否生成表头行（字典版本通常为False，因为键本身就是表头）
        ignore_empty: 是否忽略空字符串
        case_sensitive: 是否区分大小写
    
    返回:
        二维列表，第一行为表头，后续为统计结果
    """
    if not data:
        return []
    
    # 确保column_keys是列表形式
    if isinstance(column_keys, str):
        column_keys = [column_keys]
    
    # 验证键是否存在
    if data and len(data) > 0:
        first_row = data[0]
        for key in column_keys:
            if key not in first_row:
                print(f"警告：键 '{key}' 不在数据中，可用键：{list(first_row.keys())}")
                # 尝试查找大小写不敏感的匹配
                if not case_sensitive:
                    for actual_key in first_row.keys():
                        if actual_key.lower() == key.lower():
                            print(f"提示：找到大小写不匹配的键 '{actual_key}'")
                            break
    
    result = []
    
    for key in column_keys:
        # 提取指定键的所有值
        column_values = []
        empty_count = 0
        
        for row in data:
            # 安全获取值
            value = row.get(key, "")
            
            # 处理空值
            if value is None or str(value).strip() == "" or str(value).strip() == "None":
                if ignore_empty:
                    empty_count += 1
                    continue
                else:
                    value = "" if value is None else str(value)
            
            # 处理大小写敏感性
            if not case_sensitive and isinstance(value, str):
                value = value.lower()
            
            column_values.append(value)
        
        # 统计unique值
        value_counter = Counter(column_values)
        total_values = len(column_values)
        
        # 按出现次数降序排序
        sorted_items = sorted(value_counter.items(), key=lambda x: x[1], reverse=True)
        unique_values = dict(sorted_items)

        # 添加统计摘要行
        result.append([key,
            f"调用数量总计: {total_values+empty_count},\n"+
            f"有效数量: {total_values},\n"+
            f"None数量: {empty_count},\n"+
            f"引用资产总计: {len(unique_values)}"
        ])

        # 添加详细统计
        for value, count in sorted_items:
            result.append(["", value, count])
    
    return result

