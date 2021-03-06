from reader import PDFReader
from NER import EntityRecognition
import os
import argparse

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser(description='Input Arguments')
    parser.add_argument('--pdf_dir', type=str, default='dataset', help='path to directory containing pdf files')
    parser.add_argument('--pdf_file', type=str, default=None, help='path to pdf file')
    parser.add_argument('--pdf_method', type=str, default='tesseract_split', help="Method of pdf text extraction ('pdfplumber', 'tesseract', 'tesseract_split')")
    args = parser.parse_args()

    pdf_dir = args.pdf_dir
    pdf_file = args.pdf_file
    pdf_method = args.pdf_method

    if pdf_file:
        reader = PDFReader(pdf_method)
        ER = EntityRecognition(pdf_method=pdf_method)
        txt = reader(pdf_file)
        author_institution, author, companies, target = ER(txt)
        print(f"\nAuthor Institution of the pdf file '{pdf_file}' = '{author_institution}'")
        print('Target = ', target)
        print('Author = ', author)
        print('Companies = ', companies)

    else:        
        pdf_docs_list = os.listdir(pdf_dir) 
        reader = PDFReader(pdf_method)
        ER = EntityRecognition(pdf_method=pdf_method)

        for pdf_file in pdf_docs_list:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            txt = reader(pdf_path)
            author_institution, author, companies, target = ER(txt)
            print(f"\nAuthor Institution of the pdf file '{pdf_file}' = '{author_institution}'")
            print('Target = ', target)
            print('Author = ', author)
            print('Companies = ', companies)
