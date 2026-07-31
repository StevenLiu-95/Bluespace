import unreal
import math

class ug:
    """共享的 Unreal Python 工具和子系统引用"""
    
    # 编辑器子系统
    EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    EAL = unreal.EditorAssetLibrary
    ELL = unreal.EditorLevelLibrary
    USL = unreal.SystemLibrary
    UGS = unreal.GameplayStatics
    UES = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    
    @classmethod
    def get_editor_world(cls):
        """获取当前编辑器世界（动态获取，避免缓存问题）"""
        return cls.UES.get_editor_world() if cls.UES else None

    @classmethod
    def get_current_level(cls):
        """获取当前激活的关卡"""
        return cls.LES.get_current_level() if cls.LES else None

    @classmethod
    def log(cls, message):
        """带前缀的统一日志"""
        unreal.log(f"[Utils] {message}")

    @classmethod
    def is_persistent_level(cls, actor):
        """检查给定的 actor 是否在持久化关卡中"""
        if not actor:
            return False
        level = actor.get_level()
        if not level:
            return False

        world_path = cls.get_editor_world().get_path_name()
        level_path = level.get_path_name().split(':')[0]
        return level_path == world_path

    @classmethod
    def current_level_is_persistent(cls):
        world_path = cls.get_editor_world().get_path_name()
        level_path = cls.get_current_level().get_path_name().split(':')[0]
        return level_path == world_path


world = ug.get_editor_world()
BP_ISM = ug.EAL.load_blueprint_class("/ED_BlueSpace/Scripts/Python/SMtoISM/BP_ISM")

class UnionFind_BoundLimit:
    def __init__(self, actors, max_distance, max_bound_limit):
        self.actors = actors
        self.max_distance = max_distance
        self.max_bound_limit = max_bound_limit

        n = len(actors)
        self.parent = list(range(n))  # 初始化每个点的父节点为自己
        self.rank = [0] * n          # 初始化秩（用于优化）
        self.num = [1] * n  # 每个集合的大小

        self.minpos = []
        self.maxpos = []
        self.avg_size = []
        for actor in actors:
            origin, extent = actor.get_actor_bounds(False)
            self.minpos.append((origin.x - extent.x, origin.y - extent.y, origin.z - extent.z))
            self.maxpos.append((origin.x + extent.x, origin.y + extent.y, origin.z + extent.z))
            self.avg_size.append((extent.x * 2, extent.y * 2, extent.z * 2))

def cluster_boxes(actors, max_distance, max_bound_limit):
    n = len(actors)
    uf = UnionFind_BoundLimit(actors, max_distance, max_bound_limit)
    for i in range(n):
        for j in range(i + 1, n):
            uf.union(i, j)

    # 将同一集合的点索引分组
    groups = {}
    for idx in range(n):
        root = uf.find(idx)
        if root not in groups:
            groups[root] = []
        groups[root].append(idx)
    
    return list(groups.values())

def cast(object_to_cast, object_class):
    try:
        return object_class.cast(object_to_cast)
    except:
        return None

def get_sma_group_key(sm_actor):
    sm_component = sm_actor.static_mesh_component
    sm_asset = sm_component.static_mesh

    # 可扩展的参数列表
    mesh_path = ug.USL.get_path_name(sm_asset)
    material_paths = tuple(
        ug.USL.get_path_name(sm_component.get_material(i))
        for i in range(len(sm_asset.static_materials))
    )
    collision_preset = sm_component.get_collision_profile_name()
    cast_shadow = sm_component.cast_shadow
    receives_decals = sm_component.receives_decals
    visible_in_ray_tracing = sm_component.visible_in_ray_tracing
    is_shadow_behavior_static = sm_component.shadow_cache_invalidation_behavior == 3
    has_tag_ForbiddingActivityVolume = "ForbiddingActivityVolume" in sm_actor.tags
    #group_tag_list = [str(tag.get_editor_property("tag_name")) for tag in sm_actor.actor_group_tags.gameplay_tags]
    #group_tag_tuple = tuple(group_tag_list)
    
    return (mesh_path, material_paths, collision_preset, cast_shadow, receives_decals, visible_in_ray_tracing, is_shadow_behavior_static, has_tag_ForbiddingActivityVolume )

def is_positive_scale(actor):
    scale = actor.get_actor_scale3d()
    return scale.x * scale.y * scale.z > 0

def is_valid_to_merge(sm_actor):
    if sm_actor.get_editor_property("is_editor_only_actor") or sm_actor.hidden:
        return False
    if not is_positive_scale(sm_actor) or not ug.is_persistent_level(sm_actor):
        return False
    for tag in sm_actor.tags:
        if tag == "ISM_ignore" or tag == "ISM_Ignore":
            return False
    
    sm_component = sm_actor.static_mesh_component
    if not sm_component.static_mesh or not sm_component.visible:
        return False
    if sm_component.hidden_in_game: #or sm_component.has_component_vertex_color():
        return False
    if sm_component.get_collision_profile_name() == "Custom":
        return False
    if len(sm_component.get_editor_property("custom_primitive_data").get_editor_property("data")) > 0:
        return False
    return True

