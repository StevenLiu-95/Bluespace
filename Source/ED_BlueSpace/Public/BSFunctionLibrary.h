// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "BSFunctionLibrary.generated.h"

class AActor;
class UTexture;
class UAnimSequence;
class UStaticMesh;
class UMaterialInterface;

/**
 * 
 */
UCLASS()
class ED_BLUESPACE_RUNTIME_API UBSFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	
public:
    // Returns fixed string: Hello, UE!
    UFUNCTION(BlueprintPure, Category = "Bluespacer|Base")
    static FString HelloUE();

    UFUNCTION(BlueprintPure, Category = "Bluespacer|Base")
    static void TensileAdaptation(float Whole, float Unit, float& Long, int32& Count);

    // Merge random rectangles into a polygon outline; returns clockwise vertices (FVector, Z=0).
    UFUNCTION(BlueprintCallable, Category = "Bluespacer|Geometry")
    static TArray<FVector> GenerateRandomPolygonFromRectangles(float MinSize, float MaxSize, int32 Iterations, int32 Seed = 0);

    // Extract fields from a string with regex.
    // Pattern: regex pattern, capture groups supported.
    // OutMatches: matched results in order.
    // bAllMatches: true = all matches of the capture group; false = first match only.
    // CaptureGroup: capture group index to return; 0 = whole match.
    UFUNCTION(BlueprintCallable, Category = "Bluespacer|String")
    static bool RegexExtract(const FString& Input, const FString& Pattern, TArray<FString>& OutMatches, bool bAllMatches = true, int32 CaptureGroup = 1);

    // Collect texture assets referenced by Actors.
    // If Actors is empty, iterate all actors in the current world; otherwise only the given list.
    UFUNCTION(BlueprintCallable, Category = "Bluespacer|Asset", meta = (WorldContext = "WorldContextObject", AutoCreateRefTerm = "Actors"))
    static TArray<UTexture*> CollectReferencedTextures(const UObject* WorldContextObject, const TArray<AActor*>& Actors);

    /**
     * Batch-bake AnimSequence frames into StaticMesh assets (editor-only).
     * RemeshPercentage: percent of triangles to keep (100 = no remesh, 50 = keep ~50% tris, 0 = reduce to minimum).
     * GenerateLOD: when true, auto-generate LOD levels.
     */
    UFUNCTION(BlueprintCallable, Category = "Bluespacer|Animation", meta = (AutoCreateRefTerm = "Animations,Frames"))
    static TArray<UStaticMesh*> MultyCaptureAnimSequence(
        const TArray<UAnimSequence*>& Animations,
        const TArray<float>& Frames,
        const FString& Path,
        float RemeshPercentage,
        UMaterialInterface* Material,
        bool GenerateLOD);
};
