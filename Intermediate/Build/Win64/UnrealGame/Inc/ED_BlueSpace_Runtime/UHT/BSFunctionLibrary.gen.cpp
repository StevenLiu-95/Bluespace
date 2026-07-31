// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "ED_BlueSpace/Public/BSFunctionLibrary.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBSFunctionLibrary() {}

// Begin Cross Module References
COREUOBJECT_API UClass* Z_Construct_UClass_UObject_NoRegister();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FVector();
ED_BLUESPACE_RUNTIME_API UClass* Z_Construct_UClass_UBSFunctionLibrary();
ED_BLUESPACE_RUNTIME_API UClass* Z_Construct_UClass_UBSFunctionLibrary_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_AActor_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UAnimSequence_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UBlueprintFunctionLibrary();
ENGINE_API UClass* Z_Construct_UClass_UMaterialInterface_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UStaticMesh_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UTexture_NoRegister();
UPackage* Z_Construct_UPackage__Script_ED_BlueSpace_Runtime();
// End Cross Module References

// Begin Class UBSFunctionLibrary Function CollectReferencedTextures
struct Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics
{
	struct BSFunctionLibrary_eventCollectReferencedTextures_Parms
	{
		const UObject* WorldContextObject;
		TArray<AActor*> Actors;
		TArray<UTexture*> ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "AutoCreateRefTerm", "Actors" },
		{ "Category", "Bluespacer|Asset" },
		{ "Comment", "// Collect texture assets referenced by Actors.\n// If Actors is empty, iterate all actors in the current world; otherwise only the given list.\n" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
		{ "ToolTip", "Collect texture assets referenced by Actors.\nIf Actors is empty, iterate all actors in the current world; otherwise only the given list." },
		{ "WorldContext", "WorldContextObject" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_WorldContextObject_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Actors_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_WorldContextObject;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Actors_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_Actors;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_ReturnValue_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_WorldContextObject = { "WorldContextObject", nullptr, (EPropertyFlags)0x0010000000000082, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventCollectReferencedTextures_Parms, WorldContextObject), Z_Construct_UClass_UObject_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_WorldContextObject_MetaData), NewProp_WorldContextObject_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_Actors_Inner = { "Actors", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UClass_AActor_NoRegister, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_Actors = { "Actors", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventCollectReferencedTextures_Parms, Actors), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Actors_MetaData), NewProp_Actors_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_ReturnValue_Inner = { "ReturnValue", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UClass_UTexture_NoRegister, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventCollectReferencedTextures_Parms, ReturnValue), EArrayPropertyFlags::None, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_WorldContextObject,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_Actors_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_Actors,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_ReturnValue_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "CollectReferencedTextures", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::BSFunctionLibrary_eventCollectReferencedTextures_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::BSFunctionLibrary_eventCollectReferencedTextures_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execCollectReferencedTextures)
{
	P_GET_OBJECT(UObject,Z_Param_WorldContextObject);
	P_GET_TARRAY_REF(AActor*,Z_Param_Out_Actors);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(TArray<UTexture*>*)Z_Param__Result=UBSFunctionLibrary::CollectReferencedTextures(Z_Param_WorldContextObject,Z_Param_Out_Actors);
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function CollectReferencedTextures

// Begin Class UBSFunctionLibrary Function GenerateRandomPolygonFromRectangles
struct Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics
{
	struct BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms
	{
		float MinSize;
		float MaxSize;
		int32 Iterations;
		int32 Seed;
		TArray<FVector> ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Bluespacer|Geometry" },
		{ "Comment", "// Merge random rectangles into a polygon outline; returns clockwise vertices (FVector, Z=0).\n" },
		{ "CPP_Default_Seed", "0" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
		{ "ToolTip", "Merge random rectangles into a polygon outline; returns clockwise vertices (FVector, Z=0)." },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_MinSize;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_MaxSize;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Iterations;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Seed;
	static const UECodeGen_Private::FStructPropertyParams NewProp_ReturnValue_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_MinSize = { "MinSize", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms, MinSize), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_MaxSize = { "MaxSize", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms, MaxSize), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_Iterations = { "Iterations", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms, Iterations), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_Seed = { "Seed", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms, Seed), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_ReturnValue_Inner = { "ReturnValue", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FVector, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms, ReturnValue), EArrayPropertyFlags::None, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_MinSize,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_MaxSize,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_Iterations,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_Seed,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_ReturnValue_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "GenerateRandomPolygonFromRectangles", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04022401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::BSFunctionLibrary_eventGenerateRandomPolygonFromRectangles_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execGenerateRandomPolygonFromRectangles)
{
	P_GET_PROPERTY(FFloatProperty,Z_Param_MinSize);
	P_GET_PROPERTY(FFloatProperty,Z_Param_MaxSize);
	P_GET_PROPERTY(FIntProperty,Z_Param_Iterations);
	P_GET_PROPERTY(FIntProperty,Z_Param_Seed);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(TArray<FVector>*)Z_Param__Result=UBSFunctionLibrary::GenerateRandomPolygonFromRectangles(Z_Param_MinSize,Z_Param_MaxSize,Z_Param_Iterations,Z_Param_Seed);
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function GenerateRandomPolygonFromRectangles

// Begin Class UBSFunctionLibrary Function HelloUE
struct Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics
{
	struct BSFunctionLibrary_eventHelloUE_Parms
	{
		FString ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Bluespacer|Base" },
		{ "Comment", "// Returns fixed string: Hello, UE!\n" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
		{ "ToolTip", "Returns fixed string: Hello, UE!" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FStrPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FStrPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventHelloUE_Parms, ReturnValue), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "HelloUE", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::BSFunctionLibrary_eventHelloUE_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x14022401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::BSFunctionLibrary_eventHelloUE_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_HelloUE()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_HelloUE_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execHelloUE)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	*(FString*)Z_Param__Result=UBSFunctionLibrary::HelloUE();
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function HelloUE

// Begin Class UBSFunctionLibrary Function MultyCaptureAnimSequence
struct Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics
{
	struct BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms
	{
		TArray<UAnimSequence*> Animations;
		TArray<float> Frames;
		FString Path;
		float RemeshPercentage;
		UMaterialInterface* Material;
		bool GenerateLOD;
		TArray<UStaticMesh*> ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "AutoCreateRefTerm", "Animations,Frames" },
		{ "Category", "Bluespacer|Animation" },
		{ "Comment", "/**\n     * Batch-bake AnimSequence frames into StaticMesh assets (editor-only).\n     * RemeshPercentage: percent of triangles to keep (100 = no remesh, 50 = keep ~50% tris, 0 = reduce to minimum).\n     * GenerateLOD: when true, auto-generate LOD levels.\n     */" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
		{ "ToolTip", "Batch-bake AnimSequence frames into StaticMesh assets (editor-only).\nRemeshPercentage: percent of triangles to keep (100 = no remesh, 50 = keep ~50% tris, 0 = reduce to minimum).\nGenerateLOD: when true, auto-generate LOD levels." },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Animations_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Frames_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Path_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Animations_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_Animations;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_Frames_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_Frames;
	static const UECodeGen_Private::FStrPropertyParams NewProp_Path;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_RemeshPercentage;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Material;
	static void NewProp_GenerateLOD_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_GenerateLOD;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_ReturnValue_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Animations_Inner = { "Animations", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UClass_UAnimSequence_NoRegister, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Animations = { "Animations", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, Animations), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Animations_MetaData), NewProp_Animations_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Frames_Inner = { "Frames", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Frames = { "Frames", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, Frames), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Frames_MetaData), NewProp_Frames_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Path = { "Path", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, Path), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Path_MetaData), NewProp_Path_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_RemeshPercentage = { "RemeshPercentage", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, RemeshPercentage), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Material = { "Material", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, Material), Z_Construct_UClass_UMaterialInterface_NoRegister, METADATA_PARAMS(0, nullptr) };
void Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_GenerateLOD_SetBit(void* Obj)
{
	((BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms*)Obj)->GenerateLOD = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_GenerateLOD = { "GenerateLOD", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms), &Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_GenerateLOD_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_ReturnValue_Inner = { "ReturnValue", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UClass_UStaticMesh_NoRegister, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms, ReturnValue), EArrayPropertyFlags::None, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Animations_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Animations,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Frames_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Frames,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Path,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_RemeshPercentage,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_Material,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_GenerateLOD,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_ReturnValue_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "MultyCaptureAnimSequence", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::BSFunctionLibrary_eventMultyCaptureAnimSequence_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execMultyCaptureAnimSequence)
{
	P_GET_TARRAY_REF(UAnimSequence*,Z_Param_Out_Animations);
	P_GET_TARRAY_REF(float,Z_Param_Out_Frames);
	P_GET_PROPERTY(FStrProperty,Z_Param_Path);
	P_GET_PROPERTY(FFloatProperty,Z_Param_RemeshPercentage);
	P_GET_OBJECT(UMaterialInterface,Z_Param_Material);
	P_GET_UBOOL(Z_Param_GenerateLOD);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(TArray<UStaticMesh*>*)Z_Param__Result=UBSFunctionLibrary::MultyCaptureAnimSequence(Z_Param_Out_Animations,Z_Param_Out_Frames,Z_Param_Path,Z_Param_RemeshPercentage,Z_Param_Material,Z_Param_GenerateLOD);
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function MultyCaptureAnimSequence

// Begin Class UBSFunctionLibrary Function RegexExtract
struct Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics
{
	struct BSFunctionLibrary_eventRegexExtract_Parms
	{
		FString Input;
		FString Pattern;
		TArray<FString> OutMatches;
		bool bAllMatches;
		int32 CaptureGroup;
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Bluespacer|String" },
		{ "Comment", "// Extract fields from a string with regex.\n// Pattern: regex pattern, capture groups supported.\n// OutMatches: matched results in order.\n// bAllMatches: true = all matches of the capture group; false = first match only.\n// CaptureGroup: capture group index to return; 0 = whole match.\n" },
		{ "CPP_Default_bAllMatches", "true" },
		{ "CPP_Default_CaptureGroup", "1" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
		{ "ToolTip", "Extract fields from a string with regex.\nPattern: regex pattern, capture groups supported.\nOutMatches: matched results in order.\nbAllMatches: true = all matches of the capture group; false = first match only.\nCaptureGroup: capture group index to return; 0 = whole match." },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Input_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Pattern_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FStrPropertyParams NewProp_Input;
	static const UECodeGen_Private::FStrPropertyParams NewProp_Pattern;
	static const UECodeGen_Private::FStrPropertyParams NewProp_OutMatches_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_OutMatches;
	static void NewProp_bAllMatches_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAllMatches;
	static const UECodeGen_Private::FIntPropertyParams NewProp_CaptureGroup;
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FStrPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_Input = { "Input", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventRegexExtract_Parms, Input), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Input_MetaData), NewProp_Input_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_Pattern = { "Pattern", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventRegexExtract_Parms, Pattern), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Pattern_MetaData), NewProp_Pattern_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_OutMatches_Inner = { "OutMatches", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_OutMatches = { "OutMatches", nullptr, (EPropertyFlags)0x0010000000000180, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventRegexExtract_Parms, OutMatches), EArrayPropertyFlags::None, METADATA_PARAMS(0, nullptr) };
void Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_bAllMatches_SetBit(void* Obj)
{
	((BSFunctionLibrary_eventRegexExtract_Parms*)Obj)->bAllMatches = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_bAllMatches = { "bAllMatches", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(BSFunctionLibrary_eventRegexExtract_Parms), &Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_bAllMatches_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_CaptureGroup = { "CaptureGroup", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventRegexExtract_Parms, CaptureGroup), METADATA_PARAMS(0, nullptr) };
void Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((BSFunctionLibrary_eventRegexExtract_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(BSFunctionLibrary_eventRegexExtract_Parms), &Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_Input,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_Pattern,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_OutMatches_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_OutMatches,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_bAllMatches,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_CaptureGroup,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "RegexExtract", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::BSFunctionLibrary_eventRegexExtract_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::BSFunctionLibrary_eventRegexExtract_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execRegexExtract)
{
	P_GET_PROPERTY(FStrProperty,Z_Param_Input);
	P_GET_PROPERTY(FStrProperty,Z_Param_Pattern);
	P_GET_TARRAY_REF(FString,Z_Param_Out_OutMatches);
	P_GET_UBOOL(Z_Param_bAllMatches);
	P_GET_PROPERTY(FIntProperty,Z_Param_CaptureGroup);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=UBSFunctionLibrary::RegexExtract(Z_Param_Input,Z_Param_Pattern,Z_Param_Out_OutMatches,Z_Param_bAllMatches,Z_Param_CaptureGroup);
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function RegexExtract

// Begin Class UBSFunctionLibrary Function TensileAdaptation
struct Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics
{
	struct BSFunctionLibrary_eventTensileAdaptation_Parms
	{
		float Whole;
		float Unit;
		float Long;
		int32 Count;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Bluespacer|Base" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FFloatPropertyParams NewProp_Whole;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_Unit;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_Long;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Count;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Whole = { "Whole", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventTensileAdaptation_Parms, Whole), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Unit = { "Unit", nullptr, (EPropertyFlags)0x0010000000000080, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventTensileAdaptation_Parms, Unit), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Long = { "Long", nullptr, (EPropertyFlags)0x0010000000000180, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventTensileAdaptation_Parms, Long), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Count = { "Count", nullptr, (EPropertyFlags)0x0010000000000180, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(BSFunctionLibrary_eventTensileAdaptation_Parms, Count), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Whole,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Unit,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Long,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::NewProp_Count,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::PropPointers) < 2048);
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::FuncParams = { (UObject*(*)())Z_Construct_UClass_UBSFunctionLibrary, nullptr, "TensileAdaptation", nullptr, nullptr, Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::PropPointers, UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::PropPointers), sizeof(Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::BSFunctionLibrary_eventTensileAdaptation_Parms), RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x14422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::Function_MetaDataParams) };
static_assert(sizeof(Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::BSFunctionLibrary_eventTensileAdaptation_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBSFunctionLibrary::execTensileAdaptation)
{
	P_GET_PROPERTY(FFloatProperty,Z_Param_Whole);
	P_GET_PROPERTY(FFloatProperty,Z_Param_Unit);
	P_GET_PROPERTY_REF(FFloatProperty,Z_Param_Out_Long);
	P_GET_PROPERTY_REF(FIntProperty,Z_Param_Out_Count);
	P_FINISH;
	P_NATIVE_BEGIN;
	UBSFunctionLibrary::TensileAdaptation(Z_Param_Whole,Z_Param_Unit,Z_Param_Out_Long,Z_Param_Out_Count);
	P_NATIVE_END;
}
// End Class UBSFunctionLibrary Function TensileAdaptation

// Begin Class UBSFunctionLibrary
void UBSFunctionLibrary::StaticRegisterNativesUBSFunctionLibrary()
{
	UClass* Class = UBSFunctionLibrary::StaticClass();
	static const FNameNativePtrPair Funcs[] = {
		{ "CollectReferencedTextures", &UBSFunctionLibrary::execCollectReferencedTextures },
		{ "GenerateRandomPolygonFromRectangles", &UBSFunctionLibrary::execGenerateRandomPolygonFromRectangles },
		{ "HelloUE", &UBSFunctionLibrary::execHelloUE },
		{ "MultyCaptureAnimSequence", &UBSFunctionLibrary::execMultyCaptureAnimSequence },
		{ "RegexExtract", &UBSFunctionLibrary::execRegexExtract },
		{ "TensileAdaptation", &UBSFunctionLibrary::execTensileAdaptation },
	};
	FNativeFunctionRegistrar::RegisterFunctions(Class, Funcs, UE_ARRAY_COUNT(Funcs));
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(UBSFunctionLibrary);
UClass* Z_Construct_UClass_UBSFunctionLibrary_NoRegister()
{
	return UBSFunctionLibrary::StaticClass();
}
struct Z_Construct_UClass_UBSFunctionLibrary_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "Comment", "/**\n * \n */" },
		{ "IncludePath", "BSFunctionLibrary.h" },
		{ "ModuleRelativePath", "Public/BSFunctionLibrary.h" },
	};
#endif // WITH_METADATA
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UBSFunctionLibrary_CollectReferencedTextures, "CollectReferencedTextures" }, // 1829687182
		{ &Z_Construct_UFunction_UBSFunctionLibrary_GenerateRandomPolygonFromRectangles, "GenerateRandomPolygonFromRectangles" }, // 3860355025
		{ &Z_Construct_UFunction_UBSFunctionLibrary_HelloUE, "HelloUE" }, // 3626023923
		{ &Z_Construct_UFunction_UBSFunctionLibrary_MultyCaptureAnimSequence, "MultyCaptureAnimSequence" }, // 2184682909
		{ &Z_Construct_UFunction_UBSFunctionLibrary_RegexExtract, "RegexExtract" }, // 3379347308
		{ &Z_Construct_UFunction_UBSFunctionLibrary_TensileAdaptation, "TensileAdaptation" }, // 15058199
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBSFunctionLibrary>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
UObject* (*const Z_Construct_UClass_UBSFunctionLibrary_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UBlueprintFunctionLibrary,
	(UObject* (*)())Z_Construct_UPackage__Script_ED_BlueSpace_Runtime,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBSFunctionLibrary_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBSFunctionLibrary_Statics::ClassParams = {
	&UBSFunctionLibrary::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	nullptr,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	0,
	0,
	0x001000A0u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBSFunctionLibrary_Statics::Class_MetaDataParams), Z_Construct_UClass_UBSFunctionLibrary_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_UBSFunctionLibrary()
{
	if (!Z_Registration_Info_UClass_UBSFunctionLibrary.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBSFunctionLibrary.OuterSingleton, Z_Construct_UClass_UBSFunctionLibrary_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBSFunctionLibrary.OuterSingleton;
}
template<> ED_BLUESPACE_RUNTIME_API UClass* StaticClass<UBSFunctionLibrary>()
{
	return UBSFunctionLibrary::StaticClass();
}
UBSFunctionLibrary::UBSFunctionLibrary(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer) {}
DEFINE_VTABLE_PTR_HELPER_CTOR(UBSFunctionLibrary);
UBSFunctionLibrary::~UBSFunctionLibrary() {}
// End Class UBSFunctionLibrary

// Begin Registration
struct Z_CompiledInDeferFile_FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBSFunctionLibrary, UBSFunctionLibrary::StaticClass, TEXT("UBSFunctionLibrary"), &Z_Registration_Info_UClass_UBSFunctionLibrary, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBSFunctionLibrary), 2231972741U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_4046469822(TEXT("/Script/ED_BlueSpace_Runtime"),
	Z_CompiledInDeferFile_FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_HostProject_Plugins_ED_BlueSpace_Source_ED_BlueSpace_Public_BSFunctionLibrary_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
