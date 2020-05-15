def func(N):
    if N < 2:
        return 3
    if N == 3:
        return 5
    return (func(N - 2) * func(N - 3)) + func(N - 1)

print(func(5))