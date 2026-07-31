import unreal

def get_selected_actors_in_level():
    selected_actors = []
    # get selected actors
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not selected_actors:
        unreal.log_warning("请先在场景中选择一个蓝图 Actor！")
    return selected_actors

def select_actors(actors):
    # unreal.EditorLevelLibrary.set_selected_level_actors(actors)
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    subsystem.set_selected_level_actors([])
    print(actors)
    if not isinstance(actors, (list, tuple)):
        actors = [actors]
    subsystem.set_selected_level_actors(actors)

def set_unique_actor_label(actor, desired_label, mark_dirty=False):
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

    existing_labels = {a.get_actor_label() for a in all_actors if a != actor}

    if desired_label not in existing_labels:
        actor.set_actor_label(desired_label, mark_dirty)
        return desired_label

    counter = 1
    while True:
        new_label = f"{desired_label}_{counter}"
        if new_label not in existing_labels:
            actor.set_actor_label(new_label, mark_dirty)
            return new_label
        counter += 1


def is_bp_actor(actor):
    class_name = actor.get_class().get_name()
    # print(f"actor class name = {class_name}")
    if class_name.endswith("_C"):
        # print("actor is blueprint instance")
        return True
    else:
        return False

def is_valid_staticmesh_actor(actor):
    """判断是否为有效的StaticMeshActor"""
    if not actor:
        return False
    
    actor_name = actor.get_name()
    # 检查类型
    if not isinstance(actor, unreal.StaticMeshActor):
        unreal.log_warning(f"Actor '{actor_name}' 不是StaticMeshActor")
        return False
    # 检查组件
    if not actor.static_mesh_component:
        unreal.log_warning(f"Actor '{actor_name}' 没有StaticMeshComponent")
        return False
    # 检查资产
    if not actor.static_mesh_component.static_mesh:
        unreal.log_warning(f"Actor '{actor_name}' 没有赋予StaticMesh资产")
        return False
    unreal.log(f"Actor '{actor_name}' 是StaticMeshActor")
    return True


def get_asset_data_from_actor(actor):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    bp_path = actor.get_class().get_path_name()
    print(f"bp path name = {bp_path}")
    real_path = bp_path.split(".")[0]
    bp_asset_data = asset_registry.get_asset_by_object_path(real_path)
    print(f"bp asset data = {bp_asset_data}")
    return bp_asset_data

def get_static_mesh_actor_asset_name(actor):
    mesh_name = ""
    if is_valid_staticmesh_actor(actor):
        mesh_name = actor.static_mesh_component.static_mesh.get_name()
        unreal.log(f"asset_name = {mesh_name}")
    return str(mesh_name)

def get_static_mesh_actor_asset_package_path(actor):
    package_path = ""
    if is_valid_staticmesh_actor(actor):
        package_path = actor.static_mesh_component.static_mesh.get_path_name()
        # last_slash = str(asset_path).rfind('/')
        # if last_slash != -1:
        #     package_path = asset_path[:last_slash]
        # unreal.log(f"packag path = {package_path}")
    return str(package_path)



def create_empty_actor(
    desired_label = "", 
    b_use_unique_label = False,
    position = unreal.Vector(0, 0, 0), 
    rotation = [0.000000, 0.000000, 0.000000], 
    scale3d = unreal.Vector(1, 1, 1) 
    ):
    new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.Actor, 
        position,
        rotation
    )
    if not new_actor: return

    new_actor.set_actor_scale3d(scale3d)
    
    if desired_label:
        if b_use_unique_label:
            set_unique_actor_label(new_actor, desired_label)
        else:
            new_actor.set_actor_label(desired_label, False)
    
    return new_actor

def copy_root_actor(actor, b_use_full_trans = True, b_use_unique_label = False):
    label = actor.get_actor_label()
    pos = actor.get_actor_location()
    rot = actor.get_actor_rotation()
    scale = actor.get_actor_scale3d()
    if b_use_full_trans:
        root_actor = create_empty_actor(label, b_use_unique_label, pos, rot, scale)
    else:
        root_actor = create_empty_actor(label, b_use_unique_label, pos)
    return root_actor

