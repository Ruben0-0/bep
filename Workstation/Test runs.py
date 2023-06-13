import numpy as np
# Custom imports:
from Synthetic_Sequencer import synthseq as seq, noisify as noise
from Burgess_Model import main as burg

# TEST RUN 1; F = 5:
filepath1 = 'D:\AESB\AESB3\BEP\Figures\Coded profiles'
filepath2 = 'D:\AESB\AESB3\BEP\Figures\Synthetic Sequences'
## DEFINE PARASEQUENCE:
para_depths = [0, 2.5, 7, 10, 13, 14.3]
para_lithologies = ['SST', 'SHSST', 'SLT', 'SH', 'COAL']
colors = ['gold', 'goldenrod', 'chocolate', 'sienna', 'dimgray']
hatches = ['.', '.-', '-.-', '--', 'o.']
layout = dict()
for i in range(len(para_lithologies)):
    layout[para_lithologies[i]] = [colors[i], hatches[i]]
## Resolution and number of parasequences:
res = 0.25
n = 7
## Create synthetic sequence:
x, y, derivatives, bounds, dictionaries = seq.sequencer(para_depths, para_lithologies, layout, n, res,
                                                        alpha=0.4, beta=0.2, filepath=filepath2)
depths, lithologies = noise.gaussian_noise(x, y, derivatives, bounds, dictionaries, layout, gamma=0)
## Run Burgess model:
result1, result2 = burg.main(depths, lithologies, layout, filepath1)
