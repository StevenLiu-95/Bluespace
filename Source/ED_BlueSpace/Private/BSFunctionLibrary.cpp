// Fill out your copyright notice in the Description page of Project Settings.


#include "BSFunctionLibrary.h"
#include "Engine/Engine.h"
#include "Engine/Texture.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Actor.h"
#include "GeometryScript/GeometryScriptTypes.h"
#include "GeometryScript/PolygonFunctions.h"
#include "Internationalization/Regex.h"
#include "Materials/MaterialInterface.h"
#include "Components/PrimitiveComponent.h"
#include "UObject/UObjectGlobals.h"

#if WITH_EDITOR
#include "Animation/AnimSequence.h"
#include "Animation/Skeleton.h"
#include "Animation/SkeletalMeshActor.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "AssetUtils/CreateStaticMeshUtil.h"
#include "Components/SkeletalMeshComponent.h"
#include "Editor.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
#include "FileHelpers.h"
#include "GeometryScript/MeshMaterialFunctions.h"
#include "GeometryScript/MeshSimplifyFunctions.h"
#include "GeometryScript/SceneUtilityFunctions.h"
#include "Misc/PackageName.h"
#include "Misc/ScopedSlowTask.h"
#include "PackageTools.h"
#include "UDynamicMesh.h"
#endif

FString UBSFunctionLibrary::HelloUE()
{
    return TEXT("Hello, UE!");
}

bool UBSFunctionLibrary::RegexExtract(const FString& Input, const FString& Pattern, TArray<FString>& OutMatches, bool bAllMatches, int32 CaptureGroup)
{
    OutMatches.Empty();
    if (Pattern.IsEmpty())
    {
        return false;
    }

    FRegexPattern RegPattern(Pattern);
    FRegexMatcher Matcher(RegPattern, Input);

    bool bFoundAny = false;

    while (Matcher.FindNext())
    {
        bFoundAny = true;
        FString Captured;
        // Safely get the requested capture group; 0 means the whole match
        Captured = Matcher.GetCaptureGroup(CaptureGroup);
        OutMatches.Add(MoveTemp(Captured));

        if (!bAllMatches)
        {
            break;
        }
    }

    return bFoundAny;
}

void UBSFunctionLibrary::TensileAdaptation(float Whole, float Unit, float& Long, int32& Count)
{
    if (FMath::IsNearlyZero(Unit))
    {
        Long = 1.0f;
        Count = 0;
    }

    int32 Quotient = FMath::FloorToInt(Whole / Unit);
    int32 SelectedValue = (Quotient > 2) ? Quotient : 0;
    Long = static_cast<float>(FMath::Max(SelectedValue, 1));
    Count = Quotient;
}