def attach_to_root_actor(
        actors_to_attach,
        root_actor,
        socket_name="",
        location_rule=unreal.AttachmentRule.KEEP_WORLD,
        rotation_rule=unreal.AttachmentRule.KEEP_WORLD,
        scale_rule=unreal.AttachmentRule.KEEP_WORLD,
        weld_simulated_bodies=False
    ):
    success_count = 0

    if not isinstance(actors_to_attach, (list, tuple)):
        actors_to_attach = [actors_to_attach]

    for actor in actors_to_attach:
        if actor:
            try:
                set_actor_mobility(actor, 2)
                actor.attach_to_actor(
                    parent_actor=root_actor,
                    socket_name=unreal.Name(socket_name),
                    location_rule=location_rule,
                    rotation_rule=rotation_rule,
                    scale_rule=scale_rule,
                    weld_simulated_bodies=weld_simulated_bodies
                )
                success_count += 1
                unreal.log(f"成功附加 {actor.get_name()} 到 {root_actor.get_name()}")
            except Exception as e:
                unreal.log_error(f"附加 {actor.get_name()} 失败: {str(e)}")
    
    unreal.log(f"附加完成: 成功 {success_count}/{len(actors_to_attach)}")
    return success_count > 0

def set_actor_mobility(actor, type=2):
    """
    unreal.ComponentMobility - 
        MOVABLE: Type = 2; 
        STATIC: Type = 0; 
        STATIONARY: Type = 1;
    """
    obj = actor.get_editor_property("root_component")
    if isinstance(obj, (unreal.SceneComponent, unreal.StaticMeshComponent, unreal.InstancedStaticMeshComponent)):
        if type == 2:
            obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
        else:
            obj.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

def set_actor_visibility_in_editor(selected_actors, b_visible):
    if b_visible:
        command = "ACTOR UNHIDE SELECTED STARTUP"
    else:
        command = "ACTOR HIDE SELECTED STARTUP"
    world_context_object = unreal.UnrealEditorSubsystem().get_game_world()
    unreal.SystemLibrary.execute_console_command(world_context_object, command)

    for actor in selected_actors:
        # print(actor.is_hidden_ed())
        actor.set_is_temporarily_hidden_in_editor(not b_visible)

def set_actor_visibility_in_game(selected_actors, b_visible):
    for actor in selected_actors:
        # print(actor.is_hidden_ed_at_startup())
        actor.set_editor_property("hidden", not b_visible)
        # actor.set_actor_hidden_in_game(not b_visible)

# def get_all_child_actors(actor):
#     actors = get_all_child_actors(include_descendants=True)
#     return actors

# def reset_child_instance_relative_location(actor):
#     actor.reset_editor_property("relative_location")
#     subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
#     lib = unreal.SubobjectDataBlueprintFunctionLibrary

#     handles = subsystem.k2_gather_subobject_data_for_instance(actor)
#     if not handles or len(handles)<=2: return

#     for handle in handles[2:]:
#         obj = lib.get_object(subsystem.k2_find_subobject_data_from_handle(handle))
#         print(obj)
#         obj.reset_editor_property("relative_location")

def spawn_new_actor_by_ref_actor(actor, asset_data=None):
    # transform = actor.get_actor_transform()
    # load_asset_to_current_scene(asset_data, transform.translation)

    new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        actor.get_class(),
        actor.get_actor_location(),
        actor.get_actor_rotation()
    )
    new_actor.set_actor_scale3d(actor.get_actor_scale3d())
    for tag in actor.tags:
        new_actor.add_tag(tag)
    return new_actor

