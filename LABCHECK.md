# Laboratory Submission Check

**Course:** CPEPRO8L — Data Structures and Algorithms Laboratory  
**Student:** John Vincent M. Robles  
**Repository checked:** `iFixRefrigerator/CPEPRO8L-DSA-LABORATORIES`  
**Evaluation date:** August 1, 2026  
**Status:** Provisional repository-based evaluation

## Evaluation Criteria

| Criterion | Weight |
|---|---:|
| Program Correctness and Functionality | 40% |
| Code Quality and Organization | 20% |
| Analysis and Understanding | 20% |
| Documentation (`README.md`) | 10% |
| GitHub Repository Organization and Submission | 10% |
| **Total** | **100%** |

## Results

| Laboratory | Correctness /40 | Code Quality /20 | Analysis /20 | Documentation /10 | Repository /10 | Grade |
|---:|---:|---:|---:|---:|---:|---:|
| Lab 1 | 30 | 12 | 17 | 9 | 9 | **77/100** |
| Lab 2 | 40 | 18 | 19 | 9 | 9 | **95/100** |
| Lab 3 | 40 | 18 | 18 | 9 | 9 | **94/100** |
| **Average of submitted laboratories** | **36.7** | **16.0** | **18.0** | **9.0** | **9.0** | **88.7/100** |

## Verification Summary

- All submitted Python files compiled successfully.
- Labs 2 and 3 passed the required functional tests and additional edge cases.
- Lab 1's constant-time and linear-time functions passed.
- Lab 1's quadratic function failed the required-result test.

## Required Corrections

1. **Correct Lab 1 `quadratic_time_pairs()`.** The required function must accumulate and return the product sum:

   ```python
   def quadratic_time_pairs(arr):
       pair_sum = 0
       n = len(arr)
       for i in range(n):
           for j in range(n):
               pair_sum += arr[i] * arr[j]
       return pair_sum
   ```

2. The current implementation creates and stores every tuple pair. This changes the required result and adds **O(n²) memory consumption**, which can exhaust memory for large values such as `N = 5000`.
3. Rerun the Lab 1 profiling experiment after correcting the function and replace the benchmark table with the new measurements.
4. Update the Lab 1 analysis to distinguish time complexity from space complexity.
5. Expand the root `README.md` with links to each laboratory.
6. Add Labs 4 and 5 when they become due or identify their status in the root README.

## Instructor Note

Labs 2 and 3 are strong and correct. The principal deduction is the Lab 1 quadratic function, which does not implement the assigned computation and creates a substantial memory risk. This grade covers submitted repository evidence only and may be adjusted according to deadlines, late-submission rules, or an oral/code defense.
