import pdfplumber
import os
import pdf2image #poppler too
from tqdm import tqdm
import pytesseract
from ImgProcess import ImageTools

pytesseract.pytesseract.tesseract_cmd = (
    r'/usr/bin/tesseract'
)

class PDFReader:
    def __init__(self, method='tesseract_split'):
        self.method = method
    
    def pdf2img(self, pdf_path):
        return pdf2image.convert_from_path(pdf_path)

    def tesseract_OCR(self, img):
        return pytesseract.image_to_string(img)
    
    def tesseract_method(self, pdf_path):
        doc_content = ''
        images = self.pdf2img(pdf_path)
        for pg, img in tqdm(enumerate(images)):
            doc_content += str(self.tesseract_OCR(img))
        return doc_content
    
    def tesseract_split_method(self, pdf_path):
        img_tool = ImageTools()

        doc_content = ''
        images = []
        pages = self.pdf2img(pdf_path)
        for page in pages:
            images += img_tool(page)

        for pg, img in tqdm(enumerate(images)):
            doc_content += str(self.tesseract_OCR(img))
        return doc_content

    def pdfplumber_method(self, pdf_path):
        doc_content = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in range(len(pdf.pages)):
                page_content = pdf.pages[page]
                doc_content += str(page_content.extract_text())
        return doc_content

    def __call__(self, pdf_path):
        if self.method == 'tesseract':
            doc_content = self.tesseract_method(pdf_path)
        elif self.method == 'tesseract_split':
            doc_content = self.tesseract_split_method(pdf_path)
        else:
            doc_content = self.pdfplumber_method(pdf_path)
        return doc_content



if __name__ == '__main__':
    DATA_PATH = 'dataset'
    pdf_docs_list = os.listdir(DATA_PATH) 
    reader = PDFReader('pdfplumber')

    for pdf_file in pdf_docs_list:
        pdf_path = os.path.join(DATA_PATH, pdf_file)
        print(reader(pdf_path))
