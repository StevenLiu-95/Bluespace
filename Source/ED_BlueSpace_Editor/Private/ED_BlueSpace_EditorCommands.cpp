// Copyright Epic Games, Inc. All Rights Reserved.

#include "ED_BlueSpace_EditorCommands.h"

#define LOCTEXT_NAMESPACE "FED_BlueSpace_EditorCommands"

void FED_BlueSpace_EditorCommands::RegisterCommands()
{
	UI_COMMAND(
		OpenBlueSpacePanel,
		"BlueSpace",
		"Open the BlueSpace editor panel",
		EUserInterfaceActionType::Button,
		FInputChord());
}

#undef LOCTEXT_NAMESPACE
