import unreal
import re
import ZEditorAssetFunctionLibrary as AssetLib
import ZEditorLevelFunctionLibrary as ActorLib
import ZEditorStatisticFunctionLibrary as StatisticLib
import tkinter as tk
from tkinter import filedialog

ue_asset_prefix_map = {
    "BP": "Blueprint",
    "SM": "StaticMesh",
    "T": "Texture2D",
    "M": "Material",
    "MI": "MaterialInstanceConstant",
    "MF": "MaterialFunction",
    "EUW": "EditorUtilityWidgetBlueprint"
}

building_type = {"GenlHse", "Govmt"}

building_location_designation = {"C", "CI", "M" , "U", "E", "L", "R", "S", "F"}

texture_type = {"BC", "NM", "ORM", "ORH", "ORS", "NMOp"}

def choose_folder_path():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 选择文件夹
    folder_path = filedialog.askdirectory(title="请选择文件夹")
    if folder_path:
        print("选择的文件夹路径:", folder_path)
    return folder_path

def check_asset_name_prefix(assetdata):
    """
    对UE的资产进行命名前缀检查

    Args:
        assetdata: UE的资产数据（AssetData类型）

    Returns:
        str: 错误信息，如果通过检查则返回 None
    """
    # 1. 获取资产名称
    asset_name = str(assetdata.asset_name)

    # 2. 获取资产类型名称
    asset_class_name = str(assetdata.asset_class_path.asset_name)

    # 3. 获取资产名称的第一个字段（第一个"_"之前的字段）
    parts = asset_name.split('_')
    if len(parts) < 1:
        return "资产名称格式无效"

    prefix = parts[0]

    # 4. 检查第一个字段的字符数量是否大于4
    if len(prefix) > 4:
        return "缺少类型前缀"

    # 5. 用前缀字段查询"前缀-类型对应字典"
    if prefix not in ue_asset_prefix_map:
        return "前缀无效"

    expected_class_name = ue_asset_prefix_map[prefix]
    if expected_class_name != asset_class_name:
        return "前缀错误"

    # 通过检查
    return None

def check_asset_name_special_chars(assetdata):
    """
    对UE的资产命名进行特殊字符检查

    Args:
        assetdata: UE的资产数据（AssetData类型）

    Returns:
        str: 错误信息，如果通过检查则返回 None
    """
    # 1. 获取资产名称
    asset_name = str(assetdata.asset_name)
    errors = []

    # 2. 检查名称内是否带有中文
    for char in asset_name:
        if '\u4e00' <= char <= '\u9fff':
            errors.append("名称带有中文")
            break

    # 3. 检查名称内是否带有除"_"以外的特殊字符
    # 允许的字符：英文大小写字母、数字、下划线
    for char in asset_name:
        if not char.isalnum() and char != '_':
            errors.append("名称带有特殊符号")
            break

    if errors:
        return "; ".join(errors)

    # 通过检查
    return None

def check_build_asset_naming_format(asset_name):
    """
    检查建筑资产的命名格式规范

    Args:
        asset_name: 资产名称（Str类型）

    Returns:
        str: 错误信息，多个错误由";"分割，如果通过检查则返回 None
    """
    errors = []

    # 1. 按"_"分割为字段
    parts = asset_name.split('_')

    # 2. 检查字段数量是否等于7，不等于则加入错误并结束检查
    if len(parts) != 7:
        return "不符合建筑资产字段数量规范"

    # 3. 获取第二个字段，检查是否在有效建筑类型集合内
    if parts[1] not in building_type:
        errors.append("无效建筑类型")

    # 4. 获取第三个字段，判断是否为纯数字字段
    if not parts[2].isdigit():
        errors.append("无效等级风格编号")

    # 5. 获取第五个字段，检查尺寸格式 "100x200x300"
    size_field = parts[4]
    if 'X' in size_field:
        errors.append("尺寸分割符大小写错误")
    else:
        dims = size_field.split('x')
        if len(dims) != 3 :
            errors.append("尺寸格式错误")
        elif not all(dim.isdigit() for dim in dims):
            errors.append("尺寸必须为数字")
            

    # 6. 获取第六个字段，检查是否在有效位置代号集合内
    if parts[5] not in building_location_designation:
        errors.append("无效位置代号")

    # 7. 获取第七个字段，判断是否包含数字
    if any(c.isdigit() for c in parts[6]):
        errors.append("变体描述字段带有数字")

    # 8. 返回所有错误信息
    if errors:
        return "; ".join(errors)
    return None

