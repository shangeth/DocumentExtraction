<!-- # DocumentExtraction



## Extracting PDF
1. Directly read from pdf file with pdfplumber
2. Use tesseract (pdf->img->text)

## Parsing Text


- Author
- Author Institution
- Name of Companies
- Broker Recommendation
- Target Price of Stock -->


# DocumentExtraction

This Repository contain code for extracting details such as author, author institution, companies, target price of company, BUY/SELL call from financial PDF documents.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
apt install tesseract-ocr
apt-get install poppler-utils

pip install -r requirements.txt

python -m spacy download en_core_web_trf
python -m spacy download en_core_web_sm

```
Also [install tesseract](https://github.com/UB-Mannheim/tesseract/wiki) on your Windows device and add the path to the script with

```python
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    # path to .exe file in windows
    r"C:\Users\user\Programs\Tesseract-OCR\tesseract.exe"

    # Linux('which tesseract' to get the path, after installing tesseract)
    r"/usr/bin/tesseract" 
)
```
**NOTE:** pytesseract is only necessary for methods using Tesseract-OCR.

## Usage

### ImageTools
```python
from ImgProcess import ImageTools

# split the document image into region of interest
# avoid useless parts of the document

pdf_image = 'path to image of document'
img_tool = ImageTools()
doc_imgs = img_tool(pdf_image)
```
![](assets/img_tool1.png)
![](assets/img_tool2.png)
![](assets/img_tool3.png)


### PDFReader
```python
from reader import PDFReader

# returns the text content in a PDF file using ImageTools
# 3 available methods
# - pdfplumber
# - pytesseract
# - pytesseract_split

reader = PDFReader(pdf_method='tesseract_split')
text_content = reader('path_to_pdf_document')
```

### EntityRecognition
```python
from NER import EntityRecognition

# extracts the details from the text content 
ER = EntityRecognition(pdf_method='tesseract_split')
author_institution, author, companies, target = ER(text_content)
```


```bash
# Extract details from a single pdf file
python main.py ----pdf_method='tesseract_split' --pdf_file='path_to_pdf'

# Extract details from a directory of pdf files
python main.py ----pdf_method='tesseract_split' --pdf_dir='path_to_pdf_dir'

# Extract details from a directory of pdf files to CSV file
python results.py ----pdf_method='tesseract_split' --pdf_dir='path_to_pdf_dir' --csv_path='path_to_csv'
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)