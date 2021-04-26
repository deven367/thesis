import numpy as np
import os
import matplotlib.pyplot as plt
# %matplotlib inline

ap_ody = [150,311,496,729,907,1014,1144,1283,1464,1689,1903,2098,2267,2437,3586,2744,2947,3078,3238,3355,3503,3632,3750]
bl_ody = [142,277,446,701,863,973,1078,1242,1419,1613,1796,1943,2083,2254,2445,2594,2771,2907,3073,3198,3325,3440,3550]
wc_ody = [190,358,548,897,1086,1223,1352,1582,1808,2056,2314,2481,2656,2849,3086,3295,3580,3765,4032,4210,4385,4577,4727]
bt_ody = [1,111,223,367,589,718,818,902,1057,1206,1352,1501,1612,1721,1858,2007,2139,2296,2410,2552,2648,2756,2882,2987]

def create_dict(embedding_path):
    for fx in os.listdir(embedding_path):
        if fx.endswith('.npy'):
            name = fx[:-4]
            print("Loaded "+fx)
            book_name, method = get_embed_method_and_name(name)
            embed = np.load(embedding_path+fx)
            print(method)
            ts = time_series_v2(successive_similarities(embed, 1), bl_ody)

            index = 0
            succ_y = ts[index][1] # for chp 1
            dictt(succ_y, index, method)

d = {}
def dictt(similarities, index, method):
    name = create_label(index, method)
    d[name] = similarities


def label(arg):
    switcher = {
        'dcltr_base': "Declutr Base",
        'dcltr_sm': "Declutr Small",
        'distil': "DistilBERT",
        'if_FT': "InferSent FastText",
        'if_glove': "InferSent GloVe",
        'roberta': "RoBERTa",
        'use': "USE"
    }
    return switcher.get(arg)

def create_label(index, method):
    met = label(method)
    return 'Book ' +str(index + 1) + ' Butcher and Lang ' + met


def get_embed_method_and_name(fname):
    t = fname.split('_cleaned_')
    return  t[0].split()[-1], t[-1]


def successive_similarities(embeddings, k):
    successive = []
    for i in range(len(embeddings) - k):
        successive.append(cos_sim(embeddings[i], embeddings[i+k]))
    return successive

from numpy import dot
from numpy.linalg import norm

def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))

def time_series_v2(successive, breakpoints, fname = None):
    st = 0
    plt_values = []
    for i in range(len(breakpoints)):

        if i > 0:
            st = breakpoints[i-1]

        x = [j for j in range(breakpoints[i] - st)]

        if i == 0:
            y = successive[:breakpoints[i]]
        else:
            y = successive[breakpoints[i-1] : breakpoints[i]]

        plt_values.append([x,y])

    temp = len(successive[breakpoints[-1]:])
    x = [j for j in range(temp)]
    y = successive[breakpoints[-1]:]
    plt_values.append([x,y])

    return plt_values

# def get_book_name(fname):







if __name__ == '__main__':
    embedding_path = '../final/butcher and lang/'
    create_dict(embedding_path)
