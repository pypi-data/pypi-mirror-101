class Stats:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

