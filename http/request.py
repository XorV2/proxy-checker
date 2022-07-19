CORRECT_STRING = '<a href="https://www.google.com/?gws_rd=ssl">here</a>.'

def _returned_correct_data(data) -> bool:
    """
    Checks if the data is correct by checking if the correct
    string is returned. If the correct string is returned
    the function returns true. Otherwise it returns false.
    """

    return CORRECT_STRING in data