# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import spacy

models = {} 
def_model = 'General'
models['Chung'] = spacy.load("lang_models\\Chung")
models['Thể Thao'] = spacy.load("lang_models\\TheThao")
models['Tin Tức'] = spacy.load("lang_models\\TinTuc")
models['Khoa Học'] = spacy.load("lang_models\\KhoaHoc")

texts = {}

def GetText(url) :
    try :
        page = urlopen(url)
    except :
        return ""
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    relevant_tags = ['p']
    content = ""
    for tag in relevant_tags:
        elements = soup.find_all(tag)
        for element in elements:
            content += element.get_text() + "\n"
    cleaned_content = " ".join(content.split())
    return cleaned_content

def GetData(url,model_name=def_model): 
    if model_name not in models :
        model_name = def_model 
    if url not in texts :
        texts[url] = GetText(url)
    text  = texts[url]
    ents = []
    doc = models[model_name](texts[url])
    for ent in doc.ents :
        label = ent.label_
        start = doc[ent.start].idx
        try: 
            end = doc[ent.end].idx
        except IndexError: 
            end = len(texts[url])
        ents.append([label, start, end])
    return {'text':text, 'ents': ents}

def GetTemplateContext() :
    names = []
    for model_name in models :
        names.append(model_name)
    return {'model_names' : names}
