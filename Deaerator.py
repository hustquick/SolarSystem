"""
This class describes the deaerator
"""
from Stream import Stream


class Deaerator:
    st_i = Stream()
    st_o = Stream()
    st_o.x = 0

    def __init__(self, P):
        self.P = P
