# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt 
import scipy.cluster.hierarchy as sch
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
np.random.seed(seed=1)
#from string import strip

          
def clean_axis(ax):
    """Remove ticks, tick labels, and frame from axis"""
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)        
        
        
def plot_experiment(in_df,
         #distance to cut the columns dendogram
         cut_distance_cols='',
         #distance to cut the rows dendogram
         cut_distance_rows='',
         #clustering parameters to input to scipy.linkage
         #https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
         method='ward', 
         metric='euclidean',
         #bool to plot the column dendogram
         cluster_columns = True,
         #bool make sence only if cluster_columns = True
         order_row_and_columns=True,
         figsize=None, 
         #to pass to matplolib set_cmap
         #https://matplotlib.org/examples/color/colormaps_reference.html
         color_map_id='Blues',
         #plot every n ticks for the x axes of the heatmap
         step_first_x = 5,
         color_bar = True,
         xTitle_padding=1.05,
         title='Main Title',
         fig_name='test.png',
         #add a second axis for the molecular weight
         add_second_axis={},
         height_ratios=[1, 4],
         hspace=0.05,
         #wheter to return to clustering of the rows as a new columns
         get_clusters=True,
         owerwrite_order=False):

    if figsize == None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figsize)        

    
    gs = gridspec.GridSpec(2, 2,
                        width_ratios=[1, 4],
                        height_ratios=height_ratios,
                        wspace=0.05, hspace=hspace
                       )

    #corner top left, placeholder for colormap
    ax1 = plt.subplot(gs[0])
    clean_axis(ax1)
    
    #the dendogram for the columns
    ax2 = plt.subplot(gs[1])
    if cluster_columns == True:
        #print in_df.T.head()
        link = sch.linkage(in_df.T, method, metric)
        den_cols = sch.dendrogram(link, color_threshold=cut_distance_cols, ax=ax2, orientation='top')
        ax2.set_ylabel('Distance', rotation=0, labelpad=30)
        ax2.yaxis.set_label_position('right') 
        ax2.spines['top'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.spines['right'].set_position(('outward', 10))
        yticks = ax2.get_yticks()
        ax2.set_yticks([n for n in yticks[1:-1] if n%2 ==0])
        
        ax2.tick_params(axis='y',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    left='off', 
                    right='on',
                    labelright ='on',
                    labelleft='off')        
        ax2.tick_params(axis='x',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    bottom='off', 
                    top='off',
                    labelbottom='off',
                    labeltop='off') 
        
        fig.suptitle(title, fontsize=16, y = 0.95)
    else:
        clean_axis(ax2)
        fig.suptitle(title, fontsize=16, y = 0.8)
        
    
    
    
    #the dendogram for the rows
    ax3 = plt.subplot(gs[2])
    #print in_df.head()
    link = sch.linkage(in_df, method, metric)
    
    den_rows = sch.dendrogram(link, color_threshold=cut_distance_rows, ax=ax3, orientation='left')
    
    ax3.set_xlabel('Distance')
    ax3.spines['top'].set_visible(False)
    ax3.spines['left'].set_visible(False)  
    ax3.spines['right'].set_visible(False)     
    ax3.spines['bottom'].set_visible(True)
    ax3.spines['bottom'].set_position(('outward', 10)) 
    xticks = ax3.get_xticks()
    ax3.set_xticks([n for n in xticks[1:-1] if n%2==0]) 
    
    ax3.tick_params(axis='x',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    bottom='on', 
                    top='off',
                    labelbottom='on',
                    labeltop='off')
    
    ax3.tick_params(axis='y',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    left='off', 
                    right='off',
                    labelright ='off',
                    labelleft='off')  
    
    #the heatmap plot
    ax4 = plt.subplot(gs[3])
    
    if len(add_second_axis) > 0:
        #add new axes
        new_ax = ax4.twiny()
        new_ax.plot([0,in_df.shape[1]],[0,in_df.shape[1]],c='w',alpha=0.01)
        new_ax.tick_params(axis='x',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    bottom='on', 
                    top='off',
                    labelbottom='on',
                    labeltop='off',
                    length = 5)
        new_ax.set_ylim(0,in_df.shape[0])
        new_ax.set_xlim(0,in_df.shape[1])
        new_ax.spines['top'].set_visible(False)
        new_ax.spines['left'].set_visible(False)  
        new_ax.spines['right'].set_visible(False)  
        new_ax.spines['bottom'].set_position(('outward', 50))
        new_ax.set_xlabel(add_second_axis['label'])
        new_ax.xaxis.set_label_coords(1.05, -0.12)
        xticks = [n-0.5 for n in add_second_axis['values'].keys()]
        new_ax.set_xticks(xticks)
        xtickslabels = [add_second_axis['values'][n+0.5] for n in xticks]
        new_ax.set_xticklabels(xtickslabels)
    
    #
    if owerwrite_order:
        heatmap=ax4.pcolor(in_df.ix[owerwrite_order])
    else:
        if order_row_and_columns == True:
            heatmap=ax4.pcolor(in_df.iloc[den_rows['leaves'],den_cols['leaves']])
        else:
            heatmap=ax4.pcolor(in_df.ix[den_rows['leaves']])
    
    
    
    ax4.set_aspect('auto')
    ax4.set_ylim(0,in_df.shape[0])
    ax4.set_xlim(0,in_df.shape[1])
    heatmap.set_cmap(color_map_id)
    
    ax4.tick_params(axis='x',# changes apply to the x-axis
                    which='both',# both major and minor ticks are affected
                    bottom='on', 
                    top='off',
                    labelbottom='on',
                    labeltop='off')
    
    ax4.tick_params(axis='y',# changes apply to the y-axis
                    which='both',# both major and minor ticks are affected
                    left='off', 
                    right='off',
                    labelright ='off',
                    labelleft='off') 
         
    ax4.spines['top'].set_visible(False)
    ax4.spines['left'].set_visible(False)  
    ax4.spines['right'].set_visible(False)  
    ax4.spines['bottom'].set_position(('outward', 10)) 
    ax4.set_xlabel('Fraction')
    ax4.xaxis.set_label_coords(1.05, -0.03)
    
    if step_first_x == 1:
        xticks = np.arange(0.5, in_df.shape[1], step_first_x)
        ax4.set_xticks(xticks)
        ax4.set_xticklabels([str(int(n+0.5)) for n in xticks])
    else:
        tick_range = np.arange(step_first_x-0.5, in_df.shape[1], step_first_x)
        xticks = [0.5]+[n for n in tick_range]
        ax4.set_xticks(xticks)
        ax4.set_xticklabels([str(int(n+0.5)) for n in xticks])

    cbaxes = fig.add_axes([1, 0.4, 0.03, 0.2])    
    plt.colorbar(heatmap, cax = cbaxes, orientation='vertical')
    cbaxes.spines['right'].set_position(('outward', 5))
    fig.savefig(fig_name)
    #plt.show()
    
    if get_clusters:
        clusters = sch.fcluster(link, cut_distance_rows, criterion='distance')
        in_df['clusters']=clusters
        return in_df, den_rows['leaves']
    else:
        return den_rows['leaves']