import os
import sys
from bs4 import BeautifulSoup

from parser import Table

PATH = "..\\html\\GIP_1_mill_lock_up_v03.htm" # Windows
PATH = "GIP_1_mill_lock_up_v03.htm" # Ubuntu

table = Table(PATH)

def test_build_doc_soup():
    soup = table._build_doc()

    assert(isinstance(type(soup), type(BeautifulSoup)))

def test_soup_contains_links_():
    links = []
    soup = table._build_doc()
    links = soup.find_all('link')

    assert(len(links) ==1)

def test_decompose_links_soup():
    decompose_soup = table._decompose_xmlns_link(table._build_doc())

    assert(isinstance(type(decompose_soup), type(BeautifulSoup)))

def test_decomposed_links():
    decomposed_table = table._decompose_xmlns_link(table._build_doc())
    links = decomposed_table.find_all('link')

def test_remove_html_attrs():
    decomposed_table = table._decompose_xmlns_link(table._build_doc())
    html = decomposed_table.html
    
    assert('xmlns' in html.attrs)

    
def test_remove_html_attrs():
    removed_table = table._remove_html_xmlns_attrs(table._decompose_xmlns_link(table._build_doc()))
    html = removed_table.html
    
    assert('xmlns' not in html.attrs)