TArray<FVector> UBSFunctionLibrary::GenerateRandomPolygonFromRectangles(float MinSize, float MaxSize, int32 Iterations, int32 Seed)
{
    TArray<FVector> Out;
    if (MinSize <= 0.f || MaxSize <= MinSize || Iterations <= 0)
    {
        return Out;
    }

    // �洢���о��Σ�����룩
    struct FRect { float X1, X2, Y1, Y2; };
    TArray<FRect> Rects;

    // ʹ�ø������Ӵ����������������֤�ɸ���
    FRandomStream Rand(Seed);

    // ��ʼ���Σ�����ߴ磬���Ĺ̶���ԭ��
    float W = FMath::Lerp(MinSize, MaxSize, Rand.FRand());
    float H = FMath::Lerp(MinSize, MaxSize, Rand.FRand());
    FVector2D Center = FVector2D::ZeroVector;

    auto PushRect = [&Rects](const FVector2D& C, float WW, float HH)
    {
        FRect R;
        R.X1 = C.X - WW * 0.5f; R.X2 = C.X + WW * 0.5f;
        R.Y1 = C.Y - HH * 0.5f; R.Y2 = C.Y + HH * 0.5f;
        Rects.Add(R);
    };

    PushRect(Center, W, H);

    for (int32 It = 1; It < Iterations; ++It)
    {
        // �¾��εĳ�����СֵΪ��һ�����ε� 0.6 �������ֵΪ��һ�����ε�ֵ
        float W2 = FMath::Lerp(W * 0.6f, W, Rand.FRand());
        float H2 = FMath::Lerp(H * 0.6f, H, Rand.FRand());
        int32 SX = (Rand.FRand() < 0.5f) ? 1 : -1;
        int32 SY = (Rand.FRand() < 0.5f) ? 1 : -1;

        FVector2D NewCenter = Center + FVector2D(SX * W2 * 0.5f, SY * H2 * 0.5f);
        PushRect(NewCenter, W2, H2);

        Center = NewCenter;
        W = W2;
        H = H2;
    }

    if (Rects.Num() == 0)
    {
        return Out;
    }

    // ʹ�� GeometryScript ���� SimplePolygon �б���ִ�в���
    TArray<FGeometryScriptSimplePolygon> SimplePolys;
    SimplePolys.Reserve(Rects.Num());

    for (const FRect& R : Rects)
    {
        TArray<FVector2D> Vertices2D;
        Vertices2D.Add(FVector2D(R.X1, R.Y1));
        Vertices2D.Add(FVector2D(R.X2, R.Y1));
        Vertices2D.Add(FVector2D(R.X2, R.Y2));
        Vertices2D.Add(FVector2D(R.X1, R.Y2));
        FGeometryScriptSimplePolygon Poly = UGeometryScriptLibrary_SimplePolygonFunctions::Conv_ArrayOfVector2DToGeometryScriptSimplePolygon(Vertices2D);
        SimplePolys.Add(Poly);
    }

    FGeometryScriptGeneralPolygonList PolyList = UGeometryScriptLibrary_PolygonListFunctions::CreatePolygonListFromSimplePolygons(SimplePolys);
    FGeometryScriptGeneralPolygonList UnionList = UGeometryScriptLibrary_PolygonListFunctions::PolygonsUnion(PolyList);

    // ѡȡ�������������
    int32 Count = UGeometryScriptLibrary_PolygonListFunctions::GetPolygonCount(UnionList);
    if (Count == 0) return Out;

    int32 BestIdx = 0;
    double BestArea = 0.0;
    for (int32 i = 0; i < Count; ++i)
    {
        bool bAreaValid = false;
        double Area = UGeometryScriptLibrary_PolygonListFunctions::GetPolygonArea(UnionList, bAreaValid, i);
        if (bAreaValid && FMath::Abs((float)Area) > BestArea)
        {
            BestArea = FMath::Abs((float)Area);
            BestIdx = i;
        }
    }

    TArray<FVector2D> OuterVertices2D;
    // Note: GeometryScript's GetPolygonVertices may not reliably set the validity flag in some engine versions,
    // so do not rely solely on it. Instead check the returned vertex array.
    bool bVerticesValid = false;
    UGeometryScriptLibrary_PolygonListFunctions::GetPolygonVertices(UnionList, OuterVertices2D, bVerticesValid, BestIdx, -1);
    if (OuterVertices2D.Num() == 0) return Out;

    // GeometryScript ���صĶ���ͨ��Ϊ CCW���⻷����������Ҫ CW
    auto SignedArea = [](const TArray<FVector2D>& Poly)->double
    {
        double A = 0.0;
        int32 N = Poly.Num();
        for (int32 i = 0; i < N; ++i)
        {
            const FVector2D& P = Poly[i];
            const FVector2D& Q = Poly[(i + 1) % N];
            A += (double)P.X * (double)Q.Y - (double)P.Y * (double)Q.X;
        }
        return A * 0.5;
    };

    double SA = SignedArea(OuterVertices2D);
    if (SA > 0)
    {
        Algo::Reverse(OuterVertices2D);
    }

    for (const FVector2D& P : OuterVertices2D)
    {
        Out.Add(FVector(P.X, P.Y, 0.f));
    }

    return Out;
}

