// Copyright Epic Games, Inc. All Rights Reserved.

#include "ED_BlueSpace_EditorStyle.h"
#include "Framework/Application/SlateApplication.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyleRegistry.h"

TSharedPtr<FSlateStyleSet> FED_BlueSpace_EditorStyle::StyleInstance = nullptr;

void FED_BlueSpace_EditorStyle::Initialize()
{
	if (!StyleInstance.IsValid())
	{
		StyleInstance = Create();
		FSlateStyleRegistry::RegisterSlateStyle(*StyleInstance);
	}
}

void FED_BlueSpace_EditorStyle::Shutdown()
{
	FSlateStyleRegistry::UnRegisterSlateStyle(*StyleInstance);
	ensure(StyleInstance.IsUnique());
	StyleInstance.Reset();
}

FName FED_BlueSpace_EditorStyle::GetStyleSetName()
{
	static FName StyleSetName(TEXT("ED_BlueSpace_EditorStyle"));
	return StyleSetName;
}

void FED_BlueSpace_EditorStyle::ReloadTextures()
{
	if (FSlateApplication::IsInitialized())
	{
		FSlateApplication::Get().GetRenderer()->ReloadTextureResources();
	}
}

#define IMAGE_BRUSH(RelativePath, ...) FSlateImageBrush(Style->RootToContentDir(RelativePath, TEXT(".png")), __VA_ARGS__)

const FVector2D Icon40x40(40.0f, 40.0f);
const FVector2D Icon20x20(20.0f, 20.0f);

TSharedRef<FSlateStyleSet> FED_BlueSpace_EditorStyle::Create()
{
	TSharedRef<FSlateStyleSet> Style = MakeShareable(new FSlateStyleSet(GetStyleSetName()));

	const TSharedPtr<IPlugin> Plugin = IPluginManager::Get().FindPlugin(TEXT("ED_BlueSpace"));
	check(Plugin.IsValid());
	Style->SetContentRoot(Plugin->GetBaseDir() / TEXT("Resources"));

	Style->Set("ED_BlueSpace_Editor.OpenBlueSpacePanel", new IMAGE_BRUSH(TEXT("Icon128"), Icon40x40));
	Style->Set("ED_BlueSpace_Editor.OpenBlueSpacePanel.Small", new IMAGE_BRUSH(TEXT("Icon128"), Icon20x20));

	return Style;
}

#undef IMAGE_BRUSH
