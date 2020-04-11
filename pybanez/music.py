from pybanez.settings import NOTES, STEPS

class Scale:
    """Musical scale for both Major and Minor types.

    Attributes
    ----------
    root : str
        The root note of the scale.

    demarcation : str {`Major`, `Minor`}
        The note demarcation of the scale.

    steps : list
        Index positions of whole and half notes for the demarcation specified.

    notes : list
        Notes belonging to the initialised scale.
    """

    def __init__(self, root, demarcation):
        """
        Parameters
        ----------
        root : str
            The root note of the scale.

        demarcation : str {`Major`, `Minor`}
            The note demarcation of the scale.
        """
        self.root = root
        self.demarcation = demarcation
        self.steps = STEPS[self.demarcation]
        self.notes = self._generate_scale_notes()

    def _generate_scale_notes(self):
        """Create list of notes for the root and demarcation provided.

        Returns
        -------
        scale_notes : list
            List of all notes in the scale specified.
        """
        start_index = NOTES.index(self.root)
        scale_notes = [NOTES[i + start_index] for i in self.steps]
        return scale_notes
