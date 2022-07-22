import argparse
import pandas
import matplotlib.pyplot as plt

def main(args):
    stat_data = pandas.read_csv(args.path)    
    tcp_data = stat_data[stat_data['Protocol'] == 'tcp']
    tcp_data.plot(x = 'Ave arrive time (unit: ms)', y = 'Physical distance', xlabel = 'Round travel time (ms)', 
                    ylabel = "Physical distance (Km)", kind = 'scatter')
    plt.savefig(args.outputPath + args.prefix + 'rtt-phyDistance.png')

    tcp_data = stat_data[stat_data['Protocol'] == 'tcp']
    tcp_data.plot(x = 'Average hop needed', y = 'Physical distance', xlabel = 'Number of hops needed', 
                    ylabel = "Physical distance (Km)", kind = 'scatter')
    plt.savefig(args.outputPath + args.prefix + 'hops-phyDistance.png')

    
    tcp_data = stat_data[stat_data['Protocol'] == 'tcp']
    tcp_data.plot(x = 'Average hop needed', y = 'Ave arrive time (unit: ms)', xlabel = 'Number of hops', 
                    ylabel = "Round travel time (ms)", kind = 'scatter')
    plt.savefig(args.outputPath + args.prefix + 'rtt-hops.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "A script to convert large-scale traceroute csv data to diagram.")
    parser.add_argument('-p', '--path', required=True, help='''The path to the csv file''')
    parser.add_argument('-o', '--outputPath', default='', help='The path to the output folder')
    parser.add_argument('--prefix', default="", help = "Prefix name for the output diagram")
    args = parser.parse_args()
    main(args)