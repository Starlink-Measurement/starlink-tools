import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pytz
import argparse

# Input argvs:  1 - input csv file name
#               2 - diagram output path (leave umpty will not save the image)

def main(args):
    df = pd.read_csv(args.path)
    df["timestamp"] = df["timestamp"].apply(lambda x: pd.to_datetime(x, unit = 's'))
    df["connection speed"] = df["connection speed"].apply(lambda x: int(''.join(c for c in x if c.isdigit())))
    df["network activity"] = df["network activity"].apply(lambda x: int(''.join(c for c in x if c.isdigit())))
    df["buffer health"] = df["buffer health"].apply(lambda x: float(''.join(c for c in x if c.isdigit() or c == '.')))

    # Edit here manually if you want to add the outage timestamp
    outages_time = pd.to_datetime(['2022-05-16 04:27 -0700', '2022-05-16 04:28 -0700', '2022-05-16 05:48 -0700'])
    outages_time = []

    hh_mm = DateFormatter('%H:%M:%S', tz = pytz.timezone('America/Vancouver'))

    fig1 = plt.figure(0)
    ax1 = df.plot(x = 'timestamp', y = 'buffer health', xlabel = 'time stamp', 
                ylabel = 'buffer health (second)', kind = 'scatter', figsize=(10,10))
    for ots in outages_time:
        plt.axvline(x = ots, linestyle = '-', color = 'r')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.xticks(rotation=60)
    ax1.xaxis.set_major_formatter(hh_mm)
    if args.outputPath != None:
        plt.savefig(args.outputPath + args.prefix + "buffer health.png")

    fig2 = plt.figure(1)
    ax2 = df.plot(x = 'timestamp', y = 'network activity', xlabel = 'time stamp', 
                ylabel = 'network activity (KB)', kind = 'scatter', figsize=(10,10))
    for ots in outages_time:
        plt.axvline(x = ots, linestyle = '-', color = 'r')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.xticks(rotation=60)
    ax2.xaxis.set_major_formatter(hh_mm)
    if args.outputPath != None:
        plt.savefig(args.outputPath + args.prefix + "network activity.png")

    fig3 = plt.figure(2)
    ax3 = df.plot(x = 'timestamp', y = 'connection speed', xlabel = 'time stamp',
                ylabel = 'connection speed (Kbps)', kind = 'scatter', figsize=(10,10))
    for ots in outages_time:
        plt.axvline(x = ots, linestyle = '-', color = 'r')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.xticks(rotation=60)
    ax3.xaxis.set_major_formatter(hh_mm)
    if args.outputPath != None:
        plt.savefig(args.outputPath + args.prefix + "connection speed.png")

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "This script will convert the Youtube scraper output file to a diagram.")
    parser.add_argument('-p', '--path', help='The path to the CSV input file', required=True)
    parser.add_argument('-o', '--outputPath', help='The path of the output diagram. The diagram will not be saved if left empty.')
    parser.add_argument('--prefix', help="The prefix of all diagram name.", default="")
    args = parser.parse_args()
    main(args)