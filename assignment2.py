#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Nithurshan Raveendran"
Semester: "Winter"

The python code in this file is original work written by
"Nithurshan". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os, sys

def parse_command_args() -> object:

    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")

    # To add length argument for graph length
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=20,
        help="Specify the length of the graph. Default is 20."
    )

    # To add human readable argument for human-readable output
    parser.add_argument(
        "-H", "--human-readable",
        action="store_true",
        help="Prints sizes in human-readable format"
    )

    # To add running-only argument for showing running processes only
    parser.add_argument(
        "-r", "--running-only",
        action="store_true",
        help="Only display running processes (optional)."
    )

    # Parse and return the argument
    parser.add_argument(
        "program",
        type=str,
        nargs="?",
        help="If a program is specified, show memory use of all associated processes. Show only total use if not."
    )

    return parser.parse_args()
#---------------------------------------------------------------------------------------------------------------------------------------------
                                                    # MILESTONE 01

# percent to graph function
def percent_to_graph(percent: float, length: int=20) -> str: 
    "turns a percent 0.0 - 1.0 into a bar graph"

    # Ensure percent is fasten between 0.0 and 1.0 to prevent invalids inputs
    percent = max(0.0, min(percent, 1.0))

    # Calculate the filled length based on the percentage and total length, defined using the given formula
    filled_length = int(percent * length)  

    # To construct the bar graph by combining filled '#' characters and empty spaces to match the total length
    bar_graph = f"{'#' * filled_length}{' ' * (length - filled_length)}"

    # Return the final output of constructed graph
    return bar_graph



def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    """This returns the total system memory in kilobytes by reading the memtotal entry from /proc/meminfo"""
    
    try: 
        # Open the file from the path in read mode to retrieve system memory details
        with open("/proc/meminfo", "r") as file:
            # Iterate throughout each line in the file and check if the a line starts with 'MemTotal'
            for line in file:
                if line.startswith("MemTotal:"):
                    # Draw out system memory value from the file and return as an interger in kilobytes.
                    return int(line.split()[1])
    
    # To handle incase file is not found or any other errors occur and exit the program with an error status to indicate the failure
    except FileNotFoundError:
        print("Error: /proc/meminfo file not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading system memory: {e}")
        sys.exit(1)

def get_avail_mem() -> int:
    "return total memory that is available"
    try:
        # Open the file in read mode to retrieve system memory details
        with open("/proc/meminfo", "r") as file:

            # Variables for free memory and free swap memory
            mem_free = 0
            swap_free = 0

            # To iterate each line in the file and check if it contains 'MemAvailable' and return the memory value in integer in kb
            for line in file:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1])
                
                # To check if line contains 'MemFree' for free memory fallback and extract it in kb and store it
                elif line.startswith("MemFree:"):
                    mem_free = int(line.split()[1])

                # To check if the line contains 'SwapFree' for free swap free memory fallback and then to extract it in kb and store it
                elif line.startswith("SwapFree:"):
                    swap_free = int(line.split()[1])

            # This is to fall back to sum of MemFree and SwapFree if 'memAvailable' is not found and return the sum of free memory and free swap memory        
            if mem_free and swap_free:
                return mem_free + swap_free
            
            # To raise an error if no valid memory info is available  and handle cases where file not found and print the error status and exit the program
            raise ValueError("MemAvailable not found, and fallback values are incomplete.")
    except FileNotFoundError:
        print("Error: /proc/meminfo file not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading available memory: {e}")
        sys.exit(1)
    
#---------------------------------------------------------------------------------------------------------------------------------------------

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_args()

    # If no program is provided, show system-wide memory usage
    if not args.program:
        # To print system-wide memory visualization
        print(f"System-wide memory visualization. Graph length: {args.length}")

        # check if output should be in human readable format and print a message
        if args.human_readable:
            print("Outputting in human-readable format.")

        # To check if only running processes should be displayed and print a message
        if args.running_only:
            print("Only displaying running processes (no program specified).")
    else:
        # Print a message indicating program-specific memory visualization
        print(f"Program-specific memory visualization for {args.program}. Graph length: {args.length}")

        # check if output should be in human readable format and print a message
        if args.human_readable:
            print("Outputting in human-readable format.")

        # Check if only running processes for the specified program should be displayed and print a message
        if args.running_only:
            print("Only displaying running processes for the specified program.")

    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
