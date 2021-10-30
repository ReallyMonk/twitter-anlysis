import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from scipy import stats, integrate
import random
import pandas as pd
import numpy as np
from itertools import cycle
import networkx as nx

import textanly
'''testlist_x = [random.uniform(-1, 1) for i in range(1000)]
testlist_y = [random.uniform(-1, 1) for i in range(1000)]
testlist_z = [str(random.randint(0, 10)) for i in range(1000)]'''
'''testdf = pd.DataFrame({
    'polarity': testlist_x,
    'subjectivity': testlist_y,
    'category': testlist_z
})'''

#newgp = testdf.groupby(['category'])
#print(len(newgp))


def visualize(polarity, subjectivity, category, cat_num):
    plotpath = './plot/'

    # build dataframe structure
    ps_df = pd.DataFrame({'polarity': polarity, 'subjectivity': subjectivity, 'category': category})

    if False:
        # polarity distribution plot
        plt.title('Polarity distribution')
        polr_displot_path = plotpath + 'polr_displot.png'
        polr_dist_plot = sns.distplot(ps_df['polarity'], bins=20, rug=True)
        polr_dist_fig = polr_dist_plot.get_figure()
        polr_dist_fig.savefig(polr_displot_path, dpi=400)
        plt.close()

        # subjectivity distribution plot
        plt.title('Subjectivity distribution')
        subj_distplot_path = plotpath + 'subj_displot.png'
        subj_distplot = sns.distplot(ps_df['subjectivity'], bins=20, rug=True)
        subj_dist_fig = subj_distplot.get_figure()
        subj_dist_fig.savefig(subj_distplot_path, dpi=400)
        plt.close()

    # scatter plot
    plt.figure(figsize=(20, 15))
    plt.title('Polarity and Subjectivity of top-k Categories')
    # seperate dataframe and sort according to amount
    # get top k cat and num
    top_k_num = {}
    top_k_cat_num = ps_df.groupby('category', as_index=False).count().sort_values(by='polarity', ascending=False).head(cat_num)
    for cnt_num in top_k_cat_num.iterrows():
        cnt_num = cnt_num[1]
        #print(cnt_num['category'], cnt_num['polarity'])
        top_k_num[cnt_num['category']] = cnt_num['polarity']
    print(top_k_num)
    return

    # seperate dataframe and sort according to amount
    top_k_cat = ps_df.groupby('category', as_index=False).count().sort_values(by='polarity', ascending=False)['category'].head(cat_num)
    top_k_list = list(top_k_cat)
    print(top_k_cat)
    print(top_k_list)
    #print(ps_df.loc[ps_df['category'].isin(top_k_list)])
    #cat_num = len(spt_df)
    #print(cat_num)
    labels = []
    graphs = []

    spt_df = ps_df.loc[ps_df['category'].isin(top_k_list)]  #.groupby('category')
    # reorder spt_df with topkcat list
    spt_df['category'] = spt_df['category'].astype('category')
    spt_df['category'].cat.reorder_categories(top_k_list, inplace=True)
    spt_df.sort_values('category', inplace=True)
    print(spt_df)

    spt_df = spt_df.groupby('category')
    # color change
    cmap = plt.cm.get_cmap("nipy_spectral", cat_num + 1)
    #print(spt_df)
    #return
    for i, sing_cate in enumerate(spt_df):
        print('-' * 10, i, '-' * 10)
        print(sing_cate)
        sing_cate_data = sing_cate[1]
        print(type(sing_cate))

        g = plt.scatter(sing_cate_data['polarity'], sing_cate_data['subjectivity'], c=cmap(i))
        labels.append(sing_cate[0])
        graphs.append(g)
    '''plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')
    plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')
    plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')'''

    plt.xlabel('polarity')
    plt.ylabel('subjectivity')
    plt.legend(handles=graphs, labels=labels)
    plt.savefig(plotpath + 'scatter.png', figsize=(20, 15), dpi=400)
    #plt.show()


data_path = './mentions.csv'


def plot_network(data_path):
    # read data and data processing
    data = pd.read_csv(data_path, index_col=[0])
    nodes = data.columns.values.tolist()

    cluster_num = 112

    print(data.sum(axis=1).sort_values(ascending=False)[:20])

    #nodes = nodes[0:50]
    # print(nodes)
    cmap = plt.get_cmap('Spectral', cluster_num)
    # cmap_clr = cmap._segmentdata
    for i in range(cmap.N):
        print(matplotlib.colors.rgb2hex(cmap(i)))
    # build node list
    #graph = nx.random_geometric_graph(112, 0.125)
    graph = nx.Graph()
    graph.add_nodes_from(nodes)

    # add edge
    for source in nodes:
        for target in nodes:
            if data[source][target] > 0 and source != target:
                graph.add_edge(source, target, weight=data[source][target])

    nx.spring_layout(graph, scale=2)
    nx.draw(graph, with_labels=False, font_weight='bold', node_size=100, alpha=0.7)
    plt.show()


plot_network(data_path)