from point import Point


def extract_details(user_input: str) -> tuple[str, float, float]:
    """
    Extract the name and the coordinates from the user input
    :param user_input:
    :return:   name, x, y
    """
    # Split the expression by '=' to separate the name and the point creation
    name, point_str = user_input.split('=')

    # Strip whitespace from name
    name = name.strip()

    # Remove leading and trailing whitespaces and split the point string by ';'
    sep = ';' if ';' in point_str else ','
    point_str = point_str.strip()[len('Point('):-1]
    x_str, y_str = point_str.split(sep)

    try:
        x = float(x_str)
        y = float(y_str)
        return name, x, y
    except ValueError:
        raise ValueError("Les coordonnées doivent être des nombres")


def read_point_input() -> Point:
    """
    Read a point from the user input
    :return: A point object
    """
    user_input = input(f"Declarer un point: \n")
    name, x, y = extract_details(user_input)
    return Point(name, x, y)
