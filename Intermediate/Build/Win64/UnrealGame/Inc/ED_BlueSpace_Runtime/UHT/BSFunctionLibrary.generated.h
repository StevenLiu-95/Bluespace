// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "BSFunctionLibrary.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class AActor;
class UAnimSequence;
class UMaterialInterface;
class UObject;
class UStaticMesh;
class UTexture;
#ifdef ED_BLUESPACE_RUNTIME_BSFunctionLibrary_generated_h
#error "BSFunctionLibrary.generated.h already included, missing '#pragma once' in BSFunctionLibrary.h"
#endif
#define ED_BLUESPACE_RUNTIME_BSFunctionLibrary_generated_h

#define FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execMultyCaptureAnimSequence); \
	DECLARE_FUNCTION(execCollectReferencedTextures); \
	DECLARE_FUNCTION(execRegexExtract); \
	DECLARE_FUNCTION(execGenerateRandomPolygonFromRectangles); \
	DECLARE_FUNCTION(execTensileAdaptation); \
	DECLARE_FUNCTION(execHelloUE);


#define FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUBSFunctionLibrary(); \
	friend struct Z_Construct_UClass_UBSFunctionLibrary_Statics; \
public: \
	DECLARE_CLASS(UBSFunctionLibrary, UBlueprintFunctionLibrary, COMPILED_IN_FLAGS(0), CASTCLASS_None, TEXT("/Script/ED_BlueSpace_Runtime"), NO_API) \
	DECLARE_SERIALIZER(UBSFunctionLibrary)


#define FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_ENHANCED_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API UBSFunctionLibrary(const FObjectInitializer& ObjectInitializer = FObjectInitializer::Get()); \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	UBSFunctionLibrary(UBSFunctionLibrary&&); \
	UBSFunctionLibrary(const UBSFunctionLibrary&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UBSFunctionLibrary); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UBSFunctionLibrary); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(UBSFunctionLibrary) \
	NO_API virtual ~UBSFunctionLibrary();


#define FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_18_PROLOG
#define FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_INCLASS_NO_PURE_DECLS \
	FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_21_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> ED_BLUESPACE_RUNTIME_API UClass* StaticClass<class UBSFunctionLibrary>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h


PRAGMA_ENABLE_DEPRECATION_WARNINGS
