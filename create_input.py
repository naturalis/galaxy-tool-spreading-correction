import sys, os, argparse, string
import glob
from subprocess import call, Popen, PIPE
import pandas as pd

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='')
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument('-t', metavar='input otutable', dest='otutable', type=str,required=True)
requiredArguments.add_argument('-n', metavar='nextera sheet', dest='nextera', type=str,required=True)
requiredArguments.add_argument('-ot', metavar='output_transposed', dest='output_transposed', type=str, required=True)
requiredArguments.add_argument('-o', metavar='output', dest='output', type=str, required=True)
args = parser.parse_args()


pd.read_csv(args.otutable, sep='\t').T.to_csv(args.output_transposed, header=False, sep="\t")

nexteraDict = {}
with open(args.nextera) as nexterasheet:
    for sample in nexterasheet:
        if sample.split("\t")[0] != "#samplename":
            nexteraDict[sample.split("\t")[0]] = [sample.split("\t")[1], sample.split("\t")[2]]

with open(args.output_transposed) as otutable, open(args.output, "a") as output:
    for line in otutable:
        if line.split("\t")[0] == "#OTU ID":
            otus = "\t".join(line.split("\t")[1:])
            output.write("cell.name\tN.index.name\tS.index.name\t"+otus.strip()+"\n")
        else:
            if line.split("\t")[0] in nexteraDict:
                firstColumns = line.split("\t")[0]+"\t"+nexteraDict[line.split("\t")[0]][0]+"\t"+nexteraDict[line.split("\t")[0]][1]
                abundance = "\t".join(line.split("\t")[1:])
                output.write(firstColumns.strip()+"\t"+abundance.strip()+"\n")
