// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "Framework/Commands/Commands.h"
#include "ED_BlueSpace_EditorStyle.h"

class FED_BlueSpace_EditorCommands : public TCommands<FED_BlueSpace_EditorCommands>
{
public:
	FED_BlueSpace_EditorCommands()
		: TCommands<FED_BlueSpace_EditorCommands>(
			TEXT("ED_BlueSpace_Editor"),
			NSLOCTEXT("Contexts", "ED_BlueSpace_Editor", "ED BlueSpace Editor"),
			NAME_None,
			FED_BlueSpace_EditorStyle::GetStyleSetName())
	{
	}

	virtual void RegisterCommands() override;

	TSharedPtr<FUICommandInfo> OpenBlueSpacePanel;
};
