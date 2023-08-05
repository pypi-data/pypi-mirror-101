from starformation.star import star


class CStar(star):
    # Wrap custom function
    def __init__(self, func):
        super().__init__()
        self.func = func

    def action(self, *args, **kwargs):
        return self.func(*args, **kwargs)