def replace_actor_by_new_instance(actor, b_in_ori_hierachy=True, b_in_ori_level=False):
    new_actor = spawn_new_actor_by_ref_actor(actor)
    
    # set to original folder path
    if b_in_ori_hierachy:
        folder_path = actor.get_folder_path()
        unreal.log(f"Put actor [{new_actor.get_actor_label(False)}] in folder path: {folder_path}")
        new_actor.set_folder_path(folder_path)

    editor_subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    ori_lev = editor_subsys.get_current_level()
    target_lev = actor.get_level()
    if b_in_ori_level and target_lev!=ori_lev:
        editor_world = unreal.EditorLevelLibrary.get_editor_world()
        lev_streaming = unreal.GameplayStatics.get_streaming_level(editor_world, target_lev.get_package().get_name())
        unreal.log(f"target level package name = [{target_lev.get_package().get_name()}]")
        # guid = new_actor.actor_guid
        # unreal.log(f"actor guid = [{guid}]")
        # inst_guid = new_actor.actor_instance_guid
        # unreal.log(f"actor instance guid = [{inst_guid}]")
        target_label = new_actor.get_actor_label(False)
        unreal.EditorLevelUtils.move_actors_to_level([new_actor], lev_streaming)
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        for a in all_actors:
            # actor_guid = a.actor_guid
            # unreal.log(f"actor [{actor.get_actor_label(False)}], guid = [{actor_guid}, inst_guid = [{a.actor_instance_guid}]")
            label = a.get_actor_label(False)
            lev = a.get_level()
            if label == target_label and lev == target_lev:
                new_actor = a
        
    # attach to original parent
    if b_in_ori_level and b_in_ori_hierachy:
        parent_actor = actor.get_attach_parent_actor()
        if parent_actor:
            stat = new_actor.attach_to_actor(
                parent_actor, 
                socket_name = 'None', 
                location_rule = unreal.AttachmentRule.KEEP_WORLD,
                rotation_rule = unreal.AttachmentRule.KEEP_WORLD,
                scale_rule = unreal.AttachmentRule.KEEP_WORLD)
            if stat:
                unreal.log(f"new_actor [{new_actor.get_actor_label(False)}] is successfully attached to original parent.]")
            else:
                unreal.log_warning(f"new_actor [{new_actor.get_actor_label(False)}] failed to attach to original parent.]")

    unreal.EditorLevelLibrary.destroy_actor(actor)
    return new_actor



def spawn_static_meshes(blueprint_actor):
    # make sure it is an Actor
    if not isinstance(blueprint_actor, unreal.Actor):
        unreal.log_warning("选中的对象不是 Actor！")
        return
    
    # get all StaticMesh components
    static_mesh_components = blueprint_actor.get_components_by_class(unreal.StaticMeshComponent)
    if not static_mesh_components:
        unreal.log_warning("Actor没有 StaticMesh 组件！")
        return
    
    unreal.log(f"正在处理 Actor: {blueprint_actor.get_name()}")
    
    spawned_mesh_actors = []

    # foreach StaticMesh component
    for component in static_mesh_components:
        static_mesh = component.static_mesh
        if not static_mesh:
            unreal.log_warning(f"组件 {component.get_name()} 没有 StaticMesh，跳过")
            continue
        
        # get world transform
        world_transform = component.get_world_transform()
        
        # generate StaticMesh Actor
        mesh_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            static_mesh,
            world_transform.translation,  # 位置
            world_transform.rotation.rotator(),  # 旋转
            transient=False  # 设为 False 使其永久存在
        )
        
        if mesh_actor:
            # set scale
            mesh_actor.set_actor_scale3d(world_transform.scale3d)
            copy_material_overrides(component, mesh_actor)
            spawned_mesh_actors.append(mesh_actor)
            unreal.log(f"已生成 StaticMesh: {static_mesh.get_name()} (Scale: {world_transform.scale3d})")

    return spawned_mesh_actors

def copy_material_overrides(source_component, target_actor):
    """复制材质覆盖从源组件到目标Actor"""
    try:
        # 获取目标Actor的StaticMeshComponent
        target_component = target_actor.static_mesh_component
        if not target_component:
            unreal.log_warning(f"目标Actor没有StaticMeshComponent: {target_actor.get_name()}")
            return
        
        # 获取源组件的材质覆盖
        source_materials = source_component.get_editor_property("override_materials")
        
        if source_materials:
            # 应用材质覆盖到目标组件
            target_component.set_editor_property("override_materials", source_materials)
            unreal.log(f"已复制 {len(source_materials)} 个材质覆盖")
            
            # 记录详细的材质信息
            for i, material in enumerate(source_materials):
                material_name = material.get_name() if material else "None"
                unreal.log(f"  材质槽位 {i}: {material_name}")
        
    except Exception as e:
        unreal.log_error(f"复制材质覆盖时出错: {str(e)}")

