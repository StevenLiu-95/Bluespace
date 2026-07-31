import unreal
#from utils.unreal_globals import UnrealGlobals as ug
#from SMtoISM.ClearMergedISM import clear_merged_ism
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

def clear_merged_ism():
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

world = ug.get_editor_world()
BP_ISM_C = ug.EAL.load_blueprint_class("/Game/Tools/HISM/BP_ISM")

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

    # 查找根节点（带路径压缩）
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    # 合并两个集合
    def union(self, x, y):
        if box_min_distance(self.actors[x], self.actors[y]) > self.max_distance:
            return  # 距离太远

        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return  # 已在同一集合

        # 计算合并后集合的新边界
        minpos_x, maxpos_x = self.minpos[root_x], self.maxpos[root_x]
        minpos_y, maxpos_y = self.minpos[root_y], self.maxpos[root_y]
        minpos = tuple(min(minpos_x[i], minpos_y[i]) for i in range(3))
        maxpos = tuple(max(maxpos_x[i], maxpos_y[i]) for i in range(3))

        nx = self.num[root_x]
        ny = self.num[root_y]
        avg_size = tuple((self.avg_size[root_x][i] * nx + self.avg_size[root_y][i] * ny) / (nx + ny) for i in range(3))

        # 如果新边界超出限制条件，不合并集合
        if any(maxpos[i] - minpos[i] > avg_size[i] * self.max_bound_limit for i in range(3)):
            return

        # 按秩合并：将小树合并到大树下
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.minpos[root_y] = minpos
            self.maxpos[root_y] = maxpos
            self.avg_size[root_y] = avg_size
        else:
            self.parent[root_y] = root_x
            self.minpos[root_x] = minpos
            self.maxpos[root_x] = maxpos
            self.avg_size[root_x] = avg_size
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1

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

def box_min_distance(actor1, actor2):
    """
    计算两个三维 AABB Box 之间的最小距离（如果相交则返回 0）
    :param origin1: Box1 的中心坐标 (x1, y1, z1)
    :param extent1: Box1 的半边长 (dx1, dy1, dz1)
    :param origin2: Box2 的中心坐标 (x2, y2, z2)
    :param extent2: Box2 的半边长 (dx2, dy2, dz2)
    :return: 最小距离（>= 0）
    """
    # 计算每个轴上的间隔（如果为负则表示重叠，间隔视为 0）
    origin1, extent1 = actor1.get_actor_bounds(False)
    origin2, extent2 = actor2.get_actor_bounds(False)

    dx_sep = max(abs(origin1.x - origin2.x) - (extent1.x + extent2.x), 0)
    dy_sep = max(abs(origin1.y - origin2.y) - (extent1.y + extent2.y), 0)
    dz_sep = max(abs(origin1.z - origin2.z) - (extent1.z + extent2.z), 0)

    # 计算欧几里得距离
    dis = math.sqrt(dx_sep**2 + dy_sep**2 + dz_sep**2)

    # 计算盒子的半对角线长度
    diag_length1 = math.sqrt(extent1.x**2 + extent1.y**2 + extent1.z**2)
    diag_length2 = math.sqrt(extent2.x**2 + extent2.y**2 + extent2.z**2)

    # 返回最小距离和盒子半边对角线长度和的比值
    return dis / max((diag_length1 + diag_length2),0.00001)

def cast(object_to_cast, object_class):
    try:
        return object_class.cast(object_to_cast)
    except:
        return None


# 获取 StaticMeshActor 分组 key，便于扩展参数
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
    group_tag_list = [str(tag.get_editor_property("tag_name")) for tag in sm_actor.actor_group_tags.gameplay_tags]
    group_tag_tuple = tuple(group_tag_list)
    
    return (mesh_path, material_paths, collision_preset, cast_shadow, receives_decals, visible_in_ray_tracing, is_shadow_behavior_static, has_tag_ForbiddingActivityVolume, group_tag_tuple)

def keep_highest_importance_tag(group_tags_set):
    tag_importance_map = {"Art.Importance.1_Hero": 1,
                          "Art.Importance.2_Main": 2,
                          "Art.Importance.3_Secondary": 3,
                          "Art.Importance.4_Decoration": 4,
                          "Art.Importance.5_Ignorable": 5}
                          
    new_group_tags_set = set()
    min_importance_value = 999
    current_importance_tag = None

    for tag in list(group_tags_set):
        name = str(tag.get_editor_property("tag_name"))
        if name.endswith(".bot"):
            name = name[:-4]
        if name in tag_importance_map:
            if tag_importance_map[name] < min_importance_value:
                min_importance_value = tag_importance_map[name]
                current_importance_tag = tag
        else:
            new_group_tags_set.add(tag)
    if current_importance_tag:
        new_group_tags_set.add(current_importance_tag)

    return new_group_tags_set

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
    if sm_component.hidden_in_game or sm_component.has_component_vertex_color():
        return False
    if sm_component.get_collision_profile_name() == "Custom":
        return False
    if len(sm_component.get_editor_property("custom_primitive_data").get_editor_property("data")) > 0:
        return False
    return True


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
    group_tag_tuple = group_key[8]

    # 获取组内第一个 actor 的位置，生成 ISM actor
    first_actor = actors[0]
    pos = first_actor.get_actor_location()
    mesh = ug.EAL.load_asset(mesh_path)
    label = "ISM_" + mesh_path.split(".")[-1]

    # 对 ISM actor 进行参数设置
    ism = ug.ELL.spawn_actor_from_class(BP_ISM_C, pos)
    ism.set_folder_path("ISM_ToolMerged")
    ism.set_actor_label(label)
    ism.tags.append("ISM_ToolMerged")
    if has_tag_ForbiddingActivityVolume:
        ism.tags.append("ForbiddingActivityVolume")
    ism.actor_group_tags = first_actor.actor_group_tags
    
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


def SMtoISM(actors):
    # 按分组 key 分类 StaticMeshActor
    group_dict = dict()
    for actor in actors:
        sma = cast(actor, unreal.StaticMeshActor)
        if sma and is_valid_to_merge(sma):
            key = get_sma_group_key(sma)
            if key not in group_dict:
                group_dict[key] = []
            group_dict[key].append(sma)


    # 处理每个分组
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

    #EAS.destroy_actors(actors_merged)
    #EAS.set_selected_level_actors(ism_list)

'''
if not ug.current_level_is_persistent():
    unreal.log_error("当前激活关卡不是持久化关卡，无法执行 SMtoISM 操作！")
else:
    clear_merged_ism()
    SMtoISM(ug.EAS.get_all_level_actors())
'''