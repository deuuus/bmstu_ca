def make_table_of_squares(t_range, step):
    return [[i, i * i] for i in range(0, t_range + 1, step)]

def print_table(table):
    print("\nf(x):\n")
    for i in range(len(table)):
        print("f(", table[i][0], ") = ", table[i][1], sep="")
    print("\n")

def newton_interpolation(table, x, polynom_degree):
    diffs = [[0 for i in range(polynom_degree)] for i in range(polynom_degree)]

    start_pos = find_range(table, x, polynom_degree)

    for i in range(start_pos, start_pos + polynom_degree):
        diffs[i - start_pos][0] = (table[i][1] - table[i + 1][1]) / (table[i][0] - table[i + 1][0])

    for col in range(1, polynom_degree):
        for row in range(0, polynom_degree - col):
            diffs[row][col] = (diffs[row][col - 1] - diffs[row + 1][col - 1]) \
                              / (table[start_pos + row][0] - table[start_pos + row + col + 1][0])

    res = table[start_pos][1]
    temp = (x - table[start_pos][0])

    for i in range(polynom_degree):
        res += temp * diffs[0][i]
        temp *= (x - table[start_pos + i + 1][0])

    return res


def find_range(table, x, polynom_degree):
    pos, side = get_the_nearest_dot(table, x)

    right_indent = (polynom_degree + 1) // 2
    if side == "right":
        right_indent += (polynom_degree + 1) % 2

    left_indent = polynom_degree + 1 - right_indent

    if (pos - left_indent) < 0:
        return 0
    else:
        if (pos + right_indent) < len(table):
            return pos - left_indent
        else:
            return len(table) - polynom_degree - 1

def get_the_nearest_dot(table, x):
    i = 0
    n = len(table)
    while i < n and table[i][0] < x:
        i += 1
    if i == n:
        i -= 1
    if i > 0 and (x - table[i - 1][0]) < (table[i][0] - x):
        return i - 1, "left"
    else:
        return i, "right"


def spline_interpolation(table, x):
    pos, side = get_the_nearest_dot(table, x)

    if side == "right":
        left_pos = pos - 1
        right_pos = pos
    else:
        left_pos = pos
        right_pos = pos + 1

    a = table[left_pos][1]

    c = [0 for i in range(len(table))]
    ksi = [0 for i in range(len(table))]
    etta = [0 for i in range(len(table))]

    # h = 1 для всех i

    for i in range(2, len(table)):
        f = 3 * (table[i][1] - 2 * table[i - 1][1] + table[i - 2][1])

        ksi[i] = -1 / (ksi[i - 1] + 4)

        etta[i] = (f - etta[i - 1]) / (ksi[i - 1] + 4)

    c[len(table) - 2] = etta[len(table) - 1]

    for i in range(len(table) - 3, 0, -1):
        c[i] = ksi[i + 1] * c[i + 1] + etta[i + 1]

    i = right_pos

    b = table[i][1] - table[i - 1][1] - (c[i + 1] - 2 * c[i]) / 3

    d = (c[i + 1] - c[i]) / 3

    c = c[i]

    return a + b * (x - table[left_pos][0]) + c * (x - table[left_pos][0]) ** 2 + d * (x - table[left_pos][0]) ** 3

table = make_table_of_squares(10, 1)
print_table(table)

x1 = 0.5 # Значение аргумента х в 1-ом интервале для проведения интерполяции
x2 = 5.5 # Значение аргумента х в 6-ом интервале для проведения интерполяции

print(newton_interpolation(table, x1, 3))
print(newton_interpolation(table, x2, 3))
print(spline_interpolation(table, x1))
print(spline_interpolation(table, x2))