def spawn_static_meshes_and_remove_selected_actors(b_keep_root=True):
    selected_actors = get_selected_actors_in_level()
    if len(selected_actors) < 1: return

    # stored StaticMesh Actor
    new_actors = []
    
    for actor in selected_actors:
        spawned_mesh_actors = spawn_static_meshes(actor)
        if spawned_mesh_actors:
            new_actors.extend(spawned_mesh_actors)
            
            if b_keep_root:
                root_actor = copy_root_actor(actor)
                attach_to_root_actor(spawned_mesh_actors, root_actor)
                new_actors.append(root_actor)
            
        unreal.EditorLevelLibrary.destroy_actor(actor)
        unreal.log(f"删除选中Actor: {actor.get_name()}")

    # select all generated StaticMesh
    if new_actors:
        select_actors(new_actors)
    
    unreal.log("操作完成！")

# def convert_actors_to_static_mesh_actors(actors, path, name):
#     if not isinstance(actors, (list, tuple)):
#         actors = [actors]
#     static_mesh_package_path = path + "/" + name
#     unreal.EditorLevelLibrary.convert_actors(actors, unreal.StaticMeshActor, static_mesh_package_path)



def get_all_components_transforms(actor):
    if not actor: return
    transforms = []
    components = actor.get_components_by_class(unreal.PrimitiveComponent)
    for component in components:
        transform = component.get_world_transform()
        transforms.append(transform)
    return transforms

def compute_center_position(transforms):
    if transforms:
        anchor_position = unreal.Vector(0, 0, 0)
        for transform in transforms:
            anchor_position += transform.translation
        anchor_position /= len(transforms)
        return anchor_position


# def load_all_assets_to_current_scene(uassets):
#     subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
#     spawn_location = unreal.Vector(0, 0, 0)
#     # spawn_rotation = unreal.Rotator(0, 0, 0)
#     temp_actors = []
#     for asset in uassets:
#         temp_actor = subsystem.spawn_actor_from_object(asset.get_asset(), spawn_location)
#         temp_actors.append(temp_actor)
#         # print(asset.asset_name)
#     select_actors(temp_actors)

def load_asset_to_current_scene(uasset, spawn_location=unreal.Vector(0, 0, 0)):
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    # spawn_location = unreal.Vector(0, 0, 0)
    # spawn_rotation = unreal.Rotator(0, 0, 0)
    new_actor = subsystem.spawn_actor_from_object(uasset.get_asset(), spawn_location)
    return new_actor

def compute_location_within_the_matrix(index, offset_location=unreal.Vector(1000, 1000, 0), count=10):
    y = (index % count) * offset_location.y
    x = int(index / count) * offset_location.x
    return unreal.Vector(x, y, 0)

def load_asset_and_auto_set_location(uasset, previous_pos, spacing=100, only_colliding_bounds=False, keep_above_ground=True):
    dir = unreal.Vector(0, -1, 0)
    up = unreal.Vector(0, 0, 0)
    if keep_above_ground:
        up = unreal.Vector(0, 0, 1)
    new_actor = load_asset_to_current_scene(uasset, previous_pos)
    # unreal.log_warning(f"actor [{new_actor.get_actor_label()}], location = {new_actor.get_actor_location()}")
    if not new_actor: return
    origin, box_extent = new_actor.get_actor_bounds(only_colliding_components=only_colliding_bounds, include_from_child_actors=True)
    axis = unreal.Vector(abs(dir.x), abs(dir.y), abs(dir.z))
    # unreal.log_warning(f"origin = {origin * axis}, bounding = {box_extent}")
    current_edge_pos = origin * (axis+up) - (dir+up) * box_extent
    # unreal.log_warning(f"left_edge = {current_edge_pos.y}")
    new_actor.add_actor_world_offset(-(current_edge_pos-previous_pos), False, False)
    new_pos = previous_pos + dir * box_extent * 2 + dir * spacing
    # unreal.log_warning(f"half-boundingY = {box_extent.y}, spacing = {spacing}, new_pos = {new_pos}")
    return new_actor, new_pos



