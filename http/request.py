CORRECT_STRING = '<a href="https://www.google.com/?gws_rd=ssl">here</a>.'

def _returned_correct_data(data) -> bool:
    """
    Write this doc-string.
    """

    if CORRECT_STRING in data:
        return True
    return False