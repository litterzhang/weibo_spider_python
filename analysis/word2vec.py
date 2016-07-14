#!D:\Python35\python.exe
# -*- coding: utf-8 -*-

'转化词向量'

__author__='litterzhang'

import os
from gensim.models import Word2Vec

def convert_vec(filepath):
	with open(filepath, 'r', encoding='utf-8') as fr:
		sentences = list()
		for line in fr:
			sentences.append(line.split())

		vec_model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=3)

		#保存模型
		save_vec(vec_mode, os.path.join(os.path.dirname(__file__), 'result/model'))

def load_vec(filepath):
	return vec_model = Word2Vec.load(filepath)

def save_vec(vec_mode, filepath):
	vec_model.save(filepath)

def update_vec(vec_model, filepath)
	with open(filepath, 'r', encoding='utf-8') as fr:
		sentences = list()
		for line in fr:
			sentences.append(line.split())
		vec_model.train(sentences)
		return vec_model