def tweak_instance_anchor_pos(actor, offset_position):
    # transforms = get_all_components_transforms(actor)
    # target_position = compute_center_position(transforms)
    # if not target_position: return

    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    handles = subsystem.k2_gather_subobject_data_for_instance(actor)
    # if not handles or len(handles)<=2: return   # Exclude actors only have one root component, such as static mesh actors
    root_handle = handles[0]
    scene_root_handle = handles[1]
    scene_root_objdata = subsystem.k2_find_subobject_data_from_handle(scene_root_handle)
    scene_root_obj = lib.get_object(scene_root_objdata)

    for handle in handles[2:]:
        obj_data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = lib.get_object(obj_data)
        print(obj)
        if not isinstance(
            obj, 
            (unreal.StaticMeshComponent, unreal.InstancedStaticMeshComponent)
        ):
            continue
        if hasattr(obj, 'mobility'):
            obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
            # subsystem.reparent_subobject(root_handle, handle)
            params = unreal.ReparentSubobjectParams(
                new_parent_handle = root_handle
            )
            success = subsystem.reparent_subobject(params, handle)
            # obj.set_editor_property("mobility", unreal.ComponentMobility.STATIC)
    
    target_position = scene_root_obj.get_world_location() + offset_position
    scene_root_obj.set_world_transform(unreal.Transform(target_position), False, True)
    
    for handle in handles[2:]:
        obj_data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = lib.get_object(obj_data)
        if not isinstance(
            obj, 
            (unreal.StaticMeshComponent, unreal.InstancedStaticMeshComponent)
        ): 
            continue
        if hasattr(obj, 'mobility'):
            obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
            # subsystem.reparent_subobject(root_handle, handle)
            params = unreal.ReparentSubobjectParams(
                new_parent_handle = scene_root_handle
            )
            success = subsystem.reparent_subobject(params, handle)
            obj.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

    # unreal.EditorLevelLibrary.set_selected_level_actors([actor])

def tweak_instance_anchor_rot(actor, offset_rotation):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lib = unreal.SubobjectDataBlueprintFunctionLibrary

    handles = subsystem.k2_gather_subobject_data_for_instance(actor)
    if not handles or len(handles)<=2: return   # Exclude actors only have one root component, such as static mesh actors
    root_handle = handles[0]
    scene_root_handle = handles[1]
    scene_root_objdata = subsystem.k2_find_subobject_data_from_handle(scene_root_handle)
    scene_root_obj = lib.get_object(scene_root_objdata)

    for handle in handles[2:]:
        obj_data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = lib.get_object(obj_data)
        print(obj)
        if not isinstance(
            obj, 
            (unreal.StaticMeshComponent, unreal.InstancedStaticMeshComponent)
        ):
            continue
        if hasattr(obj, 'mobility'):
            obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
            # subsystem.reparent_subobject(root_handle, handle)
            params = unreal.ReparentSubobjectParams(
                new_parent_handle = root_handle
            )
            success = subsystem.reparent_subobject(params, handle)
            # obj.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

    scene_root_obj.add_world_rotation(offset_rotation, False, True)
    
    for handle in handles[2:]:
        obj_data = subsystem.k2_find_subobject_data_from_handle(handle)
        obj = lib.get_object(obj_data)
        if not isinstance(
            obj, 
            (unreal.StaticMeshComponent, unreal.InstancedStaticMeshComponent)
        ): 
            continue
        if hasattr(obj, 'mobility'):
            obj.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
            # subsystem.reparent_subobject(root_handle, handle)
            params = unreal.ReparentSubobjectParams(
                new_parent_handle = scene_root_handle
            )
            success = subsystem.reparent_subobject(params, handle)
            obj.set_editor_property("mobility", unreal.ComponentMobility.STATIC)



def get_actors_from_data_layers():
    """从所有数据层获取Actor信息"""
    
    # 获取数据层子系统
    data_layer_subsystem = unreal.get_editor_subsystem(unreal.DataLayerSubsystem)
    if not data_layer_subsystem:
        return []
    
    all_actors_info = []
    
    # 获取世界中的所有数据层
    world = unreal.EditorLevelLibrary.get_editor_world()
    data_layers = data_layer_subsystem.get_data_layers(world)
    
    for data_layer in data_layers:
        try:
            # 获取数据层中的Actor
            actors_in_layer = data_layer_subsystem.get_actors_from_data_layer(data_layer)
            for actor in actors_in_layer:
                all_actors_info.append({
                    "actor": actor,
                    "name": actor.get_name(),
                    "data_layer": data_layer.get_name(),
                    "is_loaded": True  # 数据层中的Actor通常是加载的
                })
        except Exception as e:
            unreal.log_warning(f"获取数据层Actor失败: {str(e)}")
    
    print(all_actors_info)

