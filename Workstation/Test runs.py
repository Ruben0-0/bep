# Custom imports:
from Synthetic_Sequencer import synthseq as seq, noisify as noise
from Burgess_Model import main as burg

# TEST RUN 1; F = 4:
filepath = 'D:\AESB\AESB3\BEP\Figures'
## DEFINE PARASEQUENCE:
para_depths = [0, 2.5, 7, 10, 13, 20, 23]
para_lithologies = ['SST', 'SHSST', 'SLT', 'SH', 'VAAD', 'NEL']
colors = ['gold', 'goldenrod', 'chocolate', 'sienna', 'purple', 'maroon']
hatches = ['.', '.-', '-.-', '--', 'o.', '*.']
layout = dict()
for i in range(len(para_lithologies)):
    layout[para_lithologies[i]] = [colors[i], hatches[i]]
## Resolution and number of parasequences:
res = 0.25
n = 5
## Create synthetic sequence:
x, y, derivatives, bounds, dictionaries = seq.sequencer(para_depths, para_lithologies, layout, res, n,
                                                        alpha=0.4, beta=0.2, filepath=filepath)
depths, lithologies = noise.gaussian_noise(x, y, derivatives, bounds, dictionaries, layout, res, gamma=0.5,
                                           filepath=filepath)
## Create sequence w. perfect cyclicity:
depths2 = para_depths
for i in range(2*len(para_depths)-2):
    depths2.append(depths2[-1] + (depths2[i+1]-depths2[i]))
lithologies2 = para_lithologies + para_lithologies + para_lithologies
## Run Burgess model:
result1, result2 = burg.main(depths, lithologies, layout, res, n, filepath)
