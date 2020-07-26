
class APIChangedError(Exception):
    def __init__(self, message="PyPI API Response format probably changed"):
        self.message = message
        super().__init__(self.message)
