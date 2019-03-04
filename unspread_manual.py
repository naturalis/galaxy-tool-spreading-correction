#!/usr/local/bin/python3
import os, sys,re
import argparse
import pandas as pd
import numpy as np
from matplotlib import use
import matplotlib.pyplot as plt
from statsmodels.sandbox.stats.multicomp import multipletests
import statsmodels.api as sm
from scipy.stats import hypergeom
from scipy.linalg import solve_sylvester
from scipy.stats import binom_test
from patsy import dmatrices

parser = argparse.ArgumentParser(description='Unspread: Computational correction of barcode index spreading')
parser.add_argument('filename', metavar='filename', type=str, nargs=1,help='.csv file with counts' )
parser.add_argument('--i5', metavar='STRING', type=str, nargs=1, default=['i5.index.name'], help='Index name of i5 barcodes (default: \'i5.index.name\')')
parser.add_argument('--i7', metavar='STRING', type=str, nargs=1, default=['i7.index.name'], help='Index name of i7 barcodes  (default: \'i7.index.name\')')
parser.add_argument('--rows', metavar='INTEGER', default=[16], type=int, nargs=1, help='Number of rows in plate (default: 16)')
parser.add_argument('--cols', metavar='INTEGER', default=[24], type=int, nargs=1,  help='Number of columns in plate (default: 24)')
parser.add_argument('--idx_col', metavar='INTEGER', default=[0], type=int, nargs=1,  help='Which column serves as the index (default: 0)')
parser.add_argument('--sep', metavar='CHAR', default=[','], type=str, nargs=1,  help='The separator in the .csv file (default \',\')')
parser.add_argument('--c', metavar='INTEGER', default=[5], type=int, nargs=1, help='Cutoff to remove addition false positives (default: 5)')
parser.add_argument('--idx_in_id', metavar='BOOLEAN', default=[0], type=float, nargs=1, help='If the index is in the cell id (i.e. cellid_i5_i7) (Default: 0 (False), set to 1 otherwise (True))')
parser.add_argument('--delim_idx', metavar='CHAR', default=['_'], type=str, nargs=1, help='If the index is in the cell id, the delimiting character (Default: \'_\')')
parser.add_argument('--column', metavar='BOOLEAN', default=[1], type=int, nargs=1, help='If each column is represents a cell, otherwise each row. (default: 1 (True), set to 0 otherwise (False))')
parser.add_argument('--output_folder', metavar='STRING',dest='output_folder', type=str, required=True)
parser.add_argument('--conditional_spreading_input', metavar='FLOAT',dest='conditional_spreading_input', type=str, required=False, nargs='?')

args = parser.parse_args()
filename = args.filename[0]
i5_index_name = args.i5[0]
i7_index_name = args.i7[0]
separator = args.sep[0]
n_rows = args.rows[0]
n_cols = args.cols[0]
idx = args.idx_col[0]
c = args.c[0]
column = args.column[0]
idx_in_id = args.idx_in_id[0]
delim_idx = args.delim_idx[0]

# Load in count table
df = pd.read_csv(filename, index_col=idx, sep=separator)
# Transform the data frame if each column represents a cell
if np.bool_(column):
    df = df.T
# Turns the end of the cell id strings into index name ids
if np.bool_(idx_in_id):
    i5_index_list = []
    i7_index_list= []
    for i,string in enumerate(df.index.values):
        sp = string.split(delim_idx)
        i5_index_list.append(sp[-2])
        i7_index_list.append(sp[-1])
    df[i5_index_name] = i5_index_list
    df[i7_index_name] = i7_index_list
df = df.sort_values(by=[i5_index_name,i7_index_name], ascending=[False, True])
df = df.loc[:,~df.columns.duplicated()]
df_noindex = df.drop([i5_index_name,i7_index_name], axis=1).astype(np.int)

base = os.path.splitext(os.path.basename(filename))[0]
#rate_spreading = np.median(prop_spread[test_bias != 1][mt].flatten()[prop_spread[test_bias != 1][mt].flatten() != 0])
rate_spreading = float(args.conditional_spreading_input)
print("Spreading correction with a manual spread rate: "+str(rate_spreading))

plt.tight_layout()
plt.savefig('{}_figures.pdf'.format(args.output_folder+base))

# Setting the rate of spreading matricies
column_spread = np.zeros((n_rows, n_rows))
row_spread = np.zeros((n_cols,n_cols))
column_spread[:,:] = rate_spreading
row_spread[:,:] = rate_spreading
np.fill_diagonal(column_spread, 0.5 - rate_spreading/2)
np.fill_diagonal(row_spread, 0.5 - rate_spreading/2)

# The function which does the correction, you can set the cutoff yourself
def adjust_reads(mat, i, column_spread = column_spread, row_spread = row_spread, cutoff = c, r = n_rows, c = n_cols):
    mat = np.array(mat).flatten()
    mat = mat.reshape(r,c)
    adjusted_reads = np.rint(solve_sylvester(column_spread,row_spread,mat))

    #A small change to the original script to avoid higher counts
    matdiff = np.subtract(adjusted_reads, mat)
    matdiff[matdiff > 0] = 0
    adjusted_reads2 = np.add(mat, matdiff)
    adjusted_reads2[adjusted_reads2 < cutoff] = 0

    return adjusted_reads2

adj_list = []
for i, col in df_noindex.items():
    adj_list.append(adjust_reads(col, i).flatten())

# Put correction into a dataframe and save to a .csv file
df_adj = pd.DataFrame(data=adj_list, index = df_noindex.columns.values, columns= df_noindex.index.values).T

df_adj = pd.concat([df[i7_index_name], df[i5_index_name] , df_adj], axis = 1)

df_adj.to_csv('{}_corrected.csv'.format(args.output_folder+base))
