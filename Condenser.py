"""
This class describes condenser whose outlet stream is saturated liquid
"""
from Stream import Stream


class Condenser:
    st_i = Stream()
    st_o = Stream()
    st_o.x = 0
