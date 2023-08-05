#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# symchaos.py: SYMmetric CHAOS
# Author: Rolf Sander
__version__ =  '0.9.0'

import os, sys, shutil
assert sys.version_info >= (3, 6)
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pylab 
from math import sin, cos, pi
from ast import literal_eval
from random import random

HLINE  = '-' * 78

##############################################################################

def evaluate_command_line_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inifile', nargs='?', default=None,
                        help='configuration file (*.ini)')
    args = parser.parse_args()
    return args

##############################################################################

def evaluate_config_file(configfile, section=None, allow_no_value=False, verbose=False):
    # https://docs.python.org/3.6/library/configparser.html
    import configparser
    config = configparser.ConfigParser(inline_comment_prefixes=('#'),
                                       allow_no_value=allow_no_value)
    # make config case-sensitive:
    # https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    config.optionxform = str
    # use 'read_file' because 'read' ignores it if ini file doesn't exist:
    with open(configfile) as f:
        config.read_file(f)
    if (section):
        if (verbose):
            print(f'The section [{section}] of the config file {configfile} contains:')
            for key in config[section]:
                print(f'{key:16}= {config[section][key]}')
            print()
        return config[section]
    else:
        return config

##############################################################################

def symchaos_calc_py(ixres, iyres, x, y, a, b, c, d):

    screen = np.zeros((iyres, ixres))
    for i in range(400*ixres*iyres):
        xnew = a*cos(2.*pi*x) + b*cos(2.*pi*x)*sin(2.*pi*y) + \
            c*cos(4.*pi*x) + d*cos(6.*pi*x)*sin(4.*pi*y) + x
        ynew = a*cos(2.*pi*y) + b*cos(2.*pi*y)*sin(2.*pi*x) + \
            c*cos(4.*pi*y) + d*cos(6.*pi*y)*sin(4.*pi*x) + y
        x = xnew-int(xnew)
        if (xnew<0.):
            x=x+1.
        y = ynew-int(ynew)
        if (ynew<0.):
            y=y+1.
        if (i>=100):
            ix = int(ixres*x)
            iy = int(iyres*y)
            screen[iy,ix] = screen[iy,ix] + 1
            if (i==ixres*iyres):
                if (screen[iy,ix]>10):
                    sys.exit('very strong attractor')
    return screen

##############################################################################

def makepng(screen, palette, dirname, basename):

    edges   = np.percentile(screen, np.linspace(0, 100, 256))
    screen2 = np.digitize(screen, edges, right=False)
    if (MAKETILES):
        # create an array showing the quilt tessellated 3*3:
        screen3 = np.tile(screen2, (3, 3))

    if (palette=='*'):
        # make one image for each available palette, see also:
        # https://scipy-cookbook.readthedocs.io/items/Matplotlib_Show_colormaps.html
        for pal in pylab.cm.datad:
            filename = dirname + '/' + basename + '_' + pal + '.png'
            plt.imsave(filename, screen2, cmap=plt.get_cmap(pal))
            if (MAKETILES):
                filename = dirname + '/tile_' + basename+'_'+pal+'.png'
                plt.imsave(filename, screen3, cmap=plt.get_cmap(pal))
    else:
        # make one image, using selected palette:
        filename = dirname + '/' + basename + '.png'
        plt.imsave(filename, screen2, cmap=plt.get_cmap(palette))
        if (MAKETILES):
            filename = dirname + '/tile_' + basename + '.png'
            plt.imsave(filename, screen3, cmap=plt.get_cmap(palette))

    if(VERBOSE):
        print('screen:')
        print(screen.shape)
        print(screen)

    if (HISTOGRAM):
        (hist, bin_edges) = np.histogram(screen, bins=edges)
        print('hist_screen:')
        print(hist.shape)
        print(hist)

        (hist, bin_edges) = np.histogram(screen2, bins=256)
        print('hist_screen2:')
        print(hist.shape)
        print(hist)

##############################################################################

