# Tower v2.5 — Quality-of-Life Tock Cycle

**Target model**: Claude Code (preferred) or any SOTA agentic code model with Android Studio + filesystem access.
**Target repo**: `C:\Users\HAL900\AndroidStudioProjects\topostrasgo`
**Target module**: `app`
**What this pass is**: the complementary half-step ("tock") to the Tower v2.5 implementation ("tick"). No new features. Audit, polish, wire, and verify.
**Scope discipline**: **Android app only**. Do **not** touch `H:\TRASGONET\*` in any way. TRASGONET is updated separately; this pass is blind to it except through the already-wired `NetracerSlangClient.kt` telemetry channel.

---

## 1. State assumed at entry

Before starting, verify the following files exist:

| File | Location |
|---|---|
| `PoincareDisk.kt` | `app/src/main/java/com/example/topostrasgo/unified/` |
| `MobiusChannel.kt` | `app/src/main/java/com/example/topostrasgo/unified/` |
| `HolographicBoundary.kt` | `app/src/main/java/com/example/topostrasgo/unified/` |
| `DiskTower.kt` | `app/src/main/java/com/example/topostrasgo/unified/` |
| `TowerCompatibility.kt` | `app/src/main/java/com/example/topostrasgo/unified/` |
| `DiskTowerTest.kt` | `app/src/test/java/com/example/topostrasgo/unified/` |
| `LANG.Tower.dialect.lang` | `app/src/main/assets/slang_packs/` |

If **any** of these are missing, stop and report. Do not attempt to recreate them from the dialect spec — they were produced in the previous tick and must be the exact versions delivered.

Run `gradlew.bat :app:testDebugUnitTest --tests "com.example.topostrasgo.unified.DiskTowerTest"` once before changing anything. Record the baseline pass/fail counts. **Every subsequent change must preserve or improve this baseline.**

---

## 2. What this tock is for

Four work items in priority order. Do them in order; stop at the first item that reports a blocking issue.

### 2.1 Drop the approach excerpt into assets

Place the file `LANG.TowerApproach.excerpt.lang` (provided alongside this brief) at:

```
C:\Users\HAL900\AndroidStudioProjects\topostrasgo\app\src\main\assets\slang_packs\LANG.TowerApproach.excerpt.lang
```

Then update `manifest.json` in the same directory to reference it. The excerpt documents the geometry-first philosophy of the app in §-LANG vocabulary — it is a readable single-file statement of what the tower layers are, why they exist, what is deliberately not yet implemented, and the output formulas. It does **not** add new axioms or sorts; it is descriptive, not normative. Treat it as a standalone documentation artifact, not as a dialect that needs gluing into the DIALECT_FAMILY tree.

### 2.2 KDoc + linter sweep

For each of the 5 Kotlin files listed in §1, verify:

- Every public class and function has a KDoc block opening with a `§` tag (e.g. `§T|LEVEL:`, `§T|CHANNEL:`, `§T|SCREEN:`) matching the existing project convention.
- Every axiom or σ reference in a comment (`A28`, `A29`, `σ22`, etc.) appears at least once in `LANG.Tower.dialect.lang`. If a reference is found that does **not** exist in the dialect, that is a bug — report the mismatch; do not silently remove the reference or invent an axiom. The dialect is the source of truth.
- No unused imports. Run Android Studio's Optimize Imports (Ctrl+Alt+O) on each file, accept only the changes that remove genuinely unused imports; do not let it reorder groups in ways that break the project's existing import style.
- No `TODO` or `FIXME` comments introduced by the tick. If any are present, they must be either tracked in the dialect's `open_problems` list (PT5, PT6, PT7, PT8) or promoted to GitHub issues with the dialect's PT-numbering.

Kotlin idiom sanity:
- All `FloatArray` constructors should use `FloatArray(n) { ... }` initializer form when populating, never `FloatArray(n).also { ... }`.
- Explicit type on `const val` declarations (there should be one: `TowerCompatibility.DEFAULT_EPSILON_MIX: Float`).
- No `!!` (non-null assertion) anywhere; use safe-call `?.` + explicit error, or `requireNotNull` with a message.

