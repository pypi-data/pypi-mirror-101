import os
import sys
import pandas as pd
from argparse import ArgumentParser


def read_columns(path):
    columns = []
    for elem in path:
        with open(elem, "r") as f:
                lines = f.readlines()
                for x  in lines:
                    columns.append(x.strip("\n"))
    return columns

def read_data(path, columns):
    dataframe = pd.read_csv(path, delim_whitespace= True, lineterminator='\n', names = columns, dtype=float )
    return dataframe

def check_path(path):
    for elem in path:
        if not os.path.isfile(elem):
            return None
    return True
def main(argv = sys.argv[1:]):
    print("_____________________________________________________")
    print("OpenCARP Analyzer")
    print("Extracts data and multiple txt files from Trace data created by openCARP at once.")
    print("_____________________________________________________")
    parser  = ArgumentParser()
    parser.add_argument("-c", "--columns", help = "Name of files that contain header data", nargs = "+")
    parser.add_argument("-t", "--trace", help="Trace data file, e.g. Trace_0.dat")
    parser.add_argument("-i", "--iion", help = "Ion you want to visualize, e.g. -i i_Ks ", nargs = "+")
    parser.add_argument("-v", "--version", help = "Displays current version of the script", nargs="?", const=True)

    args = parser.parse_args()

    if args.version:
        print("Version 1.0, Crossplatfrom compatible build.")
        print("Report Issues,Suggestions opencarp@regdelivery.de")
        exit()


    if not args.columns or check_path(args.columns) is None:
        print("[ERROR] Either you did not specify a header file or specified file does not exist.")
        exit()
    if not args.trace or os.path.isfile(args.trace) is None:
        print("[ERROR] Please specify a trace file with -t or --trace.")
        exit()

    columns = read_columns(args.columns)

    if not args.iion:
        print("[ERROR] Please input at least one Ion.")
        print(f"Currently you have following choices from {','.join(args.columns)}")
        print(*columns)
        exit()

    for elem in args.iion:
        if not elem in columns:
            print(f"[ERROR] {elem} is not in your header files")
            exit()

    columns.insert(0,"time")
    df = read_data(args.trace, columns)

    for elem in args.iion:
        c = 0
        time = df["time"]
        value = df[elem]
        lines = []
        for i in range(0, len(value)):
            lines.append(str(time[i]) +" "+  str(float(value[i]))+ os.linesep)
        with open (elem + ".txt", "w") as f:
            f.writelines(lines)
        print("[INFO] ", elem + ".txt was generated.")


if __name__ == "__main__":
    main()