import pdfplumber
import os
import pdf2image #poppler too
import pytesseract

class PDFReader:
    def __init__(self,):
        pass

    def __call__(self, pdf_path):
        doc_content = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in range(len(pdf.pages)):
                page_content = pdf.pages[page]
                doc_content += str(page_content.extract_text())
        return doc_content

class PDFTesseractReader:
    def __init__(self,):
        pass
    
    def pdf2img(self, pdf_path):
        return pdf2image.convert_from_path(pdf_path)

    def tesseract_OCR(self, img):
        return pytesseract.image_to_string(img)

    def __call__(self, pdf_path):
        doc_content = ''
        images = self.pdf2img(pdf_path)
        for pg, img in enumerate(images):
            doc_content += str(self.tesseract_OCR(img))
        return doc_content



if __name__ == '__main__':
    DATA_PATH = 'dataset'
    pdf_docs_list = os.listdir(DATA_PATH) 
    reader = PDFReader()

    for pdf_file in pdf_docs_list:
        pdf_path = os.path.join(DATA_PATH, pdf_file)
        print(reader(pdf_path))
