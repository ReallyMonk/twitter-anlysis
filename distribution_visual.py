import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats, integrate
import random
import pandas as pd
from itertools import cycle

testlist_x = [random.uniform(-1, 1) for i in range(1000)]
testlist_y = [random.uniform(-1, 1) for i in range(1000)]
testlist_z = [str(random.randint(0, 10)) for i in range(1000)]
'''testdf = pd.DataFrame({
    'polarity': testlist_x,
    'subjectivity': testlist_y,
    'category': testlist_z
})'''

#newgp = testdf.groupby(['category'])
#print(len(newgp))


def visualize(polarity, subjectivity, category):
    plotpath = './plot/'

    # build dataframe structure
    ps_df = pd.DataFrame({
        'polarity': polarity,
        'subjectivity': subjectivity,
        'category': category
    })
    '''# polarity distribution plot
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
    plt.close()'''

    # scatter plot
    plt.title('')
    # seperate dataframe
    spt_df = ps_df.groupby(['category'])
    cat_num = len(spt_df)
    labels = []
    graphs = []

    # color change
    cmap = plt.cm.get_cmap("nipy_spectral", cat_num + 1)

    for i, sing_cate in enumerate(spt_df):
        print(sing_cate)
        sing_cate_data = sing_cate[1]
        print(type(sing_cate))
        g = plt.scatter(sing_cate_data['polarity'],
                        sing_cate_data['subjectivity'],
                        c=cmap(i))
        labels.append(sing_cate[0])
        graphs.append(g)
    '''plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')
    plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')
    plt.scatter(ps_df['polarity'], ps_df['subjectivity'], marker='o')'''

    plt.xlabel('polarity')
    plt.ylabel('subjectivity')
    plt.legend(handles=graphs, labels=labels)
    plt.show()


visualize(testlist_x, testlist_y, testlist_z)