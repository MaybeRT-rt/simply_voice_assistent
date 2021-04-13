## код из статьи на хабре (https://habr.com/ru/post/462333/) Давид Дале
## 

import pandas as pd
#импортируем библиотеку на машинного обучния
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline
from lets_talk import say

def boltalka():
    good = pd.read_csv('good.tsv', sep='\t')
    good.sample(5)
    say('Давай, коль не шутишь')

    ok = input('И? ')
     
    
    #создаем объект, который булет преобразовыватьь короткие - числовые векторы
    vectorizer = TfidfVectorizer()
    #обучаем на контакстах --> запоминаем частоту каждоо слова
    vectorizer.fit(good.context_0)
    # в матрицу сколько раз кадое слово встречалось в тексте
    matrix_big = vectorizer.transform(good.context_0)
    print('думаю...')
    svd = TruncatedSVD(n_components=300)
    svd.fit(matrix_big)
    matrix_small = svd.transform(matrix_big)
    print('думаю...')

    def softmax(x):
        proba = np.exp(-x)
        return proba / sum(proba)
        
    print('думаю...')
    

    class NeighborSampler(BaseEstimator):
        """класс выбор случайных соседей"""
        def __init__(self, k = 5, temperature=1.0):
            self.k = k
            self.temperature =  temperature
        def fit(self, X, y):
            self.tree_ = BallTree(X)
            self.y_ = np.array(y)
        def predict(self, X, random_state=None):
            distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
            result = []
            for distances, index in zip(distances, indices):
                result.append(np.random.choice(index, p=softmax(distances * self.temperature)))
            return self.y_[result]

        
    ns = NeighborSampler()
    ns.fit(matrix_small, good.reply)
    pipe = make_pipeline(vectorizer, svd, ns)
    okey = " ".join(pipe.predict([ok]))
    oko = okey
    say(oko)


