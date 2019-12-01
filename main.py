#/usr/bin/env python3
import argparse
import os
import sys

from pageparser import parse_files
from pagerank import PageRank


def main():
    # Command line arguments options
    parser = argparse.ArgumentParser(description="Calculate the pagerank for \
        inside a directory.")
    parser.add_argument("-d", 
        help = "Set the directory containing the pages .html. Default = pages.")
    parser.add_argument("-a",
        help = "Set the teleport probability between [0,1]. Default = 0.1.")
    parser.add_argument("-e", 
        help = "Set the acceptable error for the Pagerank algorithm. \
        Default: 0.001.")
    parser.add_argument("-c", action = 'store_true',
        help = "Set for correction of dangling nodes. Default: off.")
    parser.add_argument("-l", action = 'store_true',
        help = "Set where it should use the last iteraction PR value \
        or the current iteraction. Default: current.")
    parser.add_argument("-n", action = 'store_true',
        help = "Set option to normalize values between 0-1 after the \
        acceptable error has been reached. Default: off.")

    args = parser.parse_args()
    # Default arguments for initialize PageRank and build_page_rank()
    pages_directory  = args.__dict__["d"] if args.__dict__["d"] else "pages"
    alpha_teleport   = float(args.__dict__["a"]) if args.__dict__["a"] else 0.1
    error_acceptable = float(args.__dict__["e"]) if args.__dict__["e"] else 0.001
    correct_dangling = args.__dict__["c"] 
    last_pr_value    = args.__dict__["l"]
    normalize_values = args.__dict__["n"]
    nodes, edges = parse_files(pages_directory)

    pagerank = PageRank(
        nodes = nodes, 
        edges = edges, 
        alpha = alpha_teleport,
        epsilon = error_acceptable)


    pagerank.create_graph()    
    pagerank.build_pagerank(
        correct_dangling, 
        last_pr_value,
        normalize_values)
    
    print_graph = input("\nShow graph structute and plot it? ")
    if(print_graph.lower() == "y"):
        print("Structure: ")
        print("Nodes: ", nodes)
        print("Edges: ", edges)
        pagerank.show_graph()


if __name__ == '__main__':
    main()