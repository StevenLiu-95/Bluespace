import unreal

def get_all_assetsdata_under_folder(path):
    if path.startswith("/All/"):
        real_path = path.replace("/All/", "/", 1)
    else:
        real_path = path
    unreal.log(f"Scanning the path: {real_path}")
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_registry.get_assets_by_path(real_path, recursive=True)
        
    if not assets:
        unreal.log(f"Not find any assets in: {real_path}")

    return assets

def get_all_selected_assetsdata():
    all_selected_assets = []

    selected_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
    if selected_paths:
        for path in selected_paths:
            assets = get_all_assetsdata_under_folder(path)
            all_selected_assets.extend(assets)
    
    selected_assets = unreal.EditorUtilityLibrary.get_selected_asset_data()
    if selected_assets:
        all_selected_assets.extend(selected_assets)
    
    validate_selected_assets(all_selected_assets)
    
    return all_selected_assets

def get_uassets(assetsdata):
    uassets = [
        a for a in assetsdata 
        if unreal.AssetRegistryHelpers.is_u_asset(a) 
        and not str(a.asset_name).endswith('_C')
    ]
    return uassets

def get_redirectors(assetsdata):
    redirectors = [
        a for a in assetsdata 
        if unreal.AssetRegistryHelpers.is_redirector(a) 
        and not str(a.asset_name).endswith('_C')
    ]
    if not redirectors:
        unreal.log(f"Not find any redirectors")
    return redirectors

def get_assets_by_class(assetsdata, class_type):
    target_assets = [
        a for a in assetsdata 
        if str(a.asset_class_path.asset_name) == class_type
    ]
    return target_assets

def get_all_selected_uassets():
    assets = get_all_selected_assetsdata()
    uassets = get_uassets(assets)
    return uassets

def get_all_selected_bpassets():
    assets = get_all_selected_assetsdata()
    bpassets = get_assets_by_class(assets, "Blueprint")
    # for a in bpassets:
    #     print(a)
    return bpassets

def get_all_selected_smassets():
    assets = get_all_selected_assetsdata()
    smassets = get_assets_by_class(assets, "StaticMesh")
    if not smassets:
        unreal.log_warning("[TweakComponentTransform] 未选中 StaticMesh")
        return
    return smassets

def debug_asset_info(assetsdata):
    if not assetsdata: return
    for asset in assetsdata:
        print(f"AssetData = {assetsdata}")
        # unreal.log(f"资产: {asset.asset_name}, 路径: {asset.package_name}, 类型: {asset.asset_class_path.asset_name}")
        
        # for member in dir(asset):
        #     # 过滤掉Python内置方法
        #     if not member.startswith('_'):
        #         unreal.log(member)

def debug_redirector_dependency(redirectors):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if not redirectors: return
    for asset in redirectors:
        # Get soft dependencies (assets not strictly required for usage)
        soft_dependencies = asset_registry.get_dependencies(asset.package_name, unreal.AssetRegistryDependencyOptions(True, True))
        print(f"Soft Dependencies: {soft_dependencies}")

def get_asset_objs(assetsdata):
    assetobjs = []
    for assetdata in assetsdata:
        assetobjs.append(assetdata.get_asset())
    return assetobjs

# def get_asset_data_from_actor(actor):
#     asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
#     bp_path = actor.get_class().get_path_name()
#     print(f"bp path name = {bp_path}")
#     real_path = bp_path.split(".")[0]
#     bp_asset_data = asset_registry.get_asset_by_object_path(real_path)
#     print(f"bp asset data = {bp_asset_data}")
#     return bp_asset_data

# def load_asset_obj_from_actor(actor):
#     asset_data = get_asset_data_from_actor(actor)
#     assetobj = load_asset_obj_by_assetdata(asset_data)
#     return assetobj

def load_asset_obj_by_assetdata(assetdata):
    # assetobj = assetdata.get_asset()
    real_path = assetdata.package_name
    assetobj = unreal.EditorAssetLibrary.load_asset(real_path)
    # print(assetobj)

    return assetobj
    
def get_cdo_by_assetdata(assetdata):
    real_path = assetdata.package_name
    assetobj = unreal.EditorAssetLibrary.load_asset(real_path)
    # print(assetobj)

    cdo = unreal.get_default_object(assetobj.get_class())
    # print(f"cdo1 = {cdo}")
    # cdo = bp_asset.get_class().get_default_object()
    # print(f"cdo2 = {cdo}")

    return cdo

