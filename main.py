from pybanez.music import Scale
from pybanez.utilities import shared_notes
from pybanez.instrument import Guitar

# Generate some musical keys
a_maj = Scale('A', 'Major')
d_maj = Scale('D', 'Major')
e_maj = Scale('E', 'Major')

# Check the overlap of different scale
scale_overlap = shared_notes(d_maj.notes, e_maj.notes)
a = shared_notes(d_maj.notes)

# create a guitar with given tuning
bass = Guitar(tuning=list('EADG'), n_frets=15)
tab = bass.tab_notes(notes=a_maj.notes, start=[0, 5])

