# -*- coding: utf-8 -*-

import re
import os.path
import numpy as np
import pandas as pd

import matplotlib.gridspec as gr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from librosa.display import specshow
from miran.format import split_key_str
from miran.utils import folderfiles
from miran.defs import KEY2


PRINT_QUALITY = 300
FORMAT = 'pdf' # 'pdf
TRANSPARENT = True # 'pdf

def plot_chroma(chromagram, name="untitled", sr=44100, hl=2048,
                output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", cmap='Reds', save=False):

    if chromagram.shape[0] == 12:
        plt.figure(figsize=(5.16, 2), dpi=150)
        plt.yticks((0.5, 2.5, 4.5, 5.5, 7.5, 9.5, 11.5), ('c', 'd', 'e', 'f', 'g', 'a', 'b'))

    elif chromagram.shape[0] == 36:
        plt.figure(figsize=(5.16, 2.5), dpi=150)
        plt.yticks((0.5, 3.5, 6.5, 9.5, 12.5, 15.5, 18.5, 21.5, 24.5, 27.5, 30.5, 33.5),
                   ('c', r'c$\sharp$', 'd', r'e$\flat$', 'e', 'f', r'f$\sharp$', 'g', r'a$\flat$', 'a', r'b$\flat$', 'b'))

        specshow(chromagram, x_axis='time', sr=sr, hop_length=hl, cmap=cmap)
        plt.xlabel('time (secs.)')
        plt.ylabel('chroma')
        plt.yticks((0.5, 2.5, 4.5, 5.5, 7.5, 9.5, 11.5), ('c', 'd', 'e', 'f', 'g', 'a', 'b'))
        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(output_dir, name + '.pdf'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
        plt.show()



def plot_bchroma(chromagram, name="untitled", sr=44100, hl=2048,
                output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", cmap='Reds', save=False):

    if chromagram.shape[0] != 24:
        chromagram = chromagram.T
        if chromagram.shape[0] != 24:
            print('does not look like a compound chromagram')
            return

        plt.figure(figsize=(5.16, 3), dpi=150)

        bass = chromagram[:12].T
        bass = np.roll(bass, -3)

        treble = chromagram[12:].T
        treble = np.roll(treble, -3)

        plt.subplot(2, 1, 1)
        specshow(treble.T, x_axis='time', sr=sr, hop_length=hl,cmap=cmap)
        plt.yticks((0.5, 2.5, 4.5, 5.5, 7.5, 9.5, 11.5), ('c', 'd', 'e', 'f', 'g', 'a', 'b'))
        plt.xticks([])
        plt.xlabel('')
        plt.ylabel('treble')

        plt.subplot(2, 1, 2)
        specshow(bass.T, x_axis='time', sr=sr, hop_length=hl,cmap=cmap)
        plt.yticks((0.5, 2.5, 4.5, 5.5, 7.5, 9.5, 11.5), ('c', 'd', 'e', 'f', 'g', 'a', 'b'))
        plt.ylabel('bass')
        plt.xlabel('time (secs.)')
        if save:
            plt.savefig(os.path.join(output_dir, name + '.pdf'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
        plt.show()



def plot_majmin_dist(dataset_dir, name="Key_Distribution", title=None, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures/",
                     ext=".txt", nokey=True, save=False):

    corpus = folderfiles(dataset_dir, ext=ext)

    if not title:
        title = name

    raw_keys = []
    for item in corpus:
        with open(item, 'r') as f:
            raw_keys.append(split_key_str(f.readline()))

    major = np.zeros(12)
    minor = np.zeros(12)
    no_key = 0
    for e in raw_keys:
        if e[1] == 0:
            major[e[0]] += 1
        elif e[1] == 1:
            minor[e[0]] += 1
        else:
            no_key += 1

    total_maj = np.sum(major)
    total_min = np.sum(minor)
    total_items = total_maj + total_min + no_key
    percentage_factor = 100.00 / total_items
    percentage_major = np.multiply(major, percentage_factor)
    percentage_minor = np.multiply(minor, percentage_factor)
    percentage_no_key = np.multiply(no_key, percentage_factor)

    # NOW THE PLOTTING
    plt.figure(figsize=(5.16, 2.5), dpi=150)

    gs = gr.GridSpec(2, 1, height_ratios=[1.4, 12])
    ax = plt.subplot(gs[0])
    a = ax.barh(0, total_maj)
    b = ax.barh(0, total_min, left=total_maj)
    if nokey:
        c = ax.barh(0, no_key, left=total_min+total_maj)
    plt.xlim((0, total_items))
    plt.xticks([])
    plt.yticks([])
    plt.title(title, fontsize=10)

    for r in a:
        pmaj = "%.1f" % (total_maj * percentage_factor)
        str_l = len(pmaj) + 1
        plt.text((total_maj * 0.5) - (str_l * 0.8), -0.25, pmaj + '\%', fontsize=8)

    for r in b:
        pmin = "%.1f" % (total_min * percentage_factor)
        str_l = len(pmin) + 1
        plt.text(total_maj + (total_min * 0.5) - (str_l * 0.8), -0.25, pmin + '\%', fontsize=8 , color='white')

    if nokey:
        for r in c:
            pnk = "%.1f" % (no_key * percentage_factor)
            if no_key * percentage_factor > 3:
                str_l = len(pnk) + 1
                plt.text(total_maj + total_min + (no_key * 0.5) - (str_l * 0.8), -0.25, pnk + '\%', fontsize=8)

    plt.subplot(gs[1])
    plt.xlabel('tonic note')
    plt.ylabel('percentage (\%)')
    if nokey:
        plt.xticks(range(13), (
        r'C', r'C$\sharp$', r'D', r'E$\flat$', r'E', r'F', r'F$\sharp$', r'G', r'A$\flat$', r'A', r'B$\flat$', r'B',
        r'--'))
    else:
        plt.xticks(range(12), (
        r'C', r'C$\sharp$', r'D', r'E$\flat$', r'E', r'F', r'F$\sharp$', r'G', r'A$\flat$', r'A', r'B$\flat$', r'B'))
    plt.bar(range(12), percentage_major, label='major')
    plt.bar(range(12), percentage_minor, bottom=percentage_major, label='minor')
    if nokey:
        plt.bar(12, percentage_no_key, label='no key')
    plt.legend(fontsize=8, frameon=True)
    plt.tight_layout()
    if save:
        plt.savefig(os.path.join(output_dir, re.sub(' ', '_', name) + '.pdf'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
    plt.show()



def plot_bin_profiles(profile_name, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures/",
                      yr=None, yt=None, loc=None, yl="weigths", fy1=7, fy2=0, fx=0, l1='major', l2='minor'):
    plt.figure(figsize=(5.16, 2.5), dpi=150)
    a = plt.plot(KEY2[profile_name][0], '-o', linewidth=1, markersize=4, label=l1)
    c1 = a[0].get_color()
    b = plt.plot(KEY2[profile_name][1], '--s', linewidth=1, markersize=4, label=l2)
    c2 = b[0].get_color()
    plt.xlabel('relative scale degrees')
    plt.ylabel(yl)
    if yr:
        plt.ylim(yr)
    if yt:
        plt.yticks(yt)
    plt.xticks(range(12), (r'\^{1}', r'$\sharp$\^{1}/$\flat$\^{2}', r'\^{2}', r'$\sharp$\^{2}/$\flat$\^{3}', r'\^{3}',
                           r'\^{4}', r'$\sharp$\^{4}/$\flat$\^{5}', r'\^{5}', r'$\sharp$\^{5}/$\flat$\^{6}', r'\^{6}',
                           r'$\sharp$\^{6}/$\flat$\^{7}', r'\^{7}'))
    i = -0.25
    for f in KEY2[profile_name][0]:
        plt.text(i + fx, fy1, '%.2f' % f, fontsize=8, color=c1)
        i += 1
    i = -0.25
    for f in KEY2[profile_name][1]:
        plt.text(i + fx, fy2, '%.2f' % f, fontsize=8, color=c2)
        i += 1

    if not loc:
        plt.legend(fontsize=8, frameon=True)
    else:
        plt.legend(fontsize=8, loc=loc, frameon=True)  # typically some (0.8,0.6)

    plt.tight_layout(pad=2, rect=(0, 0, 1, 1))
    plt.savefig(os.path.join(output_dir, profile_name + '_profiles.png'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
    plt.show()



def plot_single_profile(data, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures",
                  yr=None, yt=None, loc=None, label="", yl="weigths", fy=7, fx=0, save=True):

    plt.figure(figsize=(5.16, 2.5), dpi=150)
    a = plt.plot(data, '-p', linewidth=1, markersize=4, label=label)
    c1 = a[0].get_color()
    plt.xlabel('relative scale degrees')
    plt.ylabel(yl)
    if yr:
        plt.ylim(yr)
    if yt:
        plt.yticks(yt)
    plt.xticks(range(12), (r'\^{1}', r'$\sharp$\^{1}/$\flat$\^{2}', r'\^{2}', r'$\sharp$\^{2}/$\flat$\^{3}', r'\^{3}',
                           r'\^{4}', r'$\sharp$\^{4}/$\flat$\^{5}', r'\^{5}', r'$\sharp$\^{5}/$\flat$\^{6}', r'\^{6}',
                           r'$\sharp$\^{6}/$\flat$\^{7}', r'\^{7}'))
    i = -0.25
    for f in data:
        plt.text(i + fx, fy, '%.2f' % f, fontsize=8, color=c1)
        i += 1
    if not loc:
        plt.legend(fontsize=8, frameon=True)
    else:
        plt.legend(fontsize=8,loc=loc, frameon=True)
    plt.tight_layout(pad=2, rect=(0, 0, 1, 1))
    if save:
        plt.savefig(os.path.join(output_dir, label + '_single_profile.pdf'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
    plt.show()


def plot_relative_mtx(xlx_with_valid_matrix, label='', output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", cmap='Reds', save=False):

    a = pd.read_excel(xlx_with_valid_matrix, sheetname=1)
    aa = a.as_matrix()

    plt.figure(figsize=(8.2, 1.6), dpi=150)

    xlabs = (r'I', r'$\flat$II', r'II', r'$\flat$III', r'III', r'IV', r'$\flat$V', r'V', r'$\flat$VI', r'VI', r'$\flat$VII', r'VII',
             r'i', r'$\flat$ii', r'ii', r'$\flat$iii', r'iii', r'iv', r'$\flat$v', r'v', r'$\flat$vi', r'vi', r'$\flat$vii', r'vii',
             r'1', r'$\flat$2', r'2', r'$\flat$3', r'3', r'4', r'$\sharp$4', r'5', r'$\flat$6', r'6', r'$\flat$7', r'7',
             r'X')
    ylabs = (r'I', r'i', r'1', 'X')

    ax = plt.imshow(aa, interpolation='nearest', cmap=cmap, origin='lower', aspect='auto', norm=LogNorm())
    plt.xticks(range(37), xlabs, size=8)
    plt.yticks(range(4), ylabs, size=8)

    width, height = aa.shape

    for x in xrange(width):
        for y in xrange(height):
            if aa[x][y] > 0:
                if aa[x][y] > 100:
                    my_color = 'white'
                else:
                    my_color = 'black'
                plt.annotate(str(aa[x][y]), xy=(y, x), horizontalalignment='center', verticalalignment='center', size=7, color=my_color)

    plt.tight_layout()
    if save:
        plt.savefig(os.path.join(output_dir, label + '_relative_matrix.pdf'), format="pdf", dpi=PRINT_QUALITY, transparent=TRANSPARENT)
    plt.show()



def plot_confusion_mtx(xlx_with_valid_matrix, label='', output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", cmap='Reds', save=False):

    a = pd.read_excel(xlx_with_valid_matrix, sheetname=0)
    aa = a.as_matrix()

    plt.figure(figsize=(8, 5.16), dpi=150)

    labs = (r'C', r'D$\flat$', r'D', r'E$\flat$', r'E', r'F', r'G$\flat$', r'G', r'A$\flat$', r'A', r'B$\flat$', r'B',
            r'C', r'D$\flat$', r'D', r'E$\flat$', r'E', r'F', r'G$\flat$', r'G', r'A$\flat$', r'A', r'B$\flat$', r'B',
            r'C', r'D$\flat$', r'D', r'E$\flat$', r'E', r'F', r'G$\flat$', r'G', r'A$\flat$', r'A', r'B$\flat$', r'B', r'X')

    plt.imshow(aa, interpolation='nearest', cmap=cmap, origin='lower', aspect='auto', norm=LogNorm())
    plt.xticks(range(37), labs, size=6)
    plt.yticks(range(37), labs, size=6)
    plt.text(5, -3, 'major', size=7)
    plt.text(17, -3, 'minor', size=7)
    plt.text(29, -3, 'other', size=7)
    plt.text(-2.5, 5, 'major', rotation=90, size=7)
    plt.text(-2.5, 17, 'minor', rotation=90, size=7)
    plt.text(-2.5, 29, 'other', rotation=90, size=7)

    width, height = aa.shape

    for x in xrange(width):
        for y in xrange(height):
            if aa[x][y] > 0:
                if aa[x][y] > 60:
                    my_color = 'white'
                else:
                    my_color = 'black'
                plt.annotate(str(aa[x][y]), xy=(y, x - 0.1), horizontalalignment='center', verticalalignment='center', size=6, color=my_color)

    plt.tight_layout()
    if save:
        plt.savefig(os.path.join(output_dir, label + '_confusion_matrix.pdf'), format=FORMAT, dpi=PRINT_QUALITY, transparent=TRANSPARENT)
    plt.show()
