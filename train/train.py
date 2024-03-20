# -*- coding: utf8 -*-

import codecs
import json
import random
from os.path import exists
import time
import os.path
import re
from spacy.tokens import Token
from spacy.training.example import Example
from spacy.pipeline import EntityRuler
from spacy.tokenizer import Tokenizer
import spacy

nlp = spacy.blank("vi")
ner = nlp.add_pipe("ner")


text_path ="texts\\"
def open_data(name, text_number = None):
    file = open(f'{text_path}{name}{text_number}.json', 'r', encoding='utf-8')
    return json.load(file)

def get_labels(data):
    return data["classes"]

def get_example(data, i):
    text = data["annotations"][0][0] #type: string
    entities = data["annotations"][0][1] #type: dict
    doc = nlp(text) 
    example = Example.from_dict(doc, entities)
    for e in entities["entities"] : 
        entcount[e[2]]+=1
    return example  

entcount = {'ORG': 0, 'LOC': 0, 'PER': 0, 'EVENT': 0, 'MISC' :0}
def load_labels_examples(labels, examples, name, data_count):
    i=1
    while i <= data_count:
        data = open_data(name,i)
        labels += get_labels(data)
        examples.append(get_example(data, i))
        i+=1
    return (labels, examples)

examples = []
labels = []
load_labels_examples(labels, examples, "the_thao",42) 
load_labels_examples(labels, examples, "tin_tuc",65) 
load_labels_examples(labels, examples, "chinh_tri",7) 
load_labels_examples(labels, examples, "du_lich",14) 
load_labels_examples(labels, examples, "khoa_hoc",7) 
print(entcount)

optimizer = nlp.begin_training()
ver = "Gen10"
iter = 100
for itn in range(iter+1):
    losses = {}
    random.shuffle(examples)
    for example in examples:
        nlp.update([example], drop=0.5, losses=losses)
    print(f"iter {itn}:{losses}")
    if itn % 5 == 0 and itn >0  :
        nlp.to_disk(f"models\\ner_{itn}{ver}")
        print(f"to disk: models\\ner_{itn}{ver}")
nlp.to_disk(f"models\\ner_{iter}{ver}")