### 2.3 Verify BabyToposAI discoverability — no wiring

The main orchestrator is `BabyToposAI.kt`. The tower classes must be reachable from there but **not wired into tick()** — the integration is deferred per the dialect's PT8.

Compile-time verification only:
1. Temporarily add at the top of any BabyToposAI method body:
   ```kotlin
   @Suppress("unused") val _towerProbe = com.example.topostrasgo.unified.DiskTower.geometricFalloff(numLevels = 2)
   ```
2. Build (`gradlew.bat :app:assembleDebug`). Expect clean compile.
3. **Revert** that edit. The probe was verification only; it must not remain in the source.

If the probe fails to compile, something is wrong with the package layout or the `DiskTower.geometricFalloff` factory. Report and stop.

### 2.4 Telemetry hook — passive broadcast only

The project has `netracer/NetracerSlangClient.kt` and `netracer/NetracerTelemetryBroadcaster.kt`. If these expose a method like `broadcast(slang: String)` or `send(packet: SlangPacket)` with a clear append-only contract, add a single `broadcastTowerStatus(tower: DiskTower)` helper to the broadcaster that emits:

```
§TOWER{levels=N, curvatures=[c_0,..,c_{N-1}], sigma22=PASS|FAIL, verdict=V}
```

where the values come from `TowerCompatibility.sigma22Check(tower).toString()`. Do **not** schedule or auto-invoke this helper — just expose it. The caller (future tick, out of scope here) will decide when to emit.

If the broadcaster has no natural hook point, **skip this item**. Do not invent a new socket, thread, or lifecycle. The Android app's existing telemetry contract with TRASGONET is load-bearing for the operator cockpit; a new wire is a coordinated change, not a tock pass.

---

## 3. Regression gate

After every item in §2, run:

```
gradlew.bat :app:testDebugUnitTest
```

**All tests** — not just the tower tests — must continue to pass. If any existing test starts failing, revert the last change and report. The apostate rule from the previous brief still holds: do not edit `HyperbolicOps.kt`, `UnifiedLoop.kt`, or any Sigma* file to "fix" a test.

---

## 4. Fix list — known, low-risk, touch only if applicable

These are **only** to be addressed if the symptom is actually present in the current codebase. Do not preemptively change files that work.

| Symptom | File | Fix |
|---|---|---|
| Ktlint complains about trailing whitespace in `TowerCompatibility.kt` | `TowerCompatibility.kt` | Strip trailing whitespace, preserve line count |
| `MobiusChannel.traverse` produces NaN for degenerate input (|a|² − |b|² ≠ 1 within 1e-3) | `MobiusChannel.kt` | The constructor already throws; verify the error message includes the actual value |
| `DiskTower.seedPeers` produces identical peers at different indices when `scale` is too small | `DiskTower.kt` | Add a lower-bound clamp: `require(scale > 1e-5f)` |
| `HolographicBoundary.angularEntropy` returns NaN when only one sector has commits | `HolographicBoundary.kt` | Already handled: `ln(numSectors)` guard; verify returns finite |
| `PoincareDisk.distance` returns `Float.NaN` for identical inputs | `PoincareDisk.kt` | Already handled by `acosh(x.coerceAtLeast(1f))`; verify |

