import spacy
from spacy.matcher import Matcher
import re

def clean(text):
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

nlp = spacy.load("en_core_web_trf")

text = '  Research Analysts  Prakash Gaurav Goel prakash.goel@icicisecurities.com 91 22 6637 7373  Apoorva Bahadur  apoorva.bahadur@icicisecurities.com  91 22 6637 7419  '
text = clean(text)
# print(text)
doc = nlp(text)

pattern = [
    # {'IS_SENT_START': True}, 
    {'IS_ALPHA': True, 'OP' : '*'},
    {'IS_SPACE': True, 'OP' : '*'} ,
    {'LIKE_EMAIL': True}, 
]
    

matcher = Matcher(nlp.vocab)
matcher.add('target', [pattern])

new_doc = nlp(text)

# print(new_doc)
matches = matcher(new_doc)
print(matches)
print(new_doc[matches[-1][1]:matches[-1][2]])


# import spacy
# from spacy.matcher import DependencyMatcher
# nlp = spacy.load("en_core_web_sm")
# matcher = DependencyMatcher(nlp.vocab)

# pattern = [
#     {
#         "RIGHT_ID": "anchor_reported",
#         "RIGHT_ATTRS": {"ORTH": "reported"}
#     },
#     {
#         "LEFT_ID": "anchor_reported",
#         "REL_OP": ">>",
#         "RIGHT_ID": "founded_subject",
#         "RIGHT_ATTRS": {"DEP": "nsubj"},
#     },
#     {
#         "LEFT_ID": "anchor_reported",
#         "REL_OP": ">",
#         "RIGHT_ID": "founded_object",
#         "RIGHT_ATTRS": {"DEP": "dobj"},
#     },
#     # {
#     #     "LEFT_ID": "founded_object",
#     #     "REL_OP": ">",
#     #     "RIGHT_ID": "founded_object_modifier",
#     #     "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
#     # }
# ]


# l = 'AdaniPower reported EBITDA of Rs15.6bn in Q1FY18'

# matcher.add("FOUNDED", [pattern])
# doc = nlp(l)
# matches = matcher(doc)

# # print(matches) # [(4851363122962674176, [6, 0, 10, 9])]
# # Each token_id corresponds to one pattern dict
# match_id, token_ids = matches[0]
# for i in range(len(token_ids)):
#     print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)




# import spacy
# from spacy.language import Language
# from spacy.tokens import Span

# nlp = spacy.load("en_core_web_sm")

# @Language.component("expand_person_entities")
# def expand_person_entities(doc):
#     new_ents = []
#     for ent in doc.ents:
#         if ent.label_ == "PERSON" and ent.start != 0:
#             prev_token = doc[ent.start - 1]
#             if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
#                 new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
#                 new_ents.append(new_ent)
#         else:
#             new_ents.append(ent)
#     doc.ents = new_ents
#     return doc

# # Add the component after the named entity recognizer
# nlp.add_pipe("expand_person_entities", after="ner")

# doc = nlp("Dr. Alex Smith chaired first board meeting of Acme Corp Inc.")
# print([(ent.text, ent.label_) for ent in doc.ents])