TArray<UTexture*> UBSFunctionLibrary::CollectReferencedTextures(const UObject* WorldContextObject, const TArray<AActor*>& Actors)
{
    TArray<UTexture*> Result;
    TSet<UTexture*> UniqueTextures;

    auto AddTexture = [&UniqueTextures](UTexture* Texture)
    {
        if (IsValid(Texture) && Texture->IsAsset())
        {
            UniqueTextures.Add(Texture);
        }
    };

    auto CollectFromActor = [&AddTexture](AActor* Actor)
    {
        if (!IsValid(Actor))
        {
            return;
        }

        // Collect hard UObject references recursively (components, materials, textures, etc.)
        TArray<UObject*> ReferencedObjects;
        FReferenceFinder RefFinder(ReferencedObjects, nullptr, false, true, true, false);
        RefFinder.FindReferences(Actor);

        for (UObject* Obj : ReferencedObjects)
        {
            if (UTexture* Texture = Cast<UTexture>(Obj))
            {
                AddTexture(Texture);
            }
        }

        // Also collect textures used by materials on primitive components
        TArray<UPrimitiveComponent*> PrimitiveComponents;
        Actor->GetComponents<UPrimitiveComponent>(PrimitiveComponents);
        for (UPrimitiveComponent* Component : PrimitiveComponents)
        {
            if (!IsValid(Component))
            {
                continue;
            }

            TArray<UMaterialInterface*> Materials;
            Component->GetUsedMaterials(Materials);
            for (UMaterialInterface* Material : Materials)
            {
                if (!IsValid(Material))
                {
                    continue;
                }

                ERHIFeatureLevel::Type FeatureLevel = ERHIFeatureLevel::SM5;
                if (const UWorld* World = Actor->GetWorld())
                {
                    FeatureLevel = World->GetFeatureLevel();
                }

                TArray<UTexture*> UsedTextures;
                Material->GetUsedTextures(UsedTextures, EMaterialQualityLevel::Num, true, FeatureLevel, true);
                for (UTexture* Texture : UsedTextures)
                {
                    AddTexture(Texture);
                }
            }
        }
    };

    if (Actors.Num() == 0)
    {
        UWorld* World = GEngine
            ? GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull)
            : nullptr;
        if (!World)
        {
            return Result;
        }

        for (TActorIterator<AActor> It(World); It; ++It)
        {
            CollectFromActor(*It);
        }
    }
    else
    {
        for (AActor* Actor : Actors)
        {
            CollectFromActor(Actor);
        }
    }

    Result.Reserve(UniqueTextures.Num());
    for (UTexture* Texture : UniqueTextures)
    {
        Result.Add(Texture);
    }
    return Result;
}

