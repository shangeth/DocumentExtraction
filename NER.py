import nltk
import spacy
import os
from reader import PDFReader
from collections import Counter
from tqdm import tqdm

class EntityRecognition:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")

    def __call__(self, content):
        orgs = []
        persons = []
        content_list = content.split(' ')
        for i in tqdm(range(int(len(content.split(' '))/512))):
            content = ' '.join(content_list[i*512 : (i+1)*512])
            doc = self.nlp(content)
            
            for entity in doc.ents:
                # print(entity.label_, entity.text)
                if entity.label_ == 'ORG':
                    orgs.append(entity.text)
                if entity.label_ == 'PERSON':
                    persons.append(entity.text)

        org_counter = Counter(orgs)
        author_institution = org_counter.most_common(1)[0][0]

        person_counter = Counter(persons)
        print(person_counter)
        return author_institution

if __name__ == '__main__':
    DATA_PATH = 'dataset'
    pdf_docs_list = os.listdir(DATA_PATH) 
    reader = PDFReader()
    ER = EntityRecognition()

    for pdf_file in pdf_docs_list:
        pdf_path = os.path.join(DATA_PATH, pdf_file)
        txt = reader(pdf_path)
        author_institution = ER(txt)
        print(f"Author Institution of the pdf file '{pdf_file}' = '{author_institution}'")