class star:
    # Base class for a single action in a formation. Contains nodes this star point to.
    def __init__(self):
        self._nodes = []

    def action(self, input):
        return input