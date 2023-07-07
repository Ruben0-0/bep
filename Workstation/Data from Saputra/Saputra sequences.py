import pandas as pd
import numpy
# Custom imports:
from Synthetic_Sequencer import synthtools as syn
from Burgess_Model import main as burg

# Read the excel file:
df1 = pd.read_excel('Saputra Logs.xlsx', sheet_name='depfa_1')
df2 = pd.read_excel('Saputra Logs.xlsx', sheet_name='depfa_2')
df3 = pd.read_excel('Saputra Logs.xlsx', sheet_name='depfa_3')
# Extract the depth and code profiles as numpy arrays:
depth_profile_1, code_profile_1 = df1.iloc[:, 0].to_numpy(), df1.iloc[:, 1].to_numpy().astype(int)
depth_profile_2, code_profile_2 = df2.iloc[:, 0].to_numpy(), df2.iloc[:, 1].to_numpy().astype(int)
depth_profile_3, code_profile_3 = df3.iloc[:, 0].to_numpy(), df3.iloc[:, 1].to_numpy().astype(int)
# Convert code profiles to flagged profiles:
code_dict = {'0': 'Fluv.', '1': 'U.Delta', '2': 'L.Delta', '3': 'Coast.', '4': 'N.Shore', '5': 'Marine'}
flagged_profile_1 = syn.coded_to_flagged(code_profile_1, code_dict)
flagged_profile_2 = syn.coded_to_flagged(code_profile_2, code_dict)
flagged_profile_3 = syn.coded_to_flagged(code_profile_3, code_dict)
# Convert the flagged profiles to a list of depth boundaries and lithological units:
depths1, lith1 = syn.flagged_reader(depth_profile_1, flagged_profile_1)
depths2, lith2 = syn.flagged_reader(depth_profile_2, flagged_profile_2)
depths3, lith3 = syn.flagged_reader(depth_profile_3, flagged_profile_3)
# Create a layout dictionary:
seq_facies = ['Fluv.', 'U.Delta', 'L.Delta', 'Coast.', 'N.Shore', 'Marine']
colors = ['gold', 'yellowgreen', 'mediumspringgreen', 'cyan', 'cornflowerblue', 'navy']
patterns = ['o.', '\ \*', '\ \o', '\ \.', '-.-', '--']
layout = dict()
for i in range(len(seq_facies)):
    layout[seq_facies[i]] = [colors[i], patterns[i]]
# Set filepath, res and n (res and n are here only relevant for figure size and y-tick configuration):
filepath = r'D:\AESB\AESB3\BEP\Figures\04 - Results\Saputra logs'
res = 5
n = 6
# Run the data through the Burgess model:
result1_1, result2_1, result3_1 = burg.main(depths1, lith1, layout, res, n, filepath=filepath + r'\Log 1')
result1_2, result2_2, result3_2 = burg.main(depths2, lith2, layout, res, n, filepath=filepath + r'\Log 2')
result1_3, result2_3, result3_3 = burg.main(depths3, lith3, layout, res, n, filepath=filepath + r'\Log 3')