def get_bp_asset_obj_root_handle(bp_asset):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    handles = subsystem.k2_gather_subobject_data_for_blueprint(bp_asset)
    if not handles: return
    root_handle = handles[0]

    for handle in handles:
        obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(handle))
        # print(f"scan current obj : {obj}")
        if obj.get_class() == unreal.SceneComponent.static_class():
            root_handle = handle
            break
    return root_handle

def reset_blueprint_root_transform(assetdata):
    bp_asset = load_asset_obj_by_assetdata(assetdata)

    root_handle = get_bp_asset_obj_root_handle(bp_asset)
    
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    root_obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(root_handle))
    if root_obj:
        # print(f"location = {root_obj.relative_location}")
        if (root_obj.relative_location == unreal.Vector()
            and root_obj.relative_rotation == unreal.Rotator()
            and root_obj.relative_scale3d == unreal.Vector(1,1,1)):
            print("root trans is initialized")
        else:
            root_obj.reset_relative_transform()
            
            unreal.BlueprintEditorLibrary.compile_blueprint(bp_asset)
            bp_asset.modify(True)
            # unreal.EditorAssetLibrary.save_asset(real_path)


import sys
path = r"\\10.130.67.26\千图共享盘\JinYong_TA\Scripts\Python\Unreal"
sys.path.append(path)
import ZEditorPromptFunctionLibrary
from ZEditorPromptFunctionLibrary import EditorPrompt

import importlib
importlib.reload(ZEditorPromptFunctionLibrary)

def validate_selected_assets(assets):
    if not assets:
        unreal.log_warning("Please Select Folders or Assets in Content Browser")
        message = "请在内容浏览器中选择文件夹或资产"
        # EditorPrompt.show_notification(message)
        EditorPrompt.show_modal_warning(message)



def tweak_bpasset_anchor_pos(bp_asset, offset_position):
    # because the child handles of bp will be traversed twice
    delta_pos = unreal.Vector(-offset_position.x, -offset_position.y, -offset_position.z)/2
    # print(f"asset delta pos = {delta_pos}")

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    handles = subsystem.k2_gather_subobject_data_for_blueprint(bp_asset)
    if not handles: return
    # root_handle = handles[0]

    # for handle in handles[1:]:
    #     obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(handle))
    #     print(f"obj: {obj.get_name()}")

    root_handle = get_bp_asset_obj_root_handle(bp_asset)
    # print(f"root_handle: {root_handle}")
    root_obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(root_handle))

    for handle in handles[1:]:
        # print(f"handle: {handle}")
        obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(handle))
        if not isinstance(obj, unreal.SceneComponent): continue

        if obj != root_obj: 
            # print(f"child obj: {obj.get_name()}")
            obj.add_relative_location(delta_pos, False, True)
        # else:
        #     # print(f"root obj: {obj.get_name()}")

    unreal.BlueprintEditorLibrary.compile_blueprint(bp_asset)
    bp_asset.modify(True)


def tweak_bpasset_anchor_rot(bp_asset, offset_rotation):

    offset_rotation = unreal.Rotator(offset_rotation.roll/2, offset_rotation.pitch/2, offset_rotation.yaw/2)
    
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    handles = subsystem.k2_gather_subobject_data_for_blueprint(bp_asset)
    if not handles: return
    root_handle = get_bp_asset_obj_root_handle(bp_asset)

    pivot_math_tr = unreal.Transform()
    pivot_math_tr.rotation = offset_rotation.quaternion()

    for handle in handles:
        if handle == root_handle: continue
            
        data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = lib.get_object(data)
        
        if isinstance(obj, unreal.StaticMeshComponent):
            old_tr = obj.get_relative_transform()
            target_tr = old_tr.multiply(pivot_math_tr)
            
            obj.set_editor_property("relative_location", target_tr.translation)
            obj.set_editor_property("relative_rotation", target_tr.rotation.rotator())

    unreal.BlueprintEditorLibrary.compile_blueprint(bp_asset)
    bp_asset.modify(True)



def get_reference_assets_by_smasset(smasset, class_type=None):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    dependency_options = unreal.AssetRegistryDependencyOptions(True, True)

    reference_assets = []
    referencers = asset_registry.get_referencers(smasset.package_name, dependency_options)

    for ref_package in referencers:
        assets = asset_registry.get_assets_by_package_name(ref_package)

        if class_type:
            assets = get_assets_by_class(assets, class_type)

        reference_assets.extend(assets)

    return reference_assets


