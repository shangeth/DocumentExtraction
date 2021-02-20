import nltk
import spacy
import os
from reader import PDFReader
from collections import Counter
from tqdm import tqdm
import re
from spacy.matcher import Matcher
import pandas as pd

class EntityRecognition:
    def __init__(self, bse_csv='bse_companies.csv', pdf_method=None, only_bse=True):
        self.nlp = spacy.load("en_core_web_trf")
        self.match_nlp = spacy.load("en_core_web_sm")
        self.bse_csv = bse_csv
        self.pdf_method = pdf_method
        self.only_bse = only_bse

    def clean(self, text):
        # removing paragraph numbers
        text = re.sub('[0-9]+.\t','',str(text))
        # removing new line characters
        text = re.sub('\n ','',str(text))
        text = re.sub('\n',' ',str(text))
        # removing apostrophes
        text = re.sub("'s",'',str(text))
        # removing hyphens
        text = re.sub("-",' ',str(text))
        text = re.sub("— ",'',str(text))
        # removing quotation marks
        text = re.sub('\"','',str(text))
        # removing salutations
        text = re.sub("Mr\.",'Mr',str(text))
        text = re.sub("Mrs\.",'Mrs',str(text))
        # removing any reference to outside text
        text = re.sub("[\(\[].*?[\)\]]", "", str(text))
        # remove unnecessary symbols
        text = re.sub('[^.@a-zA-Z0-9 \n\.]', '', text)
        
        return text
    def get_target(self, content):
        
        content = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", content).strip()
        doc = self.match_nlp(content)
        pattern = [{'LOWER': 'target'}, {'LOWER': 'price', 'OP' : '*'} ,{'LOWER': 'of', 'OP' : '*'}, {'LOWER': 'rs', 'OP' : '*'},{'IS_SPACE': True, 'OP' : '*'},{'LIKE_NUM' : True}]
        matcher = Matcher(self.match_nlp.vocab)
        matcher.add('target_price', [pattern])
        content = self.match_nlp(content)
        matches = matcher(content)
        return matches, doc

    def get_author(self, content):
        doc = self.match_nlp(content)
        pattern = [
            # {'IS_SENT_START': True}, 
            {'IS_ALPHA': True, 'OP' : '?'},
            {'IS_SPACE': True, 'OP' : '?'} ,
            {'IS_ALPHA': True},
            {'IS_SPACE': True, 'OP' : '*'} ,
            {'IS_ALPHA': True},
            {'IS_SPACE': True, 'OP' : '*'} ,
            {'LIKE_EMAIL': True,}, 
        ]
        matcher = Matcher(self.match_nlp.vocab)
        matcher.add('authors', [pattern])
        content = self.match_nlp(content)
        matches = matcher(content)
        return matches, doc

    def filter_companies(self, companies, author_institution):
        bse_df = pd.read_csv(self.bse_csv, encoding='latin-1')

        final_company_list = []
        for company in companies:
            if author_institution in company:
                continue
            elif any(list(map(lambda x: x.startswith(company), bse_df['Company Name']))):
                final_company_list.append(company)
        return final_company_list


    def __call__(self, content):
        content = self.clean(content)

        if self.pdf_method == 'tesseract_split':
            authors = []
        targets = []
        orgs = []
        persons = []
        content_list = content.split(' ')
        for i in tqdm(range(int(len(content.split(' '))/512)+1)):
            content = ' '.join(content_list[i*512 : (i+1)*512])
            doc = self.nlp(content)
            
            for entity in doc.ents:
                if entity.label_ == 'ORG':
                    orgs.append(entity.text)
                if entity.label_ == 'PERSON':
                    persons.append(entity.text)
                
            # target 
            tar_vals, doc = self.get_target(content)
            if tar_vals:
                target = doc[tar_vals[0][1]:tar_vals[0][2]][-1]
                targets.append(int(str(target)))

            if self.pdf_method == 'tesseract_split':
                # author
                aut_vals, doc = self.get_author(content)
                if aut_vals:
                    for i in range(len(aut_vals)):
                        aut = doc[aut_vals[i][1]:aut_vals[i][2]-1]
                        authors.append(str(aut).strip())

        # print(authors)
        org_counter = Counter(orgs)
        author_institution = org_counter.most_common(1)[0][0]

        person_counter = Counter(persons)
        min_threshold = 1
        person_counter = {x: count for x, count in dict(person_counter).items() if count >= min_threshold and len(x.split(' '))>=2}
        author = list(person_counter.keys())
        # print(author)
        
        if self.pdf_method == 'tesseract_split':
            new_authors = []
            # author = list(set(author).intersection(authors))
            for a in author:
                if any(str(a.split(' ')[-1]) in string for string in authors):
                    new_authors.append(a)



        # author = person_counter.most_common(1)[0][0]
        companies = list(set(orgs))
        if self.only_bse:
            companies = self.filter_companies(companies, author_institution)
        if author_institution == []:
            author_institution = 'Other'
        return author_institution, new_authors, companies, list(set(targets))
    



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