import numpy as np
from random import choice

from pybanez.settings import NOTES, N_NOTES


class Guitar:

    def __init__(self, tuning, n_frets):
        """
        Parameters
        ----------
        tuning : list[str]
            Each entry is the tuning of the open note.

        n_frets : int
            The number of frets on the fretboard
        """
        self.tuning = tuning
        self.n_frets = n_frets
        self.strings = self.tune_guitar(self.tuning)

    def tune_guitar(self, tuning):
        """Sets the tuning of the guitar and note positions on the fret board.
        Assumes a 24 fret board (i.e. 2 repetitions of the 12 notes per string)

        Parameters
        ----------
        tuning : list
            List of notes which the open strings (index 0) will be set as.

        Returns
        -------
        strings : np.array(), shape( len(string), num_strings )
            Nested list of lists, each list is a string starting with the open note.
            Final array is sliced to only return up to the number of frets specified
        """
        strings, _repetitions = [], 2
        for t in tuning:
            start = NOTES.index(t)
            string = NOTES[start:start + N_NOTES] * _repetitions
            strings.append(string)
        return np.array(strings)[:, :self.n_frets + 1]  # + 1 to account for open string as note but not fret

    def set_tuning(self, tuning):
        """Re-tunes the guitar. Will update the strings to the tuning also.

        Parameters
        ----------
        tuning : list
            List of notes which the open strings (index 0) will be set as.

        Returns
        -------
        None
        """
        self.tuning = tuning
        self.strings = self.tune_guitar(self.tuning)

    def _note_positions(self, note):
        """Determine the fretboard coordinates of the passed note

        Parameters
        ----------
        note : str
            Name of the note to locate within the instrument strings.

        Returns
        -------
        positions : np.array(), shape(string_index, fretboard_index)
            2D coordinates on the fretboard of the positions the note is located at.
        """
        positions = np.vstack(np.where(self.strings == note)).T
        return positions

    def _determine_next_note(self, next_note, curr_position, span=1):
        """Given the name of the next note and the current fretboard position, find closest fretboard position
        of next note using euclidean distance.

        Parameters
        ----------
        next_note : str
            Note to move to on the fretboard.

        curr_position : np.array(), [string_index, note_index]
            Position of current note on fretboard.

        span : int, default = 1
            The number of strings either side of the current string which the new position can be.
            i.e. if current string index is 2 then allowed strings are {1, 2, 3}

        Returns
        -------
        closest_position : np.array() [string_index, note_index]
            Position of closest note on fretboard.
        """
        string = curr_position[0]
        valid_coords = self._note_positions(next_note)
        transition_limits = [True if (string - span) <= i[0] <= (string + span) else False for i in valid_coords]
        limited_coords = valid_coords[transition_limits]
        distances = np.linalg.norm(limited_coords - curr_position, axis=1)
        closest_position = valid_coords[np.argmin(distances)]
        return closest_position

    def tab_notes(self, notes, start=None, span=1):
        """Return the fret positions of the passed notes where the position of the next note is determined.
        User is able to set the start position of the first note, otherwise a random position is generated
        based on the first note of user input.

        Parameters
        ----------
        notes : list[str]
            list of notes to be tabulated

        start : tuple, default = None,
            Position for the first note to be placed at must be `shape(string_index, fretboard_index)`

        span : int, default = 1
            The number of strings which user could move between for any given note
            i.e. if current string index was 2 then:
                span = 0 --> {3}
                span = 1 --> {2, 3, 4}
                span = 2 --> {1, 2, 3, 4, 5}

        Returns
        -------
        tabbed : np.array(), shape(len(notes), 2)
            Tabulated coordinates of the notes passed by user
        """
        if len(notes) == 0:
            return np.array([])

        curr_position = np.array(start) if start else choice(self._note_positions(notes[0]))
        tabbed = curr_position.copy()

        for current_note, next_note in zip(notes[:-1], notes[1:]):
            next_position = self._determine_next_note(next_note, curr_position)
            tabbed = np.vstack((tabbed, next_position))

        return tabbed