def check_texture_asset_naming_format(asset_name):
    """
    检查贴图资产的命名规范

    Args:
        asset_name: 资产名称（Str类型）

    Returns:
        str: 错误信息，多个错误由";"分割，如果通过检查则返回 None
    """
    errors = []

    # 1. 按"_"分割为字段
    parts = asset_name.split('_')

    # 2. 检查字段数量是否等于3，不等于则加入错误并结束检查
    if len(parts) != 3:
        return "贴图资产字段数量错误"

    # 3. 获取第3个字段，检查是否在有效贴图后缀集合内
    if parts[2] not in texture_type:
        errors.append("无效贴图后缀")

    # 4. 返回所有错误信息
    if errors:
        return "; ".join(errors)
    return None


# 类型名称 -> 前缀的逆向映射
_ue_class_to_prefix = {v: k for k, v in ue_asset_prefix_map.items()}


def auto_fix_asset_name_prefix():
    """
    自动修复资产命名前缀

    对当前选中的资产，根据其类型自动添加或替换正确的前缀
    """
    # 1. 获取当前选中的所有资产
    assets = AssetLib.get_all_selected_assetsdata()
    if not assets:
        return

    # 2. 遍历每一个资产
    for assetdata in assets:
        asset_name = str(assetdata.asset_name)
        asset_class_name = str(assetdata.asset_class_path.asset_name)

        # 3. 查询类型对应的正确前缀
        correct_prefix = _ue_class_to_prefix.get(asset_class_name)
        if not correct_prefix:
            unreal.log_warning(f"跳过 {asset_name}: 未找到类型 {asset_class_name} 的前缀映射")
            continue

        # 4. 获取资产名称的前缀（第一个"_"前的字段）
        if '_' in asset_name:
            parts = asset_name.split('_', 1)
            current_prefix = parts[0]
            rest = parts[1]
        else:
            current_prefix = ""
            rest = asset_name

        # 5. 判断当前前缀是否需要修复
        if current_prefix in ue_asset_prefix_map:
            # 前缀存在但可能错误，替换前缀
            if current_prefix == correct_prefix:
                unreal.log(f"跳过 {asset_name}: 前缀已正确")
                continue
            new_name = correct_prefix + "_" + rest
        else:
            # 前缀不在映射中，添加新前缀
            new_name = correct_prefix + "_" + asset_name

        # 6. 如果名称未改变则跳过
        if new_name == asset_name:
            continue

        # 7. 重命名资产
        old_path = str(assetdata.package_name)
        new_path = old_path.rsplit('/', 1)[0] + '/' + new_name

        if unreal.EditorAssetLibrary.rename_asset(old_path, new_path):
            unreal.log(f"已修复: {asset_name} -> {new_name}")
        else:
            unreal.log_warning(f"重命名失败: {asset_name}")


def export_naming_error_map_to_csv(error_map):
    """
    将蓝图 Map(Str-Str) 类型的命名错误信息导出为 CSV 表格
    输出路径通过弹窗让用户选择文件夹

    Args:
        error_map: unreal.Map(str, str) 资产名称 -> 错误信息
    """
    from datetime import datetime

    if not error_map:
        unreal.log_warning("error_map 为空，无数据可导出")
        return

    # 弹出文件夹选择窗口获取输出路径
    output_dir = choose_folder_path()
    if not output_dir:
        unreal.log_warning("未选择导出文件夹")
        return

    # 生成带时间戳的文件名（精确到分钟）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    timestamp = timestamp.replace(":", "：")  
    filename = f"资产命名错误信息（{timestamp}）"

    output_path = StatisticLib.generate_output_file_path(output_dir, filename)
    if not output_path:
        return

    # 转换 unreal.Map 为列表格式
    data = []
    for key in error_map.keys():
        data.append([key, error_map[key]])

    # 导出 CSV
    StatisticLib.save_data_to_csv(data, output_path, headers=["资产名称", "错误信息"])


