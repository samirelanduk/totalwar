class SaveFile:
    """A representation of a RTW .sav file."""

    def __init__(self, bytestring):
        self.contents = bytestring
