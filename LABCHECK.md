# Laboratory Submission Recheck

**Course:** CPEPRO8L — Data Structures and Algorithms Laboratory  
**Student:** John Vincent M. Robles  
**Repository:** `iFixRefrigerator/CPEPRO8L-DSA-LABORATORIES`  
**Recheck date:** August 14, 2026  
**Status:** Provisional repository-based evaluation

## Recheck Summary

- Labs found: **1–4**
- Newly evaluated: **Lab 4**
- Missing from the current sequence: **Labs 5–7**
- All submitted Python files compile successfully.
- Labs 2–4 pass the functional tests.
- The previously reported Lab 1 quadratic-function defect remains unfixed.

## Evaluation Criteria

| Criterion | Weight |
|---|---:|
| Program Correctness and Functionality | 40% |
| Code Quality and Organization | 20% |
| Analysis and Understanding | 20% |
| Documentation (`README.md`) | 10% |
| GitHub Repository Organization and Submission | 10% |
| **Total** | **100%** |

## Updated Results

| Laboratory | Correctness /40 | Code /20 | Analysis /20 | Documentation /10 | Repository /10 | Grade |
|---:|---:|---:|---:|---:|---:|---:|
| Lab 1 | 30 | 12 | 17 | 9 | 9 | **77/100** |
| Lab 2 | 40 | 18 | 19 | 9 | 9 | **95/100** |
| Lab 3 | 40 | 18 | 18 | 9 | 9 | **94/100** |
| Lab 4 | 40 | 17 | 18 | 9 | 9 | **93/100** |
| **Average of submitted labs** | **37.5** | **16.3** | **18.0** | **9.0** | **9.0** | **89.8/100** |

If Labs 1–7 are all required and every missing laboratory receives zero, the completion-adjusted grade is **51.3/100**. Apply this only according to the instructor's deadline and missing-submission policy.

## Verified Tests

- Lab 1: constant and linear functions pass; required quadratic result fails.
- Lab 2: resizing, data preservation, capacity growth, and invalid indices pass.
- Lab 3: insertion, search, and head/middle/tail deletion pass.
- Lab 4: doubly linked `prev` integrity and circular tail-to-head closure pass.

## Corrections Required

1. Correct Lab 1 `quadratic_time_pairs()` so it accumulates and returns `pair_sum` rather than creating a list of tuple pairs.
2. The current Lab 1 implementation uses **O(n²) additional memory** and can exhaust memory at `N = 5000`.
3. Rerun and replace the Lab 1 benchmark table after fixing the function.
4. Use a simple singly linked node for the Lab 4 circular list instead of `DoubleNode`, whose `prev` field is unused.
5. Expand the root README with links to all submitted laboratories.
6. Submit Labs 5–7 when required.

## Instructor Note

Lab 4 is a correct new submission and raises the submitted-work average. However, the Lab 1 defect identified in the first evaluation was not corrected. Scores may be adjusted for deadlines, late submissions, missing laboratories, or an oral/code defense.
