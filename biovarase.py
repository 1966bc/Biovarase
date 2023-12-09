#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is the module which launchers Biovarase."""
import sys
import profile
import pstats
import frames.login as login


if len(sys.argv) > 1:
    profile.run('login.main()', 'profile_results')
    p = pstats.Stats('profile_results')
    p.sort_stats('cumulative').print_stats(10)
else:
    login.main()
    
