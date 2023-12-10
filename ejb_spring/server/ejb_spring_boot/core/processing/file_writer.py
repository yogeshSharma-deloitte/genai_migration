import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("file_writer")

def write_to_file(content, fileName):
    file = open(fileName, 'w')
    file.write(content)
    file.close()

def write_to_html_file(content, fileName):
    with open(fileName, 'w', encoding='utf-8') as html_file:
            html_file.write(content)    
