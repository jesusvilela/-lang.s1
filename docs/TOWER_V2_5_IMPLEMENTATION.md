# Tower v2.5 Implementation — Android Studio Integration Brief

**Target model**: Claude Code (preferred) or any SOTA agentic code model with Android Studio tool access.
**Target repo**: `C:\Users\HAL900\AndroidStudioProjects\topostrasgo`
**Target module**: `app`
**Android config**: minSdk 24, compileSdk 36, Kotlin, JVM 11, existing NDK setup (arm64-v8a + x86_64).
**Language spec source of truth**: `app/src/main/assets/slang_packs/LANG.v2.4.codec_trasgo.lang` (read first).

---

## 1. What this implements

§-LANG v2.5 Tower dialect — a vertical tower of Poincaré disks with horizontal peer interfaces via holographic screens, and the double-fibration compatibility law (F_mix, σ22) that makes the two scaling axes a genuine 2-fibration rather than two bundles glued at shared disks.

Single-level (N=1) usage reduces **exactly** to existing v2.4 `INTER_MANIFOLD` semantics — no behavior change for any existing caller. Tower logic activates only when `numLevels ≥ 2`.

**Do not modify any existing `unified/*.kt` file unless §5 explicitly says so.** This is an additive integration.

---

## 2. File manifest

Place the following files at the given absolute paths. All files are provided alongside this brief.

| Source file                      | Destination absolute path |
|----------------------------------|---------------------------|
| `LANG.Tower.dialect.lang`        | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\assets\slang_packs\LANG.Tower.dialect.lang` |
| `PoincareDisk.kt`                | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\java\com\example\topostrasgo\unified\PoincareDisk.kt` |
| `MobiusChannel.kt`               | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\java\com\example\topostrasgo\unified\MobiusChannel.kt` |
| `HolographicBoundary.kt`         | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\java\com\example\topostrasgo\unified\HolographicBoundary.kt` |
| `DiskTower.kt`                   | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\java\com\example\topostrasgo\unified\DiskTower.kt` |
| `TowerCompatibility.kt`          | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\java\com\example\topostrasgo\unified\TowerCompatibility.kt` |
| `DiskTowerTest.kt`               | `C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\test\java\com\example\topostrasgo\unified\DiskTowerTest.kt` |

All five Kotlin implementation files use `package com.example.topostrasgo.unified` to match the existing package. The test uses the same package so internal visibility works.

---

## 3. Dependencies

**No new Gradle dependencies required.** Everything is pure Kotlin + `kotlin.math` + `java.util.Random`. The test file uses `org.junit` which is already in the project (see `libs.junit` in `app/build.gradle.kts`).

Do **not** add any of the following (they are not needed and would bloat the APK):
- kotlinx-coroutines (the tower tick is synchronous by design)
- Apache Commons Math (we use bespoke SVD-free ops)
- Any numerical library (`HyperbolicOps.kt` has all the primitives we need)

---

## 4. Integration points

### 4.1 SlangPackLoader manifest

The existing `SlangPackLoader.kt` likely reads `manifest.json` in `slang_packs/`. Add the new dialect file to the manifest. Read:

```
C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\assets\slang_packs\manifest.json
```

Then append `LANG.Tower.dialect.lang` to the dialect file list following the pattern used for the existing dialects (e.g. `LANG.Swirl.dialect.lang`). Do **not** reorder existing entries.

### 4.2 UnifiedLoop tower hook (optional, deferred)