def check_selected_assets_name():
    """
    对当前选中的资产进行命名检查，包括前缀检查和特殊字符检查

    Returns:
        unreal.Map(str, str): 资产名称到错误信息的映射，通过检查的资产不会出现在Map中
    """
    error_map = unreal.Map(str, str)

    # 1. 获取当前选中的所有资产
    assets = AssetLib.get_all_selected_assetsdata()
    if not assets:
        return error_map

    # 2. 遍历所有资产
    for assetdata in assets:
        asset_name = str(assetdata.asset_name)
        errors = []

        # 3. 前缀检查
        prefix_error = check_asset_name_prefix(assetdata)
        if prefix_error:
            errors.append(prefix_error)

        # 4. 特殊字符检查
        special_char_error = check_asset_name_special_chars(assetdata)
        if special_char_error:
            errors.append(special_char_error)

        # 5. 合并错误信息
        if errors:
            error_map[asset_name] = "; ".join(errors)

    return error_map

def check_selected_assets_custom_name(check_items):
    """
    对UE的资产命名进行自定义检查

    Args:
        check_items: 整数列表，指定需要执行的检查项
                     1 - 前缀检查
                     2 - 特殊字符检查
                     3 - 建筑命名格式检查
                     4 - 贴图命名格式检查

    Returns:
        unreal.Map(str, str): 资产名称到错误信息的映射，通过检查的资产不会出现在Map中
    """
    error_map = unreal.Map(str, str)

    # 1. 获取当前选中的所有资产
    assets = AssetLib.get_all_selected_assetsdata()
    if not assets:
        return error_map

    # 2. 遍历所有资产
    for assetdata in assets:
        asset_name = str(assetdata.asset_name)
        errors = []

        # 3. 前缀检查
        if 1 in check_items:
            prefix_error = check_asset_name_prefix(assetdata)
            if prefix_error:
                errors.append(prefix_error)

        # 4. 特殊字符检查
        if 2 in check_items:
            special_char_error = check_asset_name_special_chars(assetdata)
            if special_char_error:
                errors.append(special_char_error)

        # 5. 建筑命名格式检查
        if 3 in check_items:
            build_error = check_build_asset_naming_format(asset_name)
            if build_error:
                errors.append(build_error)

        if 4 in check_items and assetdata.asset_class_path.asset_name == "Texture2D":
            texture_error = check_texture_asset_naming_format(asset_name)
            if texture_error:
                errors.append(texture_error)

        # 6. 合并错误信息
        if errors:
            error_map[asset_name] = "; ".join(errors)

    return error_map


def check_asset_name_by_regex(
    asset_name: str,
    regex_pattern,
    error_message=None,
) -> str | None:
    """
    使用正则表达式对资产命名进行检查。

    核心思想：把原有分散的手动字段拆分 + 逐个 if-else 判断的检查逻辑，
    统一收敛到一个正则表达式，一行配置即可定义全部命名规范。

    Args:
        asset_name    : 资产名称（str）
        regex_pattern : 正则表达式（str 或 list[tuple]）
                        - str : 单一正则，匹配成功即通过
                        - list[tuple] : 多规则模式，每个元素为 (pattern, msg)，
                          按顺序依次检查，收集所有未通过的规则错误
        error_message : 匹配失败时的错误信息
                        - None  : 使用默认错误信息 "命名格式不符合规范"
                        - str   : 统一错误信息
                        - dict  : 按规则索引（int key=0,1,2... 或 str key）映射
                                  不同规则的错误信息，key 对应 regex_pattern 中
                                  各规则的索引或自定义标识

    Returns:
        str | None: 错误信息（多个错误用"; "连接），通过所有检查返回 None

    """
    # ---------- 单规则模式 ----------
    if isinstance(regex_pattern, str):
        pattern = re.compile(regex_pattern)
        if pattern.match(asset_name):
            return None
        # 确定错误信息
        if isinstance(error_message, dict):
            msg = error_message.get("default", error_message.get(0, "命名格式不符合规范"))
        elif isinstance(error_message, str):
            msg = error_message
        else:
            msg = "命名格式不符合规范"
        return msg

    # ---------- 多规则模式 ----------
    if isinstance(regex_pattern, (list, tuple)):
        errors = []
        for idx, item in enumerate(regex_pattern):
            # 解析每条规则：(pattern, msg) 或仅 pattern
            if isinstance(item, (list, tuple)):
                pat_str, rule_msg = item[0], item[1]
            else:
                pat_str, rule_msg = item, None

            pattern = re.compile(pat_str)
            if not pattern.match(asset_name):
                # 错误信息优先级: 规则自带 > dict映射 > 默认
                if rule_msg:
                    errors.append(rule_msg)
                elif isinstance(error_message, dict):
                    errors.append(
                        error_message.get(idx, f"规则{idx+1}不通过")
                    )
                else:
                    errors.append(f"规则{idx+1}不通过")

        if errors:
            return "; ".join(errors)
        return None

    # ---------- 非法输入 ----------
    raise TypeError(
        f"regex_pattern 应为 str 或 list[tuple]，实际收到 {type(regex_pattern).__name__}"
    )