def make_symchaos(a, b, c, d, e, n, resolution, palette, method, vary_steps, dirname):

    x = 0.3
    y = 0.7
    ixres = resolution[0]
    iyres = resolution[1]
    print('i,x,y,a,b,c,d,e,n', file=LOGFILE)
    a0=a
    b0=b
    c0=c
    d0=d
    e0=e

    for i in range(vary_steps):
        frac = float(i) / float(vary_steps)
        istring = '%04d' % (i)
        print(istring,x,y,a,b,c,d,e,n,palette, file=LOGFILE)
        print(istring,x,y,a,b,c,d,e,n,palette)

        if (USE_FORTRAN): # choose either f90 or python
            # calculate with f90:
            screen = symchaos.calc_f90(ixres, iyres, x, y, a, b, c, d, e, n, method)
        else:
            # calculate with python:
            screen = symchaos_calc_py(ixres, iyres, x, y, a, b, c, d)

        makepng(screen, palette, dirname, 'pic_'+istring)

        # if vary_steps>1, change parameters for next image:
        if (vary_type=='random'):
            a = 2. * random() - 1.
            b = 2. * random() - 1.
            c = 2. * random() - 1.
            d = 2. * random() - 1.
            e = 2. * random() - 1.
            n = int(10.*random())
        elif (vary_type=='cyclic'):
            a = a0 * (1. + vary_value*sin(frac*2.*pi))
            b = b0 * (1. + vary_value*sin(1.+frac*2.*pi))
            c = c0 * (1. + vary_value*cos(frac*2.*pi))
            d = d0 * (1. + vary_value*cos(1.+frac*2.*pi))
            e = e0 * (1. + vary_value*cos(2.+frac*2.*pi))
        elif (vary_type=='random_walk'):
            a = a * (1. + vary_value*(2.*random()-1.)) 
            b = b * (1. + vary_value*(2.*random()-1.)) 
            c = c * (1. + vary_value*(2.*random()-1.)) 
            d = d * (1. + vary_value*(2.*random()-1.)) 
            e = e * (1. + vary_value*(2.*random()-1.)) 
        elif (vary_type=='neighborhood'):
            a = a0 * (1. + vary_value*(2.*random()-1.)) 
            b = b0 * (1. + vary_value*(2.*random()-1.)) 
            c = c0 * (1. + vary_value*(2.*random()-1.)) 
            d = d0 * (1. + vary_value*(2.*random()-1.)) 
            e = e0 * (1. + vary_value*(2.*random()-1.))
        else:
            sys.exit('unknown vary_type: '+vary_type)

##############################################################################

if __name__ == '__main__':

    args = evaluate_command_line_arguments()
    if (args.inifile):
        # type inifile with or without ini/ directory name and extension .ini:
        inibasename = os.path.splitext(re.sub('^ini/','',args.inifile))[0]
        inifile = 'ini/%s.ini' % (inibasename)
    else:
        sys.exit('ERROR: You must provide a config (*.ini) file!')
    config = evaluate_config_file(inifile, 'symchaos')
    # defaults for a0, b0, c0, and d0 from "Spektrum der Wissenschaft", Feb 1994:
    a = float(config.get('a', '-1.89'))
    b = float(config.get('b',   '1.8'))
    c = float(config.get('c',   '0.0'))
    d = float(config.get('d',  '1.34'))
    e = float(config.get('e',   '0.0'))
    n =   int(config.get('n',     '3'))
    palette     = config.get('palette', 'rainbow')
    method      = config.get('method', None)
    resolution  = literal_eval(config.get('resolution', '(640,480)'))
    VERBOSE     = config.getboolean('VERBOSE',     False)
    HISTOGRAM   = config.getboolean('HISTOGRAM',   False)
    MAKETILES   = config.getboolean('MAKETILES',   False)
    USE_FORTRAN = config.getboolean('USE_FORTRAN', False)
    if (USE_FORTRAN):
        from symchaos_f90 import symchaos
    vary_steps =   int(config.get('vary_steps', '1'))
    vary_type  =       config.get('vary_type',  'random')
    vary_value = float(config.get('vary_value', '0.01'))

    dirname = 'output/' + datetime.datetime.now().strftime(
        '%Y-%m-%d-%H%M%S') + '_' + inibasename
    os.makedirs(dirname)

    LOGFILE = open('symchaos.log', 'w+', 1) # 1=line-buffered
    make_symchaos(a, b, c, d, e, n, resolution, palette, method, vary_steps, dirname)
    shutil.copy2('symchaos.f90', dirname)
    shutil.copy2('symchaos.py',  dirname)
    shutil.copy2(inifile,        dirname)
    LOGFILE.close()
    shutil.copy2('symchaos.log', dirname)

##############################################################################
