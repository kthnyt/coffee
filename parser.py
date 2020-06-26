import os
from cssutils import parseStyle


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
        self.text = ''

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

    def apply_responsive_table_width(self, elem):
        elem['style']
        elem_style = parseStyle(elem['style'])
        elem_width_pt = elem_style['width'] #pt

        cols = elem.find_all('col')
        for col in cols:
            col_style = parseStyle(col['style'])
            col_width_pt = col_style['width'] #pt
            col_width_pct = 100 * float(col_width_pt.rstrip('pt')) / float(elem_width_pt.rstrip('pt'))
            col_width_pct = str(round(col_width_pct, 1)) + '%'
            col_style['width'] = col_width_pct
            col['style'] = col_style.cssText

        elem_width_pct = 100 * float(elem_width_pt.rstrip('pt')) / float(elem_width_pt.rstrip('pt'))
        elem_width_pct = str(round(elem_width_pct, 1)) + '%'
        elem_style['width'] = elem_width_pct
        elem['style'] = elem_style.cssText
        return elem

    # Apply table centering
    def align_element_center(self, elem):
        '''Takes a BeautifulSoup elemnt and adds centering'''
        try:
            if ('margin-left' not in elem['style']):
                elem['style'] += ';margin-left: auto'

            if ('margin-right' not in elem['style']):
                elem['style'] += ';margin-right: auto'

            assert(';margin-left: auto;margin-right: auto' in elem['style'])
        except:
            print('Custom ERROR: problem centering element')

        return elem

    def _extract_style_and_table_elems(self, doc):
        # save style & table elements in new htm file
        style = doc.find('style')
        table = doc.find('table')

        # centering
        table = self.align_element_center(table)

        # max table width
        table = self.apply_responsive_table_width(table)

        doc_text = str(style) + '\n\n' + str(table)
        self.text = doc_text
        return doc_text

    def _setup_build_doc(self):
        raw_text = _read(self.io)
        if not raw_text:
            raise ValueError(f"No text parsed from document: {self.io}")
        self.text = raw_text
        return raw_text

    def _build_doc(self):
        from bs4 import BeautifulSoup
        return BeautifulSoup(self._setup_build_doc(), features='html5lib',
                                from_encoding=self.encoding)

