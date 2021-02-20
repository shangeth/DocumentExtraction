from reader import PDFReader
from NER import EntityRecognition
import os


if __name__ == '__main__':
    DATA_PATH = 'dataset'
    pdf_docs_list = os.listdir(DATA_PATH) 
    reader = PDFReader('pdfplumber')
    ER = EntityRecognition()

    for pdf_file in pdf_docs_list:
        pdf_path = os.path.join(DATA_PATH, pdf_file)
        txt = reader(pdf_path)
        author_institution, author, companies, target = ER(txt)
        print(f"\nAuthor Institution of the pdf file '{pdf_file}' = '{author_institution}'")
        print('Target = ', target)
        print('Author = ', author)
        print('Companies = ', companies)
        # break