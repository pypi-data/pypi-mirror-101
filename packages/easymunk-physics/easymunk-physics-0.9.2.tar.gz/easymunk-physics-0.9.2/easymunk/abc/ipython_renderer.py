class IPythonRenderer:
    """
    IPython renderer interface.
    """

    def _impl(self):
        raise AttributeError()

    empty_renderer = True
    html = _impl
    javascript = _impl
    svg = _impl
    png = _impl
    jpeg = _impl
