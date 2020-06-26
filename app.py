import os
import sys
import numpy as np
from bs4 import BeautifulSoup

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from parser import Table


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    return render_template('parser.html', result=result)

@app.route('/parser', methods=['GET', 'POST'])
def parser():
    result = ''
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        table = Table(f.filename)
        result = table._extract_style_and_table_elems(table._build_doc())
        with open('./templates/table_frame.html', 'w') as f:
            f.write(result)
            
        os.remove(f.filename)

    return render_template('parser.html', result=result)

@app.route('/table')
def table():
    return render_template('table.html')


if __name__ == '__main__':
    app.run()