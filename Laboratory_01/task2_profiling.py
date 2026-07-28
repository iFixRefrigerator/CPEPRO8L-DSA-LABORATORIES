import time

# O(1) Constant Time
def constant_time_check(arr):
    return arr[0] if len(arr) > 0 else None

# O(n) Linear Time
def linear_time_sum(arr):
    total = 0
    for value in arr:
        total += value
    return total

# O(n²) Quadratic Time
def quadratic_time_pairs(arr):
    pairs = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            pairs.append((arr[i], arr[j]))
    return pairs

# Benchmarking
N_values = [100, 500, 1000, 5000, 10000]

print(f"{'N':<8} {'O(1) (us)':<12} {'O(n) (us)':<12} {'O(n²) (us)':<12}")
print("-" * 48)

for n in N_values:
    test_list = list(range(n))
    
    # O(1)
    start = time.perf_counter()
    constant_time_check(test_list)
    t_constant = (time.perf_counter() - start) * 1_000_000
    
    # O(n)
    start = time.perf_counter()
    linear_time_sum(test_list)
    t_linear = (time.perf_counter() - start) * 1_000_000
    
    # O(n²) - skip for N=10000 if too slow
    if n <= 5000:
        start = time.perf_counter()
        quadratic_time_pairs(test_list)
        t_quadratic = (time.perf_counter() - start) * 1_000_000
        q_text = f"{t_quadratic:.2f}"
    else:
        t_quadratic = None
        q_text = "SKIPPED"
    
    print(f"{n:<8} {t_constant:.2f}       {t_linear:.2f}       {q_text}")