The existing `UnifiedLoop.kt` operates at a single level. Do **not** wire `DiskTower` into `UnifiedLoop.tick()` in this pass. Tower integration into the main loop is a follow-up task (tracked as PT8 in the dialect's `open_problems`).

What you **should** do: verify the tower classes compile against `HyperbolicOps` without modification. No edits to `UnifiedLoop`, `UnifiedGraph`, `UnifiedNode`, `FiberBundle`, `IGBundle`, `LafforgueMetric`, `NeuralDynamics`, `SigmaModel`, or any Sigma* file.

### 4.3 Telemetry (optional)

If `NetracerTelemetryBroadcaster.kt` has a hook point for σ-invariant streaming, add a line that emits `σ22` status from `TowerCompatibility.Sigma22Result`. If no natural hook exists, skip this — do not invent one.

---

## 5. Known interaction with existing code

### 5.1 HyperbolicOps.C is a const

`HyperbolicOps.kt` declares `const val C = 1.0f`. `PoincareDisk` deliberately does **not** modify this. When `PoincareDisk.curvature == 1.0f`, results agree with `HyperbolicOps` to within 1e-5 (verified in `poincareDisk_reducesToHyperbolicOps_atCurvatureOne` test). For `curvature != 1.0`, the disk uses its own parameterized ops.

**Do not** change `HyperbolicOps.C` to a `var`. Other code in the project relies on it being a compile-time constant.

### 5.2 HolographicTape vs HolographicBoundary

`topostrasgo/HolographicTape.kt` already implements a cylinder-manifold holographic memory with angular temporal indexing. `HolographicBoundary` is a **different object** — a spatial boundary sheaf on S¹ per tower level, not a temporal cylinder. Do not merge or replace.

The natural relationship: `HolographicTape.currentTheta` is temporal phase; `HolographicBoundary.projectToAngle` produces a spatial phase. A future integration could couple them (Kuramoto R-order), but that is out of scope here.

### 5.3 FiberBundle has its own W = B·A

`unified/FiberBundle.kt` carries LoRA-style rank-r fibers per node. `DiskTower` peers are raw disk points (FloatArray of dim=8), not fibers. Do not try to unify these in this pass — they operate at different levels of the architecture.

---

## 6. Execution steps

Perform in order. Stop on first failure and report.

1. **Read** `app/src/main/assets/slang_packs/LANG.v2.4.codec_trasgo.lang` to confirm v2.4 block names match what the Tower dialect imports.
2. **Copy** all 7 files per §2 manifest.
3. **Update** `manifest.json` per §4.1.
4. **Sync Gradle** (Android Studio: File → Sync Project with Gradle Files). Expected: no new dependencies resolved.
5. **Build** (Build → Make Project). Expected: clean compile. If any unresolved reference to `HyperbolicOps.dot`, `HyperbolicOps.norm`, or `HyperbolicOps.mobiusAdd`, check that `HyperbolicOps.kt` still exposes these as `fun` not `private fun` — they should be `fun` already in the existing code.
6. **Run tests** on the `app` module:
   ```
   ./gradlew :app:testDebugUnitTest --tests "com.example.topostrasgo.unified.DiskTowerTest"
   ```
   On Windows:
   ```
   gradlew.bat :app:testDebugUnitTest --tests "com.example.topostrasgo.unified.DiskTowerTest"
   ```
   Expected: all 15 tests pass. Each test is independent and deterministic (fixed RNG seeds).
7. **Verify no regressions** — run the full existing test suite:
   ```
   gradlew.bat :app:testDebugUnitTest
   ```
   Existing tests in `HyperbolicOpsTest`, `UnifiedLoopTest`, etc. must continue to pass.
8. **Report**: file paths created, test results (pass/fail counts), any compile warnings.

---

## 7. Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Unresolved reference: HyperbolicOps` | Test file in wrong source set | Ensure test is under `src/test/java/`, not `src/main/java/` |
| SU(1,1) assertion fails at runtime | Caller passed (a, b) not satisfying `|a|² − |b|² = 1` | Use `MobiusChannel.elliptic/hyperbolic/identity` factories |
| F_mix survey returns 0 rectangles | No H channels installed | Call `tower.connectPeers(k, p, q, ...)` before `surveyFMix` |
| σ22 always fails at small ε | Floating-point noise at the metric floor | Use `DEFAULT_EPSILON_MIX = 0.05f` or higher |
| Gradle resolution of `org.junit.Assert` fails | Test deps not wired | Verify `testImplementation(libs.junit)` in `app/build.gradle.kts` (already present) |

---

## 8. Post-integration verification (acceptance criteria)

The integration is **complete** when all of the following hold:

- [ ] All 7 files are present at the paths listed in §2.
- [ ] `gradlew.bat :app:assembleDebug` succeeds.
- [ ] `gradlew.bat :app:testDebugUnitTest` reports all tests passing, including the new `DiskTowerTest`.
- [ ] `manifest.json` lists the new dialect file.
- [ ] `PoincareDisk`, `MobiusChannel`, `HolographicBoundary`, `DiskTower`, `TowerCompatibility` are discoverable from `BabyToposAI.kt` (compile-time check: add a one-line `val t = DiskTower.geometricFalloff(2)` to any method body, then **revert** that edit after confirming it compiles).
- [ ] No modifications to any pre-existing `.kt` file except `manifest.json`-adjacent plumbing if needed.

Report any deviation from these criteria before considering the task done.

---

## 9. What is deliberately out of scope

These are **not** to be implemented in this pass, even if tempting:

- Wiring `DiskTower` into `UnifiedLoop.tick()` — requires coordinated design with neural dynamics and is tracked separately.
- Full Poisson-kernel integration in `HolographicBoundary.poissonExtend` — current implementation returns a single collar point, not a bulk distribution.
- Full Busemann-based projection for off-origin geodesics — `projectToAngle` uses the origin-direction heuristic (adequate for near-origin peers, noted as PT5 in the dialect `open_problems`).
- Gyration term in `MobiusChannel.traverse` — current implementation uses pure SU(1,1) complex pair action, which is exact for rigid rotations and approximate for off-axis transport. The existing `HyperbolicOps.parallelTransport` has the same approximation and has not been a blocker.
- Adjoint lift/proj regularizer proof (PT6) — pure theory; no code impact.
- CY/SU(3) coupling to tower (PT7) — requires CY dialect integration, separate pass.

If the caller requests any of the above, treat it as a new task and require a separate brief.

---

## 10. Escalation path

If the build fails in a way not covered by §7, **stop and report** rather than attempting speculative fixes. The right answer is usually:
1. Revert the changes.
2. Report the exact failing error and the last successful state.
3. Wait for guidance.

Do **not** edit `HyperbolicOps.kt`, `UnifiedLoop.kt`, or any Sigma* file to "make things work." Those files are load-bearing for existing empirical results (Sharpe=1.003, EV=0.131 per v2.4 `CONCLUSIONS.empirical_ev`) and must not drift.

---

## 11. Dialect summary (for context, not action)

The §-LANG v2.5 Tower dialect adds:

- **Sorts**: `Tower`, `Level`, `VChannel`, `HChannel`, `Screen_k`, `FMix`, `Peer`
- **Axioms**: A28 (monotone curvatures), A29 (vertical is Isom(H²)), A30 (horizontal is boundary Isom(H²)), A31 (F_mix compatibility)
- **σ invariants**: σ22 (F_mix < ε_mix), σ23 (tower depth × curvature bounded)
- **Output formula**: `CANON(§EMIT(fix(λtower. check_f_mix(evolve_all_levels(tower), ε_mix))))`

Read `LANG.Tower.dialect.lang` for the full spec. The implementation faithfully realizes every sort and axiom listed above, modulo the out-of-scope items in §9.
