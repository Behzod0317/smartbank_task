#Additional task
#2. Implement SQRT(const double & x) without using any special functions, just fundamental arithmetic.
def sqrt(x: float, tolerance: float = 1e-10) -> float:
    if x < 0:
        raise ValueError("negative number")
    if x == 0:
        return 0.0
    g = x / 2.0

    while True:
        next_g = (g + x / g) / 2.0
        if abs(next_g - g) < tolerance:
            break

        g = next_g

    return g
print(sqrt(81))
print(sqrt(2))