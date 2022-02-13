def replace_operators(text):
    return text.replace("*", "×").replace("/", "÷")


def replace_decimal(match):
    return f"Decimal(\"{match.group(1)}\")"


def evaluate(operation):
    # TODO improve calculation of decimal numbers

    result = eval(operation)

    return str(result)
