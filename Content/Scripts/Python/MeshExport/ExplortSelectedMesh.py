import unreal
import csv
import os
import sys


def export_selected_meshes(export_dir=None, name_prefix=None):
    
    xml_name="PointCloudData"
    
    # 读取选择
    targetActors = unreal.EditorLevelLibrary.get_selected_level_actors()

    if len(export_dir.strip()) == 0:
        export_dir = unreal.Paths.project_dir() + "Plugins/ED_BlueSpace/Content/Scripts/Python/MeshExport/Meshes"

    if name_prefix and len(name_prefix.strip()) > 0:
        xmlName = name_prefix
    else:
        xmlName = xml_name

    # 配置导出选项
    fbxExporter = unreal.StaticMeshExporterFBX()
    fbxOption = unreal.FbxExportOption()
    fbxOption.export_morph_targets = False
    fbxOption.export_preview_mesh = False
    fbxOption.level_of_detail = False
    fbxOption.collision = False
    fbxOption.export_local_time = False
    fbxOption.ascii = False
    fbxOption.vertex_color = True

    # 确保导出目录存在
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)

    # 导出坐标表
    csvPath = os.path.join(export_dir, xmlName + '.csv')
    if os.path.isfile(csvPath):
        os.remove(csvPath)

    firstRow = ['actorName', 'meshName', 'locationx', 'locationy', 'locationz', 'rotationx', 'rotationy', 'rotationz', 'scalex', 'scaley', 'scalez']

    rows = []
    for targetActor in targetActors:
        actorLocation = targetActor.get_actor_location()
        actorRotation = targetActor.get_actor_rotation()
        actorScale = targetActor.get_actor_scale3d()
        actorName = targetActor.get_name()
        comp = targetActor.get_component_by_class(unreal.StaticMeshComponent)
        if comp is not None and comp.get_editor_property('static_mesh') is not None:
            mesh = comp.get_editor_property('static_mesh')
            meshName = mesh.get_name()

        locationX = actorLocation.get_editor_property('x')/100
        locationY = actorLocation.get_editor_property('y')/100
        locationZ = actorLocation.get_editor_property('z')/100
        rotationX = actorRotation.get_editor_property('roll')
        rotationY = actorRotation.get_editor_property('pitch')
        rotationZ = actorRotation.get_editor_property('yaw')
        scaleX = actorScale.get_editor_property('x')
        scaleY = actorScale.get_editor_property('y')
        scaleZ = actorScale.get_editor_property('z')
        rows.append([actorName, meshName, locationX, locationY, locationZ, rotationX, rotationY, rotationZ, scaleX, scaleY, scaleZ])

    with open(csvPath, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(firstRow)
        csvWriter.writerows(rows)

    # 导出模型
    exported_files = []
    for targetActor in targetActors:
        comp = targetActor.get_component_by_class(unreal.StaticMeshComponent)
        if comp is None:
            continue
        static_mesh = comp.get_editor_property('static_mesh')
        if static_mesh is None:
            continue
        targetMeshPath = static_mesh.get_path_name()
        targetMesh = unreal.load_asset(targetMeshPath)
        targetMeshName = targetMesh.get_name()
        file_name = f"{targetMeshName}.fbx"
        exportPath = os.path.join(export_dir, file_name)

        task = unreal.AssetExportTask()
        task.set_editor_property("object", targetMesh)
        task.set_editor_property("filename", exportPath)
        task.set_editor_property("exporter", fbxExporter)
        task.set_editor_property("automated", True)
        task.set_editor_property("prompt", False)
        task.set_editor_property("options", fbxOption)

        success = unreal.Exporter.run_asset_export_task(task)
        if success:
            exported_files.append(exportPath)

    unreal.log(f"Exported {len(exported_files)} meshes to {export_dir}")
    return exported_files