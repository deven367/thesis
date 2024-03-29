import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import os
import pandas as pd

def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def plot(path, data, name):
    n = len(data)
    if n > 1:
        titles = [f'Book {i+1} {name.title()}' for i in range(n)]
    for i in range(len(data)):
        # break
        values = list(data[i].values())
        labels = list(data[i].keys())

        '''
            code to check whether all strips are of same length
        '''
        np_values = np.asarray(values)
        for val, lab in zip(np_values, labels):
            print('{} Length is {}'.format(lab, len(val)))

        # normalize each strip separately, if null, put zero
        norm_ = []
        for val in values:
            if np.count_nonzero(np.isnan(val)) > 0:
                val = np.nan_to_num(val, nan=0)
            norm_.append(normalize(val))


        '''
            1. Create df with a transpose of the obtained values
            2. Reorganize the labels
            3. Optional - print head of the df
            4. Optional - save as csv
            5. Plot transpose of the df
        '''
        df = pd.DataFrame(np.asarray(norm_).transpose(), columns = labels)
        # organized_labels = ['DeCLUTR Base','DeCLUTR Small', 'InferSent FastText', 'InferSent GloVe','DistilBERT', 'RoBERTa', 'USE','Lexical Weights', 'Lexical Vectors', 'Lexical Vectors (Corr)']
        # print(df.head())
        organized_labels = ['DeCLUTR Base','DeCLUTR Small', 'InferSent FastText', 'InferSent GloVe','DistilBERT', 'RoBERTa', 'USE']
        df2 = df[ organized_labels]
        # df2 = df
        # print(df2.head())
        # choice = input('Do you want to save a csv? ')
        choice = 'y'
        # if choice == 'y' or choice == 'Y':
        #     df2.to_csv(get_title(name)+'.csv')

        # ax = sns.heatmap(values, yticklabels = labels, cmap = 'hot', vmin = -1, vmax = 1)

        # ax = sns.heatmap(df2.T, cmap = 'hot', vmin = 0, vmax = 1, xticklabels = 100)
        # title = get_title(name)
        title = titles[i]

        # print(title)


        # choice = input('Do you want plot a correlation plot? ')
        if choice == 'y' or choice == 'Y':
            plt.title(title)
            sns.heatmap(df2.corr(), cmap = 'hot', vmin = 0, vmax = 1, xticklabels = False, square = True)
            plt.savefig(path + title + '_corr.png', dpi = 300, bbox_inches='tight')
            # plt.show()
            plt.clf()


        # have the name of the pkl file in the format FN LN BN
        # names = name.split()
        # first_name = names[0]
        # last_name = names[1]
        # book_name = names[-1]

        # format for Book number Last Name Book name
        # title = 'Book '+ str(i + 1) + ' ' + last_name.title() + ' ' + book_name.title()

        # format for strip plot of the whole book
        # title = name.title()

        # normalized heatmap
        # plt.figure()
        # ax = sns.heatmap(norm_, yticklabels = labels, cmap = 'hot', vmin = 0, vmax = 1)
        plt.title(title)
        ax = sns.heatmap(df2.T, cmap = 'hot', vmin = 0, vmax = 1, xticklabels = 100)
        for j in range(len(data[i].keys())):
            ax.axhline(j, color='white', lw=1)


        # plt.tight_layout()
        plt.savefig(path + title + '.png', dpi = 300, bbox_inches='tight')
        # plt.show()
        plt.clf()
        print("Created {}".format(title))
        print('-'*45)
        # break

def get_title(name):
    return name.split('_whole')[0].title()

def get_title_individual(name):
    return name.split('_whole')[0].title()

def iterator(embedding_path):
    for fx in os.listdir(embedding_path):
        if fx.endswith('.pkl'):
            name = fx[:-4]
            # print("Loaded "+fx)
            fname = open(embedding_path+fx, 'rb')
            data = pickle.load(fname)
            plot(embedding_path, data, name)
            #print(data[0].values())
            # break

if __name__ == '__main__':
    embedding_path = './zz/'
    iterator(embedding_path)
