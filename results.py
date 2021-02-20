from reader import PDFReader
from NER import EntityRecognition
import os
import argparse
import pandas as pd

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser(description='Input Arguments')
    parser.add_argument('--pdf_dir', type=str, default='dataset', help='path to directory containing pdf files')
    parser.add_argument('--pdf_file', type=str, default=None, help='path to pdf file')
    parser.add_argument('--pdf_method', type=str, default='tesseract_split', help="Method of pdf text extraction ('pdfplumber', 'tesseract', 'tesseract_split')")
    parser.add_argument('--csv_path', type=str, default='results.csv', help="nam/path to results csv file")
    args = parser.parse_args()

    pdf_dir = args.pdf_dir
    pdf_file = args.pdf_file
    pdf_method = args.pdf_method
    csv_path = args.csv_path

    file_names = []
    author_instis = []
    authors = []
    targets = []
    companiess = []

    if pdf_file:
        reader = PDFReader(pdf_method)
        ER = EntityRecognition(pdf_method=pdf_method)
        txt = reader(pdf_file)
        author_institution, author, companies, target = ER(txt)
        file_names.append(pdf_file)
        author_instis.append(author_institution)
        authors.append(author)
        companiess.append(companies)
        targets.append(target)

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
            file_names.append(pdf_file)
            author_instis.append(author_institution)
            authors.append(author)
            companiess.append(companies)
            targets.append(target)
            print(f"\nAuthor Institution of the pdf file '{pdf_file}' = '{author_institution}'")
            print('Target = ', target)
            print('Author = ', author)
            print('Companies = ', companies)


    df = pd.DataFrame(list(zip(file_names, authors, author_instis, companiess, targets)), 
               columns =['File Name', 'Authors', 'Author Institution', 'Companies', 'Target Price']) 
    df.to_csv(csv_path)