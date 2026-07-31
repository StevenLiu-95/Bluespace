// Copyright Epic Games, Inc. All Rights Reserved.

#include "ED_BlueSpace_Runtime.h"

#define LOCTEXT_NAMESPACE "FED_BlueSpace_RuntimeModule"

void FED_BlueSpace_RuntimeModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
}

void FED_BlueSpace_RuntimeModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FED_BlueSpace_RuntimeModule, ED_BlueSpace_Runtime)