def find_target_staticmesh_components_in_blueprint(bp, smasset):
    target_mesh_key = str(smasset.package_name)

    subsys = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    matched_components = []
    seen = set()

    for h in subsys.k2_gather_subobject_data_for_blueprint(bp):
        obj = lib.get_object(subsys.k2_find_subobject_data_from_handle(h))
        if not isinstance(obj, unreal.StaticMeshComponent):
            continue

        comp_mesh = obj.get_editor_property("static_mesh")
        if not comp_mesh:
            continue

        comp_mesh_key = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(comp_mesh).split(".")[0]
        if comp_mesh_key != target_mesh_key:
            continue

        key = obj.get_path_name()
        if key in seen:
            continue
        seen.add(key)

        matched_components.append(obj)
     
    return matched_components


def add_relative_transform_to_component(
        component,
        offset_location=None,
        offset_rotation=None,
        offset_scale=None
        ):
    if not component:
        unreal.log_warning("请添加正确component")
        return
    
    if offset_location is None and offset_rotation is None and offset_scale is None:
        unreal.log_warning("请添加正确transform")
        return
    
    if offset_location is not None:
        current_location = component.get_editor_property("relative_location")
        component.set_editor_property("relative_location", current_location + offset_location)
    
    if offset_rotation is not None:
        current_rotation = component.get_editor_property("relative_rotation")
        new_rotation = (current_rotation.quaternion() * offset_rotation.quaternion()).rotator()
        component.set_editor_property("relative_rotation", new_rotation)


def tweak_bpasset_component_transform(smasset, offset_location, offset_rotation):
    assetdatas = get_reference_assets_by_smasset(smasset, "Blueprint")
    for assetdata in assetdatas:
        bp = load_asset_obj_by_assetdata(assetdata)
        sm_components = find_target_staticmesh_components_in_blueprint(bp, smasset)
        for component in sm_components:
            add_relative_transform_to_component(component,offset_location,offset_rotation)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)

def tweak_smasset_pivot_transform(smassetdata, offset_location, offset_rotation):
    smasset = smassetdata.get_asset()
    dm = unreal.DynamicMesh()
    asset_options = unreal.GeometryScriptCopyMeshFromAssetOptions()
    requested_lod = unreal.GeometryScriptMeshReadLOD()
    unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(smasset, dm, asset_options, requested_lod)

    # current_loc = smactor.get_actor_location()
    dm.translate_pivot_to_location(offset_location)
    # smactor.set_actor_location(current_loc, False, False)

    options = unreal.GeometryScriptCopyMeshToAssetOptions()
    target_lod = unreal.GeometryScriptMeshWriteLOD()
    unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm, smasset, options, target_lod)



def get_redirectors_info(redirectors):
    redirector_data = []
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    for asset in redirectors:
        try:
            # get destination object
            soft_dependencies = asset_registry.get_dependencies(asset.package_name, unreal.AssetRegistryDependencyOptions(True, True))
            # print(f"Soft Dependencies: {soft_dependencies}")
            target = asset_registry.get_asset_by_object_path(soft_dependencies[0])
            if target:
                redirector_name = asset.asset_name
                target_name = str(soft_dependencies[0]).split("/")[-1]
                redirector_data.append([redirector_name, target_name])
        except Exception as e:
            unreal.log_warning(f"处理重定向器 {asset.package_name} 时出错: {str(e)}")
    return redirector_data

        

def check_illegal_asset_name(asset_name):
    asset_name = str(asset_name)
    parts = asset_name.split('_')
    if len(parts) < 7:
        data = (asset_name, "名称字段不足缺少下划线分割")
        return data
    
    last_four = parts[-4:]
    target_part = last_four[1]
    if 'x' in target_part:
        try:
            values = target_part.split('x')
            if len(values) == 3:
                float(values[0])
                float(values[1])
                float(values[2])
                return
        except ValueError:
            pass
    data = (asset_name, f"无效尺寸: {target_part}")
    return data

def check_blueprint_hierarchy_depth(assetdata):
    """获取蓝图内部组件的最大嵌套深度"""
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actor = subsystem.spawn_actor_from_object(assetdata.get_asset(), unreal.Vector(0, 0, 0))

    # 获取根组件
    root_component = actor.root_component
    if not root_component:
        return 1  # 只有根组件一层
    
    # 递归计算最大深度
    max_depth = 1
    stack = [(root_component, 1)]  # (组件, 当前深度)
    
    while stack:
        current_component, current_depth = stack.pop()
        max_depth = max(max_depth, current_depth)
        
        # 获取子组件
        child_components = current_component.get_children_components(False)
        for child in child_components:
            stack.append((child, current_depth + 1))
    
    unreal.EditorLevelLibrary.destroy_actor(actor)
    return max_depth


