#!/usr/bin/python

import argparse, sys, os
sys.path.append('./scripts')
import export, utility, gardening

run = 1

def main():
    global args
    global run

    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--export', help='Exporting stored data to a web page', required=False)
    parser.add_argument('-g','--gardening', help='Fetching data by the lighthouse service', required=False)
    parser.add_argument('-v','--verbose', help='Enable console output', required=False)
    parser.add_argument('-s','--not-saved', help='Disable the persistence of received data', required=False)
    parser.add_argument('-c','--config', help='Path to config file', required=False)
    parser.add_argument('-u','--url', help='Providing an URL to check', required=False)
    parser.add_argument('-n','--run', help='Number of runs', required=False)

    args = parser.parse_args()

    if not args.config is None:
        utility.set_config(args.config)

    if not args.run is None:
        run = int(args.run)

    if is_verbose():
        print(utility.get_config()['title'])
        print('======================')

    if not args.gardening is None:
        save = args.not_saved is None
        url = None
        if not args.url is None:
            url = args.url

        if is_verbose():
            print('Fetching lighthouse data')
        
        i = 1
        while i <= run:
            gardening.fetch_data(save, url)
            i += 1

    if not args.export is None:
        if is_verbose():
            print('Exporting dashboard to ' + os.path.abspath(os.getcwd()) + '/index.html')
        export.export_html()

def is_verbose():
    return not args.verbose is None

if __name__ == "__main__":
   main()