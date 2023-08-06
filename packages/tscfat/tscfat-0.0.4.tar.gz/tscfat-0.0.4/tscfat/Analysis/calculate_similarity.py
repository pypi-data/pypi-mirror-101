#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:28:09 2020

@author: arsi

Functions for distance matrix and similarity matrix calculation.
Numpy pdist function is used for the calculation. Full reference: 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html

"""

from scipy.spatial.distance import pdist, squareform
import numpy as np

def calculate_similarity(X, metric='Euclidean'):        
    """ Calculate a distance matrix.  
    

    Parameters
    ----------
    X : Numpy ndarray
        An m by n array of m original observations in an n-dimensional space.

        
    metric : str or function, optional
            The default is "Euclidean"-

    Returns
    -------
    Y_sim : Numpy ndarray
            Returns a similarity matrix Y. 
            

    """
    
    assert isinstance(X, np.ndarray), "Data format is not a numpy array."
    assert np.ndim(X) == 2, "Matrix is not 2 dimensional."
    
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    Y_sim = 1 / (1+Y_square)
    return Y_sim

def calculate_distance(X, metric="Euclidean"):
    
    """ Calculate a similarity matrix. 
    
    Parameters
    ----------
    X : Numpy ndarray
        An m by n array of m original observations in an n-dimensional space.

        
    metric : str or function, optional
            The default is "Euclidean"-

    Returns
    -------
    Y_square : Numpy ndarray
            Returns a condensed distance matrix Y.

    """
    
    assert isinstance(X, np.ndarray), "Data format is not a numpy array."
    assert np.ndim(X) == 2, "Matrix is not 2 dimensional."
    
    Y = pdist(X,metric)
    Y_square = squareform(Y)
    return Y_square

