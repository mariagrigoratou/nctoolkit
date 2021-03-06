
from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this


def zip(self):
    """
    Zip the dataset

    """
    self._zip = True

    if len(self.history) == len(self._hold_history):
        cdo_command = "cdo copy "
        run_this(cdo_command, self, output="ensemble")
