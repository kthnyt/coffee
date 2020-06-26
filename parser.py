import os

def _read(obj):
    """
    Try to read from a url, file or string.
    Parameters
    ----------
    obj : str, unicode, or file-like
    Returns
    -------
    raw_text : str
    """
    from pandas.io.common import is_url, urlopen

    if is_url(obj):
        with urlopen(obj) as url:
            text = url.read()
    elif hasattr(obj, "read"):
        text = obj.read()
    elif isinstance(obj, (str, bytes)):
        text = obj
        try:
            if os.path.isfile(text):
                with open(text, "rb") as f:
                    return f.read()
        except (TypeError, ValueError):
            pass
    else:
        raise TypeError(f"Cannot read object of type '{type(obj).__name__}'")
    return text

class Table:
    '''Base class to parse a custom HTML <table> into a HTML WIRE tile.
    Parameters
    ----------
    io : str or file-like
        This can be either a string of raw HTML, a valid URL using the HTTP,
        FTP, or FILE protocols or a file-like object.
    encoding : str
        Encoding to be used by parser (default: 'windows-1252')
        
    Attributes
    ----------
    io : str or file-like
        raw HTML, URL, or file-like object
    encoding : str
        Encoding to be used by parser
    '''

    def __init__(self, io, encoding='windows-1252'):
        self.io = io
        self.encoding = encoding

    def _decompose_xmlns_link(self, doc):
        links = doc.find_all('link')

        if not links:
            raise ValueError("No links found")
        
        for link in links:
            link.decompose()

        return doc

    def _remove_html_xmlns_attrs(self, doc):
        doc.html.attrs = {}
        return doc

    def _setup_build_doc(self):
        raw_text = _read(self.io)
        if not raw_text:
            raise ValueError(f"No text parsed from document: {self.io}")
        return raw_text

    def _build_doc(self):
        from bs4 import BeautifulSoup
        return BeautifulSoup(self._setup_build_doc(), features='html5lib',
                                from_encoding=self.encoding)

