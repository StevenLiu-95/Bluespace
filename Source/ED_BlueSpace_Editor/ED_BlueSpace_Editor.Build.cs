// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class ED_BlueSpace_Editor : ModuleRules
{
	public ED_BlueSpace_Editor(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"ED_BlueSpace_Runtime",
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"CoreUObject",
				"Engine",
				"Slate",
				"SlateCore",
				"InputCore",
				"UnrealEd",
				"ToolMenus",
				"EditorSubsystem",
				"Blutility",
				"UMG",
				"UMGEditor",
				"Projects",
			}
		);
	}
}
