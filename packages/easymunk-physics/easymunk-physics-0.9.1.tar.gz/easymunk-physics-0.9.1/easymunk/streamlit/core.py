import streamlit as st
from matplotlib import pyplot as plt

from ..matplotlib import DrawOptions
from ..typing import BBLike


def draw(obj, bb: BBLike = None, ax=None, options=None):
    """
    Draw Easymunk object using matplotlib.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    options: DrawOptions = options or DrawOptions(ax, bb=bb)
    options.draw_object(obj)

    st.pyplot(fig)
