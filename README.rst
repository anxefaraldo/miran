miran
=====
MIRAN in a python library that includes various modules and simple command-line programs to execute recurrent operations regarding automatic key estimation from audio and other tonality related stuff for analyising Electronic Dance Music. 
As such, it condenses most of the research done during my PhD in the area of computational key estimation:

Ángel Faraldo (2017). Tonality Estimation in Electronic Dance Music, A Computational and Musically Informed Examination. PhD Thesis. Universitat Pompeu Fabra, Barcelona.

The Python modules included facilitate the following operations:

* Download tracks and stems from Beatport.
* Evaluation definitions including the MIREX standard and my proposed methodologies.
* Various formatting functions to convert annotation formats from the most popular EDM key estimation applications.
* Key estimation algorithms as described in my PhD Dissertation.
* Utilities to parse excel spreadsheets, in order to facilitate the parsing and analysis of the data contained in the test collections used for my research.
* Plotting functions to obtain key distributions, tonality profiles and confusion matrices.


The MIRAN library depends on the following python libraries:

* essentia (Actually a C++ library, with Python bindings.)
* librosa
* madmom
* matplotlib
* numpy
* openpyxl
* pandas
* scipy
* seaborn
