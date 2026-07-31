// Copyright Epic Games, Inc. All Rights Reserved.

#include "ED_BlueSpace_Editor.h"
#include "ED_BlueSpace_EditorCommands.h"
#include "ED_BlueSpace_EditorStyle.h"

#include "EditorUtilitySubsystem.h"
#include "EditorUtilityWidgetBlueprint.h"
#include "ToolMenus.h"
#include "Editor.h"

#define LOCTEXT_NAMESPACE "FED_BlueSpace_EditorModule"

namespace ED_BlueSpace_Editor
{
	static const TCHAR* BlueSpacePanelAssetPath =
		TEXT("/ED_BlueSpace/ToolBase/WBP_BluespacePanel.WBP_BluespacePanel");
}

void FED_BlueSpace_EditorModule::StartupModule()
{
	FED_BlueSpace_EditorStyle::Initialize();
	FED_BlueSpace_EditorStyle::ReloadTextures();

	FED_BlueSpace_EditorCommands::Register();

	PluginCommands = MakeShareable(new FUICommandList);
	PluginCommands->MapAction(
		FED_BlueSpace_EditorCommands::Get().OpenBlueSpacePanel,
		FExecuteAction::CreateRaw(this, &FED_BlueSpace_EditorModule::OpenBlueSpacePanel),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(
		FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FED_BlueSpace_EditorModule::RegisterMenus));
}

void FED_BlueSpace_EditorModule::ShutdownModule()
{
	UToolMenus::UnRegisterStartupCallback(this);
	UToolMenus::UnregisterOwner(this);

	FED_BlueSpace_EditorCommands::Unregister();
	FED_BlueSpace_EditorStyle::Shutdown();
}

void FED_BlueSpace_EditorModule::RegisterMenus()
{
	FToolMenuOwnerScoped OwnerScoped(this);

	UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.User");
	FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("ED_BlueSpace");
	FToolMenuEntry& Entry = Section.AddEntry(
		FToolMenuEntry::InitToolBarButton(FED_BlueSpace_EditorCommands::Get().OpenBlueSpacePanel));
	Entry.SetCommandList(PluginCommands);
}

void FED_BlueSpace_EditorModule::OpenBlueSpacePanel()
{
	UEditorUtilityWidgetBlueprint* WidgetBP = LoadObject<UEditorUtilityWidgetBlueprint>(
		nullptr,
		ED_BlueSpace_Editor::BlueSpacePanelAssetPath);

	if (!WidgetBP)
	{
		UE_LOG(LogTemp, Error, TEXT("ED_BlueSpace: Failed to load EditorUtilityWidget '%s'"),
			ED_BlueSpace_Editor::BlueSpacePanelAssetPath);
		return;
	}

	if (UEditorUtilitySubsystem* EditorUtilitySubsystem = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>())
	{
		EditorUtilitySubsystem->SpawnAndRegisterTab(WidgetBP);
	}
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FED_BlueSpace_EditorModule, ED_BlueSpace_Editor)