def check_illegal_asset(uassets):
    illegal_assets = []
    if uassets:
        for asset in uassets:
            asset_name = asset.asset_name
            # unreal.log(f"check asset: {asset_name}")
            
            # 检测资产名称规范
            data = check_illegal_asset_name(asset_name)
            if data:
                illegal_assets.append(data)
            
            # 检测蓝图层级规范
            data = []
            if str(asset.asset_class_path.asset_name) == "Blueprint":
                bp_hierarchy_depth = check_blueprint_hierarchy_depth(asset)
                if bp_hierarchy_depth > 2:
                    data = (asset_name, f"蓝图层级: {bp_hierarchy_depth}")
            if data:
                illegal_assets.append(data)

        if illegal_assets:
            unreal.log_warning(f"以下资产名称不合规:")
            for asset in illegal_assets:
                unreal.log_warning(asset)
        else:
            unreal.log_warning("所选路径下资产检查合规")
    
    return illegal_assets



# def get_module_classification_info_by_asset_name(asset_name):
#     parts = str(asset_name).split('_')
#     sizeinfo = parts[-3].split('x')
#     row_data = {
#         "ModuleName": asset_name,
#         "Class": parts[1],
#         "Style": parts[2],
#         "Variation": parts[-1],
#         "SizeZ": float(sizeinfo[0]),
#         "SizeX": float(sizeinfo[1]),
#         "SizeY": float(sizeinfo[2]),
#         "ElementName": parts[3],
#     }
#     return row_data

def get_module_classification_info(assetdata):
    # asset_name = asset.asset_name
    # print(f"Processing Asset {asset.asset_name}")'
    object_path = unreal.AssetRegistryHelpers.get_asset(assetdata).get_path_name()
    object_path = str(object_path)

    asset_name = object_path.split(".")[-1]
    parts = asset_name.split('_')

    root_folder = "/Game/Environments/Meshes/_TempBlueprints/"
    sub_folders = object_path.split(root_folder)[-1].split("/")
    
    # 初始化默认值
    result = {
        "ModuleName": asset_name,
        "Class": "Unknown",
        "Style": "Unknown",
        "Variation": "Unknown",
        "SizeZ": 0.0,
        "SizeX": 0.0,
        "SizeY": 0.0,
        "ElementName": "Unknown",
        "unreal_instance": "Unknown",
        "Material": 0,
        "unreal_material": "Unknown",
        "material_slot_name": "", 
        "Reference" : 0,
        "ReferenceDetail" : None,
        "ParseError": None
    }
    
    try:
        if assetdata.get_class() == unreal.StaticMesh.static_class():
            bbox = assetdata.get_asset().get_bounding_box()
            # center, dimensions = bbox.get_box_center_size()
            dimensions = bbox.max - bbox.min
            result.update({
                "SizeZ": round(dimensions.z),
                "SizeX": round(dimensions.x),
                "SizeY": round(dimensions.y)
            })

            sub_folders = object_path.split("/Game/Environments/Meshes/")[-1].split("/")
            if len(sub_folders) > 3:
                result["Class"] = sub_folders[-3]
            if len(sub_folders) > 2:
                result["ElementName"] = sub_folders[-2]
            
            materials = assetdata.get_asset().static_materials
            result["Material"] = len(materials)
            
            # matstr_array = [str(mat) for mat in materials]
            # matstr_array = process_material_string_array(matstr_array)
            material_interface_array = [str(mat.material_interface.get_path_name()) if mat.material_interface else "None" for mat in materials]
            material_slot_name_array = [str(mat.material_slot_name) for mat in materials]
            result["unreal_material"] = '\n'.join(material_interface_array)
            result["material_slot_name"] = '\n'.join(material_slot_name_array)
        
        else:
            # 尝试解析尺寸信息
            for part in parts:
                if 'x' in part and part.count('x') == 2:
                    sizeinfo = part.split('x')
                    if len(sizeinfo) == 3:
                        result.update({
                            "SizeZ": float(sizeinfo[0]),
                            "SizeX": float(sizeinfo[1]),
                            "SizeY": float(sizeinfo[2])
                        })
                    break
            
            # 尝试解析其他字段
            if sub_folders:
                result["Class"] = sub_folders[0]
            if len(sub_folders) > 1:
                result["Style"] = sub_folders[1]
            if len(parts) > 3:
                result["ElementName"] = parts[-4]
        if parts:  # 最后一部分作为Variation
            result["Variation"] = parts[-1]
        
        result["unreal_instance"] = object_path

        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        # print(assetdata.package_name)
        referencers = asset_registry.get_referencers(assetdata.package_name, unreal.AssetRegistryDependencyOptions(True, True))
        result["Reference"] = len(referencers)
        
        refstr_array = [str(ref) for ref in referencers]
        result["ReferenceDetail"] = '\n'.join(refstr_array)

    except Exception as e:
        unreal.log_warning(e)
        result["ParseError"] = str(e)
    
    return result

