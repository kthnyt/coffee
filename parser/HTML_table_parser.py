from bs4 import BeautifulSoup
# from cssutils import parseStyle
import os
import sys
import time

def get_html_style_table_elements(PATH, htm_filename):
    '''Get style and table elements from html file'''
    print('Editing: ' + htm_filename)
    # read htm file
    with open(PATH + htm_filename, 'r') as f:
        html_file = f.read()
        f.close()

    # replace '&nbsp' with ' '
    htm_filename.replace('&nbsp;', ' ')

    # parse html_file
    soup = BeautifulSoup(html_file, 'html.parser')

    # save style & table elements in new htm file
    style = soup.find('style')
    table = soup.find('table')
    
    # centering
    table = element_centering(table)

    with open(PATH + htm_filename, 'w') as f:
        f.write(str(style) + '\n\n' + str(table))
        f.close()
    print('Saved:   ' + htm_filename)

def new_filenames(htm_filenames):
    '''return only new htm filenames'''
    pass

# Centering: Make 'margin-(left and right)' = 'auto'
def element_centering(elem):
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

# get report folder from system args
if sys.argv[1]:
    PATH =  f'C:\\Users\\keith\\Google Drive\\MMS\\kp2\\tables\\tables_{sys.argv[1]}\\'
else:
    'C:\\Users\\keith\\Google Drive\\MMS\\kp2\\tables\\'

def main(PATH=PATH):
    while True:
        # Collect '.htm' filenames in list
        htm_filenames = [filename for filename in os.listdir(PATH) if filename[-4:] == '.htm']

        # each htm file
        for htm_filename in htm_filenames[:]:
            get_html_style_table_elements(PATH=PATH, htm_filename=htm_filename)

        # time delay
        time.sleep(10)


if __name__ == "__main__":
    main()
