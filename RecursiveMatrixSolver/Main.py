from decimal import Decimal


def main():
    # Welcome message / instructions
    print("Welcome! This program converts recursive matrix formulas into simple equations!")
    print("To start, please enter the values of the matrix, as well as the initial recursive case.")
    print("x(1) = [a b]x0; x(0)=[?]")
    print("y(1) = [c d]y0; y(0)=[?]")
    print("")

    # Prompt for values
    a = Decimal(input("Enter a value for a: "))
    b = Decimal(input("Enter a value for b: "))
    c = Decimal(input("Enter a value for c: "))
    d = Decimal(input("Enter a value for d: "))

    x0 = Decimal(input("Enter an initial value for the sequence (value for x0): "))
    y0 = Decimal(input("Enter an initial value for the sequence (value for y0): "))

    print("Calculating solution...")

    # Calculate values
    eigen_values = calculate_eigen_values(a, b, c, d)
    eigen_vectors = calculate_eigen_vectors(a, b, eigen_values)
    coefficients = calculate_coefficients(x0, y0, eigen_vectors)

    # Create formulas
    x = lambda n: float(coefficients[0] * ((eigen_values[0]) ** n) * eigen_vectors[0][0] + coefficients[1] * (
            (eigen_values[1]) ** n) * eigen_vectors[1][0])
    y = lambda n: float(coefficients[0] * ((eigen_values[0]) ** n) * eigen_vectors[0][1] + coefficients[1] * (
            (eigen_values[1]) ** n) * eigen_vectors[1][1])

    # Print results
    print("Done calculating!")
    print("")
    print("The formula is as follows:")

    # Print formulas
    print_formulas(eigen_values, eigen_vectors, coefficients)
    print("")
    response = input("Enter a value of n to run through the formulas. Enter \"q\" to quit: ")

    while response != "q":
        num = Decimal(response)

        print("[x(" + str(num) + ")] = " + str(x(num)))
        print("[y(" + str(num) + ")] = " + str(y(num)))

        print("")
        response = input("Enter another value for n (or \"q\" to quit): ")

    print("Goodbye!")


def print_formulas(eigen_values, eigen_vectors, coefficients):
    formula_x_start = "(%s)*(%s)^n*" % (format_value(coefficients[0]), format_value(eigen_values[0]))
    formula_x_mid = "[%s] + (%s)*(%s)^n*" % (
    format_value(eigen_vectors[0][0]), format_value(coefficients[1]), format_value(eigen_values[1]))
    formula_x_end = "[%s]" % format_value(eigen_vectors[1][0])

    print("[x(n)] = " + formula_x_start + formula_x_mid + formula_x_end)

    padding = format_padding(len(formula_x_start))
    formula_y_start = padding + "[%s]" % format_value(eigen_vectors[0][1])

    padding = format_padding(len(formula_x_start) + len(formula_x_mid) - len(formula_y_start))
    formula_y_end = padding + "[%s]" % format_value(eigen_vectors[1][1])

    print("[y(n)] = " + formula_y_start + formula_y_end)


def format_padding(amount):
    padding = ""

    for i in range(amount):
        padding += " "

    return padding


def format_value(val):
    num = float(val)

    # TODO express decimals as fractions

    return str(num)


def calculate_eigen_values(a, b, c, d):
    # Solve for eigen values (find values for when the determinant of (A-LI) is 0)
    # 0 = (a-L)(d-L)-bc
    # 0 = a(d-L)-L(d-L)-bc
    # 0 = ad-aL-dL+L^2-bc
    # 0 = L^2+(-a-d)L+ad-bc
    return calculate_quadratic(1, -a - d, (a * d) - (b * c))


def calculate_eigen_vectors(a, b, eigen_values):
    # Solve for eigen vectors
    vectors = list()

    for value in eigen_values:
        # q[a, c] + r[b, d] = 0
        # Solve for q and r

        q = b
        r = value - a

        # Find GCD

        vectors.append([q, r])

    return vectors


def calculate_coefficients(x0, y0, eigen_vectors):
    # x0 = c1[v] + c2[v]

    x = Decimal(x0)
    y = Decimal(y0)

    v1 = Decimal(eigen_vectors[0][0])
    v2 = Decimal(eigen_vectors[1][0])
    v3 = Decimal(eigen_vectors[0][1])
    v4 = Decimal(eigen_vectors[1][1])

    c2 = (y - (v3 / v1) * x) / (v4 - (v3 * v2) / v1)
    c1 = (x - v2 * c2) / v1

    return [c1, c2]


def calculate_quadratic(a, b, c):
    values = list()

    d = (b ** 2) - (4 * a * c)  # discriminant

    values.append((-b - d ** Decimal('0.5')) / (2 * a))
    values.append((-b + d ** Decimal('0.5')) / (2 * a))

    return values


if __name__ == "__main__":
    main()
