import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob
from argparse import ArgumentParser
import json
import numpy as np

class glob_vars():
     loc_positions = {
                            'best' : 	0,
                            'upper right': 1,
                            'upper left' : 2,
                            'lower left' : 3,
                            'lower right' : 4,
                            'right': 5,
                            'center left' : 6,
                            'center right' : 7,
                            'lower center' : 8,
                            'upper center'	: 9,
                            'center' : 	10
                            }

def read_data(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    return pd.read_csv(path, names=["Time", fname], delim_whitespace=True)

def version_reader():
    with open(os.path.join(os.path.dirname(__file__),"version.json"), "r") as f:
        return json.loads(f.read())

def is_int(s):
     try:
        int(s)
        return True
     except ValueError:
        return False
def is_float(s):
     try:
        float(s)
        return True
     except ValueError:
        return False

def main(argv = sys.argv[1:]):

    print("_____________________________________________________")
    print("OpenCARP Plotter")
    print("Plots multiple txt files created by opencarp at once.")
    print("_____________________________________________________")
    loc_positions = glob_vars.loc_positions
    parser = ArgumentParser()
    parser.add_argument("-f", "--files", help = "Files to Plot", nargs="+")
    parser.add_argument("-o", "--out", help = "Output image name")
    parser.add_argument("-i", "--ignore", help="Ignores a file name if this text exists in file", nargs="+")
    parser.add_argument("-t", "--title", help="Title of plot", nargs="+")
    parser.add_argument("-l", "--legend", help="Legend location in plot. Options: " + ",".join(loc_positions.keys()).upper(), nargs="+")
    parser.add_argument("-xlabel", help="Label for x-Axis in plot", nargs="+")
    parser.add_argument("-ylabel", help="Label for y-Axis in plot", nargs="+")
    parser.add_argument("-xlim", help="Limit for x-Axis, start and end separated by space.", nargs="+", type= int)
    parser.add_argument("-ylim", help="Limit for y-Axis, start and end separated by space.", nargs="+", type = int)
    parser.add_argument("-custom", help="Kwargs for matplotlib", nargs="+")
    parser.add_argument("-v", "--version", help = "Displays current version of the script", nargs="?", const=True)
    args = parser.parse_args()

    if args.version:
        version = version_reader()
        print (version["version"])
        print(version["version_description"])
        exit()


    if not args.files:
        print("[ERROR] Please specify at least one input file created by opencarp-analyzer with -f or --file file.txt")
        exit()

    if args.files:
        for item in args.files:
            if os.path.isdir(item):
                print("Looking for txt files in ", item)
                args.files.remove(item)
                args.files += glob.glob(os.path.join(item , "*.txt"))


    if any([x for x in args.files if "*" in x]):   #glob workaround for windows powershell because * does not pass list of files.
        for elem in args.files:
         args.files.remove(elem)
         args.files += glob.glob(elem)

    df_sum = pd.DataFrame({})
    for file in args.files:
        if not os.path.isfile(file):
            print("[WARNING]", file, " is not a valid file so it is going to be skipped ...")
            continue
        elif not args.ignore is None and  len([x for x in args.ignore if x in file]) > 0:
            print("[WARNING] Ignore (-i, --ignore) parameter was found in ", file, " skipping...")
            continue
        else:
            print("[INFO] Parsing data in ",file)
        df = read_data(file)
        if len(df_sum.columns) == 0:
            df_sum = df
        else :
            df_sum = pd.merge(df_sum, df, on="Time")

    if not len(df_sum.columns) == 0:
        if args.xlabel:
            xlabel = ' '.join(args.xlabel)
        else:
            xlabel = "Time (in ms)"
        if args.ylabel:
            ylabel = ' '.join(args.ylabel)
        else:
            ylabel = "Voltage (in mV)"
        if args.xlim:
            xlim = args.xlim
        else:
            xlim = None
        if args.ylim:
            ylim = args.ylim
        else:
            ylim = None
        if args.custom is None:
            custom_kwargs = {}
        else:
            custom_kwargs = {}

            #parsing custom kwargs for respecting datatypes for maximum compatibility with matplotlib kwargs
            for i in range(0,len(args.custom)-1,2):
                if args.custom[i+1].lower() == "true":
                    args.custom[i+1] = True
                elif args.custom[i+1].lower() =="false":
                    args.custom[i+1] = False
                elif "(" in args.custom[i+1]:
                    str_tuple = args.custom[i+1].replace("(","").replace(")","")
                    args.custom[i+1] = tuple([int(x) for x in str_tuple.split(",")])
                elif is_int(args.custom[i+1]):
                    args.custom[i+1] = int(args.custom[i+1])
                elif is_float(args.custom[i+1]):
                    args.custom[i+1] = float(args.custom[i+1])

                 #ready dict with string->dtype conversion
                custom_kwargs[args.custom[i]] = args.custom[i+1]


        if len(df_sum.columns) > 12:
            print("[WARNING] You are plotting a large dataframe. It might be hard to differentiate lines because of limited color palette.")

        df_sum.plot.line(x = "Time", xlabel= xlabel, ylabel=ylabel, xlim = xlim, ylim = ylim, **custom_kwargs)

        loc_input = 1
        if args.legend:
            leg = ' '.join(args.legend).lower()
            try:
                loc_input = loc_positions[leg]

            except:
                print("[WARNING]", leg, " is not a valid position. Valid positions are : ", ','.join(loc_positions.keys()).capitalize()  ,". Defaulting to UPPER RIGHT.")
                loc_input = 1

        plt.legend(loc=loc_input)
        if args.title:
            args.title = " ".join(args.title) #workaround if user inputs title without using ""
            plt.title(args.title)

        if not args.out:
            plt.show()
        else:
            plt.savefig(args.out)

    print("[EXIT] Done.")



if __name__ == "__main__":
    main()
