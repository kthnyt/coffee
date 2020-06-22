import os
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath('..\\parser\\'))
from tables import Table

PATH = "..\\html\\GIP_1_mill_lock_up_v03.htm"

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

def test_decompose_links():
    decomposed_table = table._decompose_xmlns_link(table._build_doc())
    links = decomposed_table.find_all('link')

    assert(not links) 