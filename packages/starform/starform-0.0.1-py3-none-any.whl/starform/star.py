class star:
    # Base class for a single action in a formation. Contains nodes this star point to.
    def __init__(self):
        self._nodes = []

    def link(self, star2):
        # Chain stars. Execution star.action() -> star2.action()
        self._nodes.append(star2)
        return self

    def unlink(self, star2):
        # Chain stars. Execution star.action() -> star2.action()
        self._nodes.remove(star2)
        return self

    def action(self, s):
        return s