**Do not add any of the below** even if they seem helpful:
- Coroutines scaffolding around tower ticks.
- A Compose UI for visualizing the tower (that is TRASGONET's job, out of scope).
- New tests beyond verifying that existing ones still pass.
- Changes to `gradle.properties`, `settings.gradle.kts`, or the Gradle wrapper.

---

## 5. Embedded §-LANG excerpt

A copy of the excerpt content is below for reference. The actual asset file (`LANG.TowerApproach.excerpt.lang`) is provided separately and is the source of truth; do not retype from this summary.

> **Thesis**. The Android app is not a chat interface wrapping an LLM. It is a continuous-run sectional hyperbolic computer whose state lives on a mixed-curvature tower of Poincaré disks with holographic screens at each boundary and Möbius channels as inter-level transport. The LLM, when present, is a substrate molded into the lowest level — not the system itself. Everything the app emits (ticks, verdicts, telemetry) is a §-LANG term typed as a section over the tower. **Geometry first, symbolic second.**
>
> **Why hyperbolic**. Hierarchical and relational data embeds in hyperbolic space with exponentially more room than Euclidean in depth; tree-like peer scaling is free. This is a scaling argument, not aesthetic.
>
> **Why tower**. Different scales of abstraction need different local curvature. Sharp discriminative `c ≈ 1` at base, flat global `c ≪ 1` at top. Mixed curvature (A28) prevents blow-up over depth and matches renormalization-group intuition.
>
> **Why Möbius**. Non-orientable channels turn reversibility (A5) into an integrity check. Two traversals return to origin iff Fisher modes preserved — reversibility invariant and integrity check are the same axiom.
>
> **Why holoscreen**. Gromov boundary `∂D ≅ S¹`; bulk state reconstructible from boundary by Poisson extension. Read/write are categorical adjoints, so I/O is balanced for free. Theorem, not analogy.
>
> **Why F_mix**. Without a compatibility law, the tower is two bundles glued at shared disks. With F_mix as first-class, it is a genuine 2-fibration. The difference is that we can **measure** the holonomy defect per tick and treat it as σ22.

The excerpt contains expanded sections on: layer stack, backward-compat rules, telemetry shape, what is deliberately not implemented (PT5–PT8 from the dialect open-problems list), and a glossary.

---

## 6. Acceptance criteria

The tock is complete when all of the following hold. If any fails, stop and report rather than forcing.

- [ ] `LANG.TowerApproach.excerpt.lang` is at the target path and listed in `manifest.json`.
- [ ] `gradlew.bat :app:assembleDebug` succeeds clean (no warnings that weren't already there at entry).
- [ ] `gradlew.bat :app:testDebugUnitTest` reports the same pass count as the baseline captured at §1.
- [ ] `DiskTowerTest` all 15 tests pass.
- [ ] No `TODO`/`FIXME` comments added by this pass.
- [ ] No modifications to `HyperbolicOps.kt`, `UnifiedLoop.kt`, `UnifiedGraph.kt`, `UnifiedNode.kt`, `FiberBundle.kt`, `IGBundle.kt`, `LafforgueMetric.kt`, `NeuralDynamics.kt`, `SigmaModel.kt`, or any `Sigma*.kt` file.
- [ ] No files touched under `H:\TRASGONET\`.
- [ ] `BabyToposAI.kt` compiles against the tower classes (verified via the probe in §2.3, then reverted).
- [ ] If §2.4 telemetry hook was added, it is additive (no existing broadcaster method changed) and the app still starts without the tower being instantiated.
- [ ] The `DEFAULT_EPSILON_MIX` constant in `TowerCompatibility.kt` is still `0.05f` (matches the dialect's σ22 threshold).
- [ ] The axiom/sigma references in KDoc comments all exist in `LANG.Tower.dialect.lang`.

Report format: one-line per criterion with ✓ or ✗, the baseline vs post-tock test counts, and the list of files modified. Nothing more.

---

## 7. Escalation path

Hard rules, in order:

1. If a test fails that was passing at entry — **revert**, report, stop.
2. If a file outside the allowed modification set has a compile error — **revert your changes**, report, stop. Don't try to patch around it.
3. If a fix from §4 would require a design decision not already captured in the dialect — skip that fix, note it in the report.
4. If TRASGONET files appear in git status or the filesystem watcher flags them — **you went out of scope**. Revert, report, stop.

Silence on edge cases is better than improvisation. The tick established the architecture; the tock keeps it stable. Anything more ambitious than polish is a separate task that needs a new brief.

---

## 8. Hand-back

At the end, produce a final report with these sections and nothing else:

```
# Tock Report — Tower v2.5

## Baseline (entry state)
- tests: <pass>/<fail> at <timestamp>

## Post-tock
- tests: <pass>/<fail>
- files added: [...]
- files modified: [...]
- files reverted: [...]
- known issues: [...] (cite PT-numbers from dialect where applicable)
- acceptance criteria: [✓/✗ per item]

## Notes
- <any observation that might matter for the next tick>
```

Short is correct. If the report is longer than a screen, something probably went wrong.