TArray<UStaticMesh*> UBSFunctionLibrary::MultyCaptureAnimSequence(
    const TArray<UAnimSequence*>& Animations,
    const TArray<float>& Frames,
    const FString& Path,
    float RemeshPercentage,
    UMaterialInterface* Material,
    bool GenerateLOD)
{
    TArray<UStaticMesh*> Result;

#if WITH_EDITOR
    if (Animations.Num() == 0 || Frames.Num() == 0 || Path.IsEmpty())
    {
        return Result;
    }

    if (!GEditor)
    {
        UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: GEditor is null, editor-only function."));
        return Result;
    }

    UWorld* World = GEditor->GetEditorWorldContext().World();
    if (!World)
    {
        UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: No editor world available."));
        return Result;
    }

    const float ClampedRemeshPct = FMath::Clamp(RemeshPercentage, 0.f, 100.f);
    const float KeepRatio = ClampedRemeshPct / 100.f;

    // Content Browser folder paths often look like "/All/Game/..." — strip the virtual "/All" root.
    FString NormalizedPath = Path;
    NormalizedPath.ReplaceInline(TEXT("\\"), TEXT("/"));
    while (NormalizedPath.EndsWith(TEXT("/")))
    {
        NormalizedPath.LeftChopInline(1);
    }
    if (NormalizedPath.StartsWith(TEXT("/All/")))
    {
        NormalizedPath.RightChopInline(4); // "/All/Game/..." -> "/Game/..."
    }
    else if (NormalizedPath.Equals(TEXT("/All")))
    {
        NormalizedPath = TEXT("/Game");
    }
    if (!NormalizedPath.StartsWith(TEXT("/")))
    {
        NormalizedPath = TEXT("/Game/") + NormalizedPath;
    }

    {
        FString MountCheckFilename;
        if (!FPackageName::TryConvertLongPackageNameToFilename(NormalizedPath, MountCheckFilename))
        {
            UE_LOG(LogTemp, Error,
                TEXT("MultyCaptureAnimSequence: Path '%s' (from '%s') is not under a valid content mount (e.g. /Game/...)."),
                *NormalizedPath, *Path);
            return Result;
        }
    }

    const int32 TotalWork = Animations.Num() * Frames.Num();
    FScopedSlowTask SlowTask(static_cast<float>(TotalWork) + 2.f, NSLOCTEXT("ED_BlueSpace", "MultyCaptureAnimSequence", "Capturing Anim Sequences..."));
    SlowTask.MakeDialog(true);

    auto RefreshSkelComponent = [](USkeletalMeshComponent* Component)
    {
        if (!Component)
        {
            return;
        }
        // Minimal pose update required for GetCPUSkinnedVertices / CopyMeshFromComponent.
        Component->TickAnimation(0.f, false);
        Component->RefreshBoneTransforms();
        Component->FinalizeBoneTransform();
    };

    auto ApplyRemeshPercentage = [KeepRatio](UDynamicMesh* TargetMesh)
    {
        if (!TargetMesh || KeepRatio >= 1.f - KINDA_SMALL_NUMBER)
        {
            return;
        }

        const int32 SourceTriCount = TargetMesh->GetTriangleCount();
        if (SourceTriCount <= 0)
        {
            return;
        }

        const int32 TargetTriCount = FMath::Max(4, FMath::RoundToInt(static_cast<float>(SourceTriCount) * KeepRatio));
        if (TargetTriCount >= SourceTriCount)
        {
            return;
        }

        // StandardQEM is significantly faster than AttributeAware; skip AutoCompact until export.
        FGeometryScriptSimplifyMeshOptions SimplifyOptions;
        SimplifyOptions.Method = EGeometryScriptRemoveMeshSimplificationType::StandardQEM;
        SimplifyOptions.bAutoCompact = false;
        SimplifyOptions.bAllowSeamCollapse = true;
        SimplifyOptions.bAllowSeamSmoothing = false;
        SimplifyOptions.bAllowSeamSplits = false;
        UGeometryScriptLibrary_MeshSimplifyFunctions::ApplySimplifyToTriangleCount(TargetMesh, TargetTriCount, SimplifyOptions);
    };

    auto MakeUniqueAssetPath = [](const FString& FolderPath, const FString& BaseAssetName) -> FString
    {
        const FString SanitizedBase = UPackageTools::SanitizePackageName(FolderPath / BaseAssetName);
        if (!FPackageName::DoesPackageExist(SanitizedBase))
        {
            return SanitizedBase;
        }

        for (int32 Suffix = 1; Suffix < 10000; ++Suffix)
        {
            const FString Candidate = UPackageTools::SanitizePackageName(
                FString::Printf(TEXT("%s_%d"), *SanitizedBase, Suffix));
            if (!FPackageName::DoesPackageExist(Candidate))
            {
                return Candidate;
            }
        }
        return SanitizedBase;
    };

    FActorSpawnParameters SpawnParams;
    SpawnParams.ObjectFlags = RF_Transient;
    SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

    ASkeletalMeshActor* TempActor = World->SpawnActor<ASkeletalMeshActor>(SpawnParams);
    if (!TempActor)
    {
        UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: Failed to spawn temporary SkeletalMeshActor."));
        return Result;
    }

    USkeletalMeshComponent* SkelComp = TempActor->GetSkeletalMeshComponent();
    SkelComp->SetUpdateAnimationInEditor(true);
    SkelComp->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
    SkelComp->SetComponentTickEnabled(true);

    // Reuse one DynamicMesh across captures to cut UObject churn.
    UDynamicMesh* DynamicMesh = NewObject<UDynamicMesh>(GetTransientPackage());
    FGeometryScriptCopyMeshFromComponentOptions CopyOptions;
    CopyOptions.bWantNormals = true;
    CopyOptions.bWantTangents = true;

    TArray<UPackage*> PackagesToSave;
    Result.Reserve(TotalWork);

    for (UAnimSequence* AnimSequence : Animations)
    {
        if (SlowTask.ShouldCancel())
        {
            break;
        }

        if (!IsValid(AnimSequence))
        {
            SlowTask.EnterProgressFrame(static_cast<float>(Frames.Num()));
            continue;
        }

        USkeletalMesh* SkeletalMesh = AnimSequence->GetPreviewMesh(true);
        if (!SkeletalMesh)
        {
            if (USkeleton* Skeleton = AnimSequence->GetSkeleton())
            {
                SkeletalMesh = Skeleton->GetPreviewMesh(true);
            }
        }

        if (!IsValid(SkeletalMesh))
        {
            UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: Anim '%s' has no preview skeletal mesh."), *AnimSequence->GetName());
            SlowTask.EnterProgressFrame(static_cast<float>(Frames.Num()));
            continue;
        }

        SkelComp->SetSkeletalMeshAsset(SkeletalMesh);
        SkelComp->SetAnimationMode(EAnimationMode::AnimationSingleNode);
        SkelComp->OverrideAnimationData(AnimSequence, false, false, 0.f, 0.f);
        SkelComp->InitAnim(true);

        const double FramesPerSecond = FMath::Max(AnimSequence->GetSamplingFrameRate().AsDecimal(), 1.0);
        const float PlayLength = AnimSequence->GetPlayLength();
        const FString AnimName = AnimSequence->GetName();

        for (float FrameValue : Frames)
        {
            if (SlowTask.ShouldCancel())
            {
                break;
            }

            SlowTask.EnterProgressFrame(1.f, FText::FromString(FString::Printf(TEXT("%s @ frame %.0f"), *AnimName, FrameValue)));

            const float SampleTime = FMath::Clamp(static_cast<float>(FrameValue / FramesPerSecond), 0.f, PlayLength);

            SkelComp->SetPosition(SampleTime, false);
            RefreshSkelComponent(SkelComp);

            if (!SkelComp->MeshObject)
            {
                UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: MeshObject missing for '%s' frame %.0f."), *AnimName, FrameValue);
                continue;
            }

            FTransform LocalToWorld;
            EGeometryScriptOutcomePins CopyOutcome = EGeometryScriptOutcomePins::Failure;
            UGeometryScriptLibrary_SceneUtilityFunctions::CopyMeshFromComponent(
                SkelComp,
                DynamicMesh,
                CopyOptions,
                false,
                LocalToWorld,
                CopyOutcome);

            if (CopyOutcome != EGeometryScriptOutcomePins::Success || DynamicMesh->GetTriangleCount() <= 0)
            {
                UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: Failed to copy mesh from '%s' frame %.0f."), *AnimName, FrameValue);
                continue;
            }

            ApplyRemeshPercentage(DynamicMesh);

            UGeometryScriptLibrary_MeshMaterialFunctions::EnableMaterialIDs(DynamicMesh);
            UGeometryScriptLibrary_MeshMaterialFunctions::ClearMaterialIDs(DynamicMesh, 0);

            const FString BaseAssetName = FString::Printf(TEXT("%s_Frame%d"), *AnimName, FMath::RoundToInt(FrameValue));
            const FString AssetPathAndName = MakeUniqueAssetPath(NormalizedPath, BaseAssetName);

            UStaticMesh* NewStaticMesh = nullptr;
            DynamicMesh->ProcessMesh([Material, &AssetPathAndName, &NewStaticMesh](const UE::Geometry::FDynamicMesh3& SourceMesh)
            {
                UE::AssetUtils::FStaticMeshAssetOptions AssetOptions;
                AssetOptions.NewAssetPath = AssetPathAndName;
                AssetOptions.NumSourceModels = 1;
                AssetOptions.NumMaterialSlots = 1;
                AssetOptions.AssetMaterials = { Material };
                AssetOptions.SourceMeshes.DynamicMeshes = { &SourceMesh };

                // Faster build options: skip expensive recomputes / collision / DF / RT during batch create.
                AssetOptions.bEnableRecomputeNormals = false;
                AssetOptions.bEnableRecomputeTangents = false;
                AssetOptions.bCreatePhysicsBody = false;
                AssetOptions.bAllowDistanceField = false;
                AssetOptions.bSupportRayTracing = false;
                AssetOptions.bBuildReversedIndexBuffer = false;
                AssetOptions.bGenerateLightmapUVs = false;
                AssetOptions.bDeferPostEditChange = true;

                UE::AssetUtils::FStaticMeshResults CreateResults;
                if (UE::AssetUtils::CreateStaticMeshAsset(AssetOptions, CreateResults) == UE::AssetUtils::ECreateStaticMeshResult::Ok)
                {
                    NewStaticMesh = CreateResults.StaticMesh;
                }
            });

            if (!IsValid(NewStaticMesh))
            {
                UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence: Failed to create static mesh asset '%s'."), *AssetPathAndName);
                continue;
            }

            // Use engine LOD reduction (one BatchBuild later) instead of GeometryScript per-LOD simplifies.
            if (GenerateLOD)
            {
                constexpr int32 NumLODs = 4;
                NewStaticMesh->SetNumSourceModels(NumLODs);
                const FMeshBuildSettings Lod0BuildSettings = NewStaticMesh->GetSourceModel(0).BuildSettings;
                for (int32 LodIndex = 1; LodIndex < NumLODs; ++LodIndex)
                {
                    FStaticMeshSourceModel& SrcModel = NewStaticMesh->GetSourceModel(LodIndex);
                    SrcModel.BuildSettings = Lod0BuildSettings;
                    const float LodKeep = FMath::Pow(0.5f, static_cast<float>(LodIndex));
                    SrcModel.ReductionSettings.PercentTriangles = LodKeep;
                    SrcModel.ReductionSettings.PercentVertices = LodKeep;
                }
            }

            FAssetRegistryModule::AssetCreated(NewStaticMesh);
            PackagesToSave.Add(NewStaticMesh->GetOutermost());
            Result.Add(NewStaticMesh);
        }
    }

    World->DestroyActor(TempActor);

    SlowTask.EnterProgressFrame(1.f, NSLOCTEXT("ED_BlueSpace", "MultyCaptureAnimSequence_Build", "Building Static Meshes..."));
    if (Result.Num() > 0)
    {
        UStaticMesh::BatchBuild(Result, /*bInSilent=*/true);
    }

    SlowTask.EnterProgressFrame(1.f, NSLOCTEXT("ED_BlueSpace", "MultyCaptureAnimSequence_Save", "Saving Assets..."));
    if (PackagesToSave.Num() > 0)
    {
        UEditorLoadingAndSavingUtils::SavePackages(PackagesToSave, /*bOnlyDirty=*/true);
    }
#else
    UE_LOG(LogTemp, Warning, TEXT("MultyCaptureAnimSequence is editor-only and unavailable in this build."));
#endif

    return Result;
}