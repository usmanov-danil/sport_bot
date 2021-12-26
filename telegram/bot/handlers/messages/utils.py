def is_valid_weight(weight: str):
    return weight.replace('.', '').isnumeric() and float(weight) > 0 and float(weight) < 200


def is_valid_height(height: str):
    return height.isnumeric() and int(height) > 0 and int(height) < 300


def is_valid_years(years: str):
    return years.isnumeric() and int(years) > 0 and int(years) < 100
