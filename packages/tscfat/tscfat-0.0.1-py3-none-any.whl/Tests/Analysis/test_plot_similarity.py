#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:20:15 2021

@author: arsii

Test for similarity plotting.

"""
import pytest
import numpy as np

from tscfat.Utils.argument_loader import setup_np, setup_pd
from tscfat.Analysis.plot_similarity import plot_similarity

#TODO! write docstrings

class TestPlotSimilarity(object):
    
    def test_bad_arguments(self):
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            plot_similarity(setup_pd(),setup_np(),setup_np(),test=True)
        expected_error_msg = "Similarity matrix type is not np.ndarray."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)
        
        # Store information about raised ValueError in exc_info
        with pytest.raises(AssertionError) as exc_info:
            plot_similarity(setup_np(),setup_pd(),setup_np(),test=True)
        expected_error_msg = "Novelty score array type is not np.ndarray."
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)

    def test_plot_similarity(self):
    
        simmat = np.eye(50)
        novelty = np.ones(50)
        stability = np.ones(50)
        ker = np.array([[1,1,0,-1,-1],
                        [1,1,0,-1,-1],
                        [0,0,0,0,0],
                        [-1,-1,0,1,1],
                        [-1,-1,0,1,1]])
        
        ret = plot_similarity(simmat,
                              novelty,
                              stability,
                              title = "test",
                              doi = None,
                              savepath = False, 
                              savename = False,
                              ylim = (0,0.05),
                              threshold = 0,
                              axis = None,
                              kernel = ker,
                              test = True
                              )
        
        assert ret is not None