def get_all_level_actors_descs():
    all_actor_descs = unreal.WorldPartitionBlueprintLibrary.get_actor_descs()
    unreal.log_warning(f"总计Actors数量: {len(all_actor_descs)}")
    return all_actor_descs

def get_all_landscape_streaming_proxy_descs():
    all_actor_descs = get_all_level_actors_descs()
    landscape_proxies = []
    for actor_desc in all_actor_descs:
        actor_name = str(actor_desc.label)
        if actor_name.startswith("LandscapeStreamingProxy_"):
            landscape_proxies.append(actor_desc)
    return landscape_proxies

def load_all_landscape_proxies():
    all_actor_descs = unreal.WorldPartitionBlueprintLibrary.get_actor_descs()
    # print(len(all_actor_descs))
    landscape_proxies = []

    for actor_desc in all_actor_descs:
        actor_name = str(actor_desc.label)
        if actor_name.startswith("LandscapeStreamingProxy_"):
            # print(actor_name)
            guid = actor_desc.guid
            landscape_proxies.append(guid)
            # actor.is_spatially_loaded = True
    
    unreal.WorldPartitionBlueprintLibrary.load_actors(landscape_proxies)

def unload_all_landscape_proxies():
    all_actor_descs = unreal.WorldPartitionBlueprintLibrary.get_actor_descs()
    landscape_proxies = []

    for actor_desc in all_actor_descs:
        actor_name = str(actor_desc.label)
        if actor_name.startswith("LandscapeStreamingProxy_"):
            # print(actor_name)
            guid = actor_desc.guid
            landscape_proxies.append(guid)
    
    if len(landscape_proxies)>0:
        unreal.WorldPartitionBlueprintLibrary.unload_actors(landscape_proxies)



def get_clean_float_value(value, tolerance=0.001):
    """清理浮点数，将接近整数的值转换为整数"""
    if abs(value - round(value)) < tolerance:
        return round(value)
    return value

def get_clean_vector(vector, tolerance=0.001):
    """清理Vector中的浮点数"""
    x = get_clean_float_value(vector.x, tolerance)
    y = get_clean_float_value(vector.y, tolerance)
    z = get_clean_float_value(vector.z, tolerance)
    return unreal.Vector(x, y, z)

def get_clean_rotator(rotator, tolerance=0.001):
    """清理Rotator中的浮点数"""
    pitch = get_clean_float_value(rotator.pitch, tolerance)
    roll = get_clean_float_value(rotator.roll, tolerance)
    yaw = get_clean_float_value(rotator.yaw, tolerance)
    return unreal.Rotator(pitch, roll, yaw)

def get_clean_transform(transform, tolerance=0.001):
    """清理Transform中的浮点数"""
    print(f"original transform: {transform.translation, transform.rotation.rotator(), transform.scale3d}")
    cleaned_location = get_clean_vector(transform.translation, tolerance)
    cleaned_rotator = get_clean_rotator(transform.rotation.rotator(), tolerance)
    cleaned_scale = get_clean_vector(transform.scale3d, tolerance)
    print(f"cleaned transform: {cleaned_location, cleaned_rotator, cleaned_scale}")
    return unreal.Transform(cleaned_location, cleaned_rotator, cleaned_scale)

def set_clean_transform(actor):
    root = actor.get_editor_property("root_component")
    transform = get_clean_transform(root.get_relative_transform())
    actor.set_actor_relative_transform(transform, False, False)

# def set_clean_transform(actor, tolerance=0.001):
#     root = actor.get_editor_property("root_component")
#     transform = root.get_relative_transform()
#     print(f"original transform: {transform.translation, transform.rotation.rotator(), transform.scale3d}")
#     cleaned_rotator = get_clean_rotator(transform.rotation.rotator(), tolerance)
#     actor.set_actor_relative_rotation(cleaned_rotator, False, False)
#     cleaned_scale = get_clean_vector(transform.scale3d, tolerance)
#     actor.set_actor_relative_scale3d(cleaned_scale)
#     cleaned_location = get_clean_vector(transform.translation, tolerance)
#     actor.set_actor_relative_location(cleaned_location, False, False)
#     print(f"cleaned transform: {cleaned_location, cleaned_rotator, cleaned_scale}")

