import streamlit as st  # type: ignore
from matplotlib import pyplot as plt  # type: ignore

from ..matplotlib import DrawOptions
from ..typing import BBLike


def draw(obj, bb: BBLike = None, ax=None, options: DrawOptions = None):
    """
    Draw Easymunk object using matplotlib.
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    options = options or DrawOptions(ax, bb=bb)
    options.draw_object(obj)

    st.pyplot(fig)
