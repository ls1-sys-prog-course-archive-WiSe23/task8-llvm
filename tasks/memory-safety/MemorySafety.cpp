#include "llvm/Analysis/PostDominators.h"
#include "llvm/Analysis/TargetLibraryInfo.h"
#include "llvm/Analysis/TargetTransformInfo.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/IR/InstVisitor.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"

#define DEBUG_TYPE "memory-safety"

using namespace llvm;

namespace {
    struct MemorySafetyPass : PassInfoMixin<MemorySafetyPass> {
    public:
        PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM) {
            errs() << "Running MemorySafetyPass on function " << F.getName() << "\n";

            return PreservedAnalyses::all();
        }

        // do not skip this pass for functions annotated with optnone
        static bool isRequired() { return true; }
    };
} // namespace

/// Registration
PassPluginLibraryInfo getPassPluginInfo() {
    const auto callback = [](PassBuilder &PB) {
        PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM, auto) {
                    if (Name == "memory-safety") {
                        FPM.addPass(MemorySafetyPass());
                        return true;
                    }
                    return false;
                });
    };
    return {LLVM_PLUGIN_API_VERSION, "MemorySafetyPass",
            LLVM_VERSION_STRING, callback};
};

extern "C" LLVM_ATTRIBUTE_WEAK PassPluginLibraryInfo llvmGetPassPluginInfo() {
    return getPassPluginInfo();
}

#undef DEBUG_TYPE
