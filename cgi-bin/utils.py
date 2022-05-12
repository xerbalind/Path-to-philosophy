def between_braces(start_index, stop_index, string) -> bool:
    """Kijkt of een stuk tekst tussen haakjes staat."""

    # Tel het aantal open en sluitende accolades tussen start en stop
    open_brace = 0
    close_brace = 0
    for i in string[start_index:stop_index]:
        if i == "(":
            open_brace += 1
        elif i == ")":
            close_brace += 1
    # als het aantal open accolades groter is dan  het aantal sluitende accolades, zit de link tussen de accolades
    return open_brace > close_brace
