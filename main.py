from reader import PDFReader
import os

DATA_PATH = 'dataset'
pdf_docs_list = os.listdir(DATA_PATH) 
reader = PDFReader()

for pdf_file in pdf_docs_list:
    pdf_path = os.path.join(DATA_PATH, pdf_file)
    print(reader(pdf_path))