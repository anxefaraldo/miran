# -*- coding: utf-8 -*-

import re
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from miran.format import *
from miran.defs import KEY2


sns.set_style('darkgrid')
mpl.rc('font', **{'family':'serif', 'serif':['Times']})
mpl.rc('xtick', labelsize=8)
mpl.rc('ytick', labelsize=8)
mpl.rc('axes', labelsize=9)
mpl.rc('text', usetex=True)


def plot_chroma(chromagram, name="untitled", sr=44100, hl=2048,
                output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", cmap='magma'):

    from librosa.display import specshow
    with sns.axes_style('ticks'):
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
        plt.savefig(os.path.join(output_dir, name + '.pdf'), format="pdf", dpi=1200)
        plt.show()



def plot_bchroma(chromagram, name="untitled", sr=44100, hl=2048,
                output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures", save=True, cmap='magma'):

    from librosa.display import specshow
    with sns.axes_style('ticks'):
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
            plt.savefig(os.path.join(output_dir, name + '.pdf'), format="pdf", dpi=1200)
        plt.show()



def plot_majmin_dist(dataset_dir, name="Key_Distribution", output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures/", ext=".txt", nokey=True):

    corpus = folderfiles(dataset_dir, ext=ext)

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

    gs = mpl.gridspec.GridSpec(2, 1, height_ratios=[1, 12])
    ax = plt.subplot(gs[0])
    a = ax.barh(0, total_maj, linewidth=0.0, edgecolor=(.1, .1, .1))
    b = ax.barh(0, total_min, left=total_maj, linewidth=0.0, edgecolor=(.1, .1, .1))
    if nokey:
        c = ax.barh(0, no_key, left=total_min+total_maj,  linewidth=0.0, edgecolor=(.1, .1, .1))
    plt.xlim((0, total_items))
    plt.xticks([])
    plt.yticks([])
    plt.title(name, fontsize=10)

    for r in a:
        pmaj = "%.1f" % (total_maj * percentage_factor)
        str_l = len(pmaj) + 1
        plt.text((total_maj * 0.5) - (str_l * 0.8), -0.25, pmaj + '\%', fontsize=8, color='white')

    for r in b:
        pmin = "%.1f" % (total_min * percentage_factor)
        str_l = len(pmin) + 1
        plt.text(total_maj + (total_min * 0.5) - (str_l * 0.8), -0.25, pmin + '\%', fontsize=8)

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
    plt.bar(range(12), percentage_major, label='major', linewidth=0, edgecolor=(.1, .1, .1))
    plt.bar(range(12), percentage_minor, bottom=percentage_major, label='minor', linewidth=0, edgecolor=(.1, .1, .1))
    if nokey:
        plt.bar(12, percentage_no_key, label='no key', linewidth=0, edgecolor=(.1, .1, .1))
    plt.legend(fontsize=8, frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, re.sub(' ', '_', name) + '.pdf'), format="pdf", dpi=1200)



def plot_profiles(profile_name, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures/",
                  yr=None, yt=None, loc=None, yl="weigths", fy1=7, fy2=0, fx=0):
    plt.figure(figsize=(5.16, 2.5), dpi=150)
    a = plt.plot(KEY2[profile_name][0], '-o', linewidth=1, markersize=4, label="major")
    c1 = a[0].get_color()
    b = plt.plot(KEY2[profile_name][1], '--s', linewidth=1, markersize=4, label="minor")
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
    plt.savefig(os.path.join(output_dir, profile_name + '_profiles.pdf'), format="pdf", dpi=1200)
    plt.show()



def plot_single_profile(data, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures",
                  yr=None, yt=None, loc=None, label="", yl="weigths", fy=7, fx=0, save=True):

    plt.figure(figsize=(5.16, 2.5), dpi=150)
    a = plt.plot(data, '-p', linewidth=1, markersize=4, label=label) # used to be '-gp' to force green
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
        plt.legend(fontsize=8,loc=loc, frameon=True) # typically some (0.8,0.6)
    plt.tight_layout(pad=2, rect=(0, 0, 1, 1))
    if save:
        plt.savefig(os.path.join(output_dir, label + '_single_profile.pdf'), format="pdf", dpi=1200)
    plt.show()