def check_all_selected_assets_by_regex_rules(regex_rule_map) -> "unreal.Map":
    """
    对所有选中的资产，按传入的正则规则进行命名检查。

    该函数将 UE Map 类型的规则表转换为 check_asset_name_by_regex
    的多规则列表模式，逐资产检查并汇总错误。

    Args:
        regex_rule_map : unreal.Map(str, str)
                         key   = 正则表达式
                                 (若 key 以 "ClassPrefix" 开头，如
                                  "ClassPrefix: BP-Blueprint, SM-StaticMesh, ...",
                                  则直接从中解析前缀-类型映射表进行前缀检查，
                                  该键不参与正则匹配)
                         value = 匹配失败时的错误信息

    Returns:
        unreal.Map(str, str):
            key   = 资产路径（package_name）
            value = 错误信息（多条错误用"; "连接）
            通过所有检查的资产不会出现在返回的 Map 中
    """
    # 1. 分离 ClassPrefix 触发键与正则规则
    prefix_type_map = None
    rules_list = []
    for key in regex_rule_map.keys():
        pattern = str(key)
        if pattern.startswith("ClassPrefix"):
            # 解析前缀-类型映射: "ClassPrefix: BP-Blueprint, SM-StaticMesh, ..."
            mapping_str = pattern[len("ClassPrefix"):].lstrip(":： ").strip()
            prefix_type_map = {}
            for pair in mapping_str.split(","):
                pair = pair.strip()
                if not pair:
                    continue
                parts = pair.split("-", 1)
                if len(parts) == 2:
                    prefix_type_map[parts[0].strip()] = parts[1].strip()
            continue  # ClassPrefix 键不参与正则匹配
        message = str(regex_rule_map[key])
        rules_list.append((pattern, message))

    # 2. 获取当前选中的所有资产
    assets = AssetLib.get_all_selected_assetsdata()
    if not assets:
        return unreal.Map(str, str)

    # 3. 遍历每个资产，执行正则规则检查 + 可选前缀检查
    error_map = unreal.Map(str, str)
    for assetdata in assets:
        asset_path = str(assetdata.package_name)
        asset_name = str(assetdata.asset_name)

        print(f"检查资产: {asset_name} rules_list: {rules_list}")

        all_errors = []

        # 3a. 正则规则检查
        if rules_list:
            regex_error = check_asset_name_by_regex(
                asset_name=asset_name,
                regex_pattern=rules_list,
            )
            if regex_error:
                all_errors.append(regex_error)

        # 3b. 前缀-类型检查 (使用 ClassPrefix 键中传入的映射表)
        if prefix_type_map:
            asset_class_name = str(assetdata.asset_class_path.asset_name)
            parts = asset_name.split('_')
            if len(parts) >= 1:
                prefix = parts[0]
                if prefix in prefix_type_map and prefix_type_map[prefix] != asset_class_name:
                    all_errors.append("前缀错误")

        if all_errors:
            error_map[asset_name] = "; ".join(all_errors)

    return error_map