# def process_material_string_array(matstr_array):
#     processed_matstr_array = []
#     for mat_str in matstr_array:
#         # 使用正则表达式提取需要的信息
#         # match = re.search(r"material_interface:\s*\"([^\"]+)\",\s*material_slot_name:\s*\"([^\"]+)\"", mat_str)
#         match = re.search(r"material_interface:\s*(.*?),\s*material_slot_name:\s*(.*?)(?:,|$)", mat_str)
#         if match:
#             material_interface, material_slot_name = match.groups()
#             material_interface = material_interface.replace("/Script/Engine.MaterialInstanceConstant'", "").replace("'", "")
#             cleaned_str = f'{{material_interface: {material_interface}, material_slot_name: {material_slot_name}}}'
#             processed_matstr_array.append(cleaned_str)
#     return processed_matstr_array



def auto_fill_material_slot_name(assetdata, ref_mapping=None):
    if assetdata.get_class() == unreal.StaticMesh.static_class():
        auto_fill_static_mesh_material_slot_name(assetdata, ref_mapping)

def auto_fill_static_mesh_material_slot_name(assetdata, ref_mapping):
    mesh_updated = False
    unreal.log(f"检测 {assetdata.asset_name} 材质槽:")
    assetobj = load_asset_obj_by_assetdata(assetdata)
    materials = assetobj.static_materials.copy()
    for i, mat in enumerate(materials):
        material_interface = mat.material_interface
        
        if not material_interface:
            print(f"material_interface = {None}, current_slot_name = {mat.material_slot_name}")
            continue
        else:
            material_name = mat.material_interface.get_name()

            # 检查是否在CSV映射中
            if material_name in ref_mapping:
                new_slot_name = ref_mapping[material_name]
                current_slot_name = mat.material_slot_name

                if current_slot_name != new_slot_name:
                    mat.material_slot_name = new_slot_name
                    materials[i] = mat
                    unreal.log(f"更新 {assetdata.asset_name} 的材质槽 {i}: {material_name}，从 '{current_slot_name}' 改为 '{new_slot_name}'")
                    mesh_updated = True
    
    # 如果网格有更新，保存
    if mesh_updated:
        assetobj.static_materials = materials
        assetobj.modify(True)
        # unreal.EditorAssetLibrary.save_loaded_asset(assetobj)


def merge_actors_to_static_mesh(actors_to_merge: list,
                                base_package_path: str,
                                merged_actor_label: str = None) -> unreal.StaticMeshActor:
    """
    将多组 StaticMeshActor 合并为新的 StaticMeshActor。
    特性：
      - pivot_point_at_zero=True
      - destroy_source_actors=True
      - 可设置 merged_actor_label
    """
    if not actors_to_merge:
        return None
    
    if not isinstance(actors_to_merge, (list, tuple)):
        actors_to_merge = [actors_to_merge]

    print(f"path: "+base_package_path)
    print(f"name: "+merged_actor_label)
    merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
    merge_options.destroy_source_actors = False
    merge_options.new_actor_label = merged_actor_label
    merge_options.spawn_merged_actor = True
    merge_options.base_package_name = base_package_path
    mesh_merging_settings = unreal.MeshMergingSettings()
    mesh_merging_settings.pivot_point_at_zero = False
    mesh_merging_settings.merge_physics_data = True
    mesh_merging_settings.merge_mesh_sockets = True
    mesh_merging_settings.bake_vertex_data_to_mesh = True
    nanite_settings = unreal.MeshNaniteSettings()
    nanite_settings.enabled = True
    mesh_merging_settings.nanite_settings = nanite_settings
    merge_options.mesh_merging_settings = mesh_merging_settings

    merged_actor = unreal.EditorLevelLibrary.merge_static_mesh_actors(actors_to_merge, merge_options)
    # if merged_actor and merged_actor_label:
    #     merged_actor.set_actor_label(merged_actor_label)
    if merged_actor:
        unreal.log(f"Actor '{merged_actor.get_actor_label()}' 已生成")
    return merged_actor


