#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:56:55 2020

@author: ikaheia1

Calculate the following summary statistics for the given timeseries and plot
the results:
    - Histogram
    - Lag plot with lag 1
    - Autocorrelation
    - Partial autocorrelation function
    - Autocorrelation function
    
"""

import pandas as pd
import matplotlib.pyplot as plt
from tscfat.Utils.plot_decorator import plot_decorator

plt.style.use('seaborn')
plt.ioff()

#TODO! clean the code!

@plot_decorator
def _plot_summary(series,
                  title,
                  window = 14,
                  savepath = False,
                  savename = False,
                  test = False
                  ):
    """ Plot summary statistic for the given timeseries.
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the surrary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    window : int
        Rolling window size. The default is 14.
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.

    Returns
    -------
    None.

    """
        
    fig,ax = plt.subplots(3,2,figsize=(10,10))
    fig.suptitle(title,fontsize=20,y=1.02)
    
    gridsize = (3,2)
    ax1 = plt.subplot2grid(gridsize, (0,0), colspan=2,rowspan=1)
    ax2 = plt.subplot2grid(gridsize, (1,0), colspan=1,rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (1,1), colspan=1,rowspan=1)
    ax4 = plt.subplot2grid(gridsize, (2,0), colspan=1,rowspan=1)
    ax5 = plt.subplot2grid(gridsize, (2,1), colspan=1,rowspan=1)
    
    ax1.plot(series.index,series.values)
    ax1.set_title('Original timeseries')
    ax1.tick_params('x', labelrotation=45)
    
    ax2.plot(series.index, series.rolling(window).mean())
    #series.rolling(window).mean().plot(ax=ax2)
    #sm.graphics.tsa.plot_pacf(series,lags=30,ax=ax5)
    ax2.set(title='Rolling Average',xlabel='date',ylabel='rolling average')
    
    ax3.hist(series.values,20)
    ax3.set_title("Histogram")
  
    ax4.plot(series.values[1:],series.values[:-1],'o')
    ax4.set_title('Lag plot / lag 1')
    ax4.set_aspect(1)
    #ax3.set(adjustable='box-forced', aspect='equal')
      
    pd.plotting.autocorrelation_plot(series,ax=ax5)
    #ax5.plot(series.index, series.values)
    ax5.set_xlim([0,30])
    ax5.set_title('Autocorrelation')
    
    #series.rolling(14).mean().plot(ax=ax5)
    #sm.graphics.tsa.plot_pacf(series,lags=30,ax=ax5)
    #ax5.set(xlabel='lag',ylabel='rolling average')
    
    #sm.graphics.tsa.plot_acf(series,lags=30,ax=ax[2,1])
    #ax[2,1].set(xlabel='lag',ylabel='correlation')
    
    fig.tight_layout(pad=1.0)
        
    return fig


def summary_statistics(series,
                       title = "Time series summary",
                       window = 14,
                       savepath = False,
                       savename = False,
                       test = False,
                       ):
    """ Calculate summary statistics for the give timeseries.
    
    Parameters
    ----------
    series : Pandas Series
        A time series for which the summary is calculated 
    title : str, optional
        Summary plot title. The default is "Time series summary".
    window : int
        Rolling window size. The default is 14.
    savepath : Path object, optional
        Figure save path. The default is False.
    savename : Path object, optional
        Figure save name. The default is False.
    test : Boolean, optional
        Flag for test function. The default is False.

    Returns
    -------
    None.

    """
    
    assert isinstance(series, pd.Series), "Series is not a pandas Series."
    
    _plot_summary(series,
                  title,
                  window,
                  savepath = savepath,
                  savename = savename,
                  test=False)

    
