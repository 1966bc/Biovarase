#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is the launcher module of Biovarase."""
import sys
import profile
import pstats
import frames.main as main

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"

if len(sys.argv)>1:
    profile.run('main.main()', 'profile_results')
    p = pstats.Stats('profile_results')
    p.sort_stats('cumulative').print_stats(10)
else:
    main.main()
    
