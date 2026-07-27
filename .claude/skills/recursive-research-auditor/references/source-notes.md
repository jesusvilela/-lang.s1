# External method notes

Use these sources as methodological anchors, not as substitutes for domain-specific evidence.

- OpenAI, “Skills in ChatGPT” and OpenAI Academy, “Using skills”: define Skills as reusable workflows containing instructions, examples, and optional code, and recommend explicit inputs, stepwise process, output format, and final quality checks.
- NIST IR 8397, “Guidelines on Minimum Standards for Developer Verification of Software”: use threat modeling, automated tests, static analysis, black-box tests, structural tests, historical tests, fuzzing, and dependency review as a minimum verification portfolio.
- NIST Information Quality Standards: preserve transparency about data, assumptions, methods, and statistical procedures; require reproducibility commensurate with the claim's impact.
- Hypothesis documentation: use property-based tests to state invariants over generated domains, including edge cases and shrinking to minimal counterexamples; prefer round-trip and reference-equivalence properties.
- Chen, Cheung, and Yiu, “Metamorphic Testing: A New Approach for Generating Next Test Cases”: use relations among transformed executions when a direct test oracle is unavailable.

Do not cite these sources as proving the audited domain claim. Cite them only for the audit method they support.
