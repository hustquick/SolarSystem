class AirPipe:
    """AirPipe This class is used to describe the air pipe in dish receiver
    """

    def __init__(self, d_i=0.07, delta_a=0.002, alpha=0.87):
        self.d_i = d_i
        self.delta_a = delta_a
        self.alpha = alpha
        self.temperature = None
