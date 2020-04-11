
def shared_notes(*args):
    """Identify notes belonging to all multiple passed lists of notes.

    Parameters
    ----------
    *args : list, shape(num_notes, )
        1D List of notes.

    Returns
    -------
    unique_notes : list shape(num_unique_notes, )
        Alphabetically sorted list of notes which are present in all `*args`
    """
    combined_notes = []
    for a in args:
        combined_notes += a
    unique_notes = sorted(list(set(combined_notes)))
    return unique_notes

