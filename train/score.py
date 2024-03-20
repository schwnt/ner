import spacy
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.training.example import Example
import codecs
import random
import json

model_names=[]
def load_modelnames(ver, start, end, stride) :
    i = start
    while i <= end :
        model_names.append(f"ner_{i}{ver}")
        i+= stride

load_modelnames("Gen1", 5, 20, 5)

example_count = 0 
texts = []
gold_entities = []
gold_examples = []

models_dir = "models\\"
text_path ="texts\\"
def open_data(name, text_number = None):
    file = open(f'{text_path}{name}{text_number}.json', 'r', encoding='utf-8')
    return json.load(file)

def get_labels(data):
    return data["classes"]

def get_example(data, i):
    global example_count
    text = data["annotations"][0][0]
    entities = data["annotations"][0][1] 
    texts.append(text)
    example_count += 1
    gold_entities.append(entities)

def load_examples(name, data_count):
    i=1
    while i <= data_count:
        data = open_data(name,i)
        get_example(data, i)
        i+=1 

load_examples("the_thaot", 10)
load_examples("tin_tuct", 10)
load_examples("khoa_hoct", 10)
fresults = {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]}
presults = {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]}
rresults = {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]}
results = { 'f' : {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]},
            'p' : {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]}, 
            'r' : {'PER':[],'LOC':[], 'ORG':[], 'EVENT':[]}}

best_model_idx = -1
best_favg = 0
for i in range(len(model_names)) :
    model = spacy.load(models_dir + model_names[i])
    examples = []
    for j in range(example_count):
        doc = model(texts[j])
        entities = gold_entities[j]
        examples.append(Example.from_dict(doc, entities))
    scorer = Scorer()
    scores = scorer.score(examples)
    for s in ['f', 'r', 'p'] :
        for l in ['PER', 'LOC', 'ORG', 'EVENT'] :
            results[s][l].append("{:.2f}".format(scores['ents_per_type'][l][s]))
    avg = 0
    for l in ['PER', 'LOC', 'ORG', 'EVENT'] :
        avg += scores['ents_per_type'][l]['f']
    if avg > best_favg :
        best_model_idx = i
        best_favg = avg
    print(f"{i}/{len(model_names)} current: {avg/4} best: {best_favg/4} {model_names[best_model_idx]}")

print(f"{best_favg/4} {model_names[best_model_idx]}")
print(model_names)
for s in ['f', 'r', 'p'] :
    print(s)
    for l in ['PER', 'LOC', 'ORG', 'EVENT'] :
        print(f"{results[s][l]} {l}")
# print("! no event on avg score")