def Select_Mesh_Actor():
    actors = ug.ELL.get_all_level_actors()
    selected = []
    group_dict = dict()

    for actor in actors:
        sma = cast(actor, unreal.StaticMeshActor)
        if sma and is_valid_to_merge(sma):
            key = get_sma_group_key(sma)
            if key not in group_dict:
                group_dict[key] = []
            group_dict[key].append(sma)
    
    for group_key, actors in group_dict.items():
        if len(actors) < 2:
            continue
        selected.extend(actors)
    # Replace the current selection with the valid static mesh actors
    ug.ELL.set_selected_level_actors(selected)

def Clear_Merged_Ism():
    """
    Clear all merged ISM actors and reset editor-only actors.
    This function removes all ISM actors tagged with 'ISM_ToolMerged'
    and resets the 'ISM_EditorOnly' tag on actors in the persistent level.
    """
    
    world = ug.get_editor_world()

    actors = ug.UGS.get_all_actors_with_tag(world, "ISM_EditorOnly")
    for actor in actors:
        if ug.is_persistent_level(actor):
            actor.set_editor_property("is_editor_only_actor", False)
            actor.tags.remove("ISM_EditorOnly")

    isms = ug.UGS.get_all_actors_with_tag(world, "ISM_ToolMerged")
    isms_to_delete = []
    for ism in isms:
        if ug.is_persistent_level(ism):
            isms_to_delete.append(ism)
    ug.EAS.destroy_actors(isms_to_delete)

def merge_ISM(group_key, actors):
    if not group_key or not actors:
        return
    
    # 从 group_key 中获取参数
    mesh_path = group_key[0]
    material_paths = group_key[1]
    collision_preset = group_key[2]
    cast_shadow = group_key[3]
    receives_decals = group_key[4]
    visible_in_ray_tracing = group_key[5]
    is_shadow_behavior_static = group_key[6]
    has_tag_ForbiddingActivityVolume = group_key[7]
    #group_tag_tuple = group_key[8]

    # 获取组内第一个 actor 的位置，生成 ISM actor
    first_actor = actors[0]
    pos = first_actor.get_actor_location()
    mesh = ug.EAL.load_asset(mesh_path)
    label = "ISM_" + mesh_path.split(".")[-1]

    # 对 ISM actor 进行参数设置
    ism = ug.ELL.spawn_actor_from_class(BP_ISM, pos)
    ism.set_folder_path("ISM_ToolMerged")
    ism.set_actor_label(label)
    ism.tags.append("ISM_ToolMerged")
    if has_tag_ForbiddingActivityVolume:
        ism.tags.append("ForbiddingActivityVolume")
    #ism.actor_group_tags = first_actor.actor_group_tags
    
    ismc = ism.get_component_by_class(unreal.InstancedStaticMeshComponent)
    ismc.set_static_mesh(mesh)
    ismc.set_collision_profile_name(collision_preset)
    ismc.set_cast_shadow(cast_shadow)
    ismc.set_receives_decals(receives_decals)
    ismc.set_visible_in_ray_tracing(visible_in_ray_tracing)
    if is_shadow_behavior_static:
        ismc.set_shadow_cache_invalidation_behavior(unreal.ShadowCacheInvalidationBehavior.STATIC)

    for i, path in enumerate(material_paths):
        material = ug.EAL.load_asset(path)
        if material:
            ismc.set_material(i, material)

    # 为 ISM component 添加 instances
    soft_path_array = []
    
    for actor in actors:
        ismc.add_instance(actor.get_actor_transform(), world_space=True)
        actor.set_editor_property("is_editor_only_actor", True)
        actor.tags.append("ISM_EditorOnly")
        soft_path_array.append(actor)
    
    ism.set_editor_property("InstanceActorMap", soft_path_array)

    unreal.log(f"Merged {len(actors)} actors into ISM: {ism.get_actor_label()}")


def Merge_Selected_ISM():
    """合并选中的实例化静态网格体（ISM）组件"""
    selected_actors = ug.ELL.get_selected_level_actors()
    if not selected_actors:
        unreal.log("No actors selected for ISM merging.")
        return
    unreal.log(f"Selected {len(selected_actors)} actors for ISM merging.")
    group_dict = dict()
    
    for actor in selected_actors:
        sma = cast(actor, unreal.StaticMeshActor)
        if sma and is_valid_to_merge(sma):
            key = get_sma_group_key(sma)
            if key not in group_dict:
                group_dict[key] = []
            group_dict[key].append(sma)
    unreal.log(f"Found {len(group_dict)} groups for ISM merging.")
    
    for group_key, actors in group_dict.items():
        min_group_size = 2
        USE_CLUSTER = False
        if USE_CLUSTER:
            max_dist = 1
            max_bound_limit = 10.0
            clusters = cluster_boxes(actors, max_dist, max_bound_limit)
            for i, group in enumerate(clusters):
                if len(group) < min_group_size:
                    continue
                group_actors = [actors[idx] for idx in group]
                merge_ISM(group_key, group_actors)
        else:
            if len(actors) < min_group_size:
                continue
            merge_ISM(group_key, actors)
    