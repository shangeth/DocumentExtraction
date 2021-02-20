import spacy
from spacy.matcher import Matcher
import re

# nlp = spacy.load("en_core_web_trf")

# text = 'Target price (): 10,600'
# text = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", text).strip()
# print(text)
# doc = nlp(text)

# pattern = [{'LOWER': 'target'}, {'LOWER': 'price', 'OP' : '*'} ,{'LOWER': 'of', 'OP' : '*'}, {'LOWER': 'rs', 'OP' : '*'},{'IS_SPACE': True, 'OP' : '*'}, {'LIKE_NUM' : True}]

# matcher = Matcher(nlp.vocab)
# matcher.add('target', [pattern])

# new_doc = nlp(text)

# matches = matcher(new_doc)
# print(matches)
# print(new_doc[matches[0][1]:matches[0][2]])


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




import spacy
from spacy.language import Language
from spacy.tokens import Span

nlp = spacy.load("en_core_web_sm")

@Language.component("expand_person_entities")
def expand_person_entities(doc):
    new_ents = []
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.start != 0:
            prev_token = doc[ent.start - 1]
            if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
                new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
                new_ents.append(new_ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

# Add the component after the named entity recognizer
nlp.add_pipe("expand_person_entities", after="ner")

doc = nlp("Dr. Alex Smith chaired first board meeting of Acme Corp Inc.")
print([(ent.text, ent.label_) for ent in doc.ents])
