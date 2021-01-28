#!/usr/bin/env python3

import tarfile
import shutil
import os
import argparse

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file',help="tar file")
    parser.add_argument('--dist_dir','-d',default='/',help="dir to extract")
    
    args=parser.parse_args()
    
    files_exists =[]
    try:
        tar = tarfile.open(args.in_file,'r')
        os.chdir(args.dist_dir)
        for info in tar:
            if info.isfile():
                fname = info.name
                if os.path.exists(fname):
                    files_exists.append(fname)
    except Exception as e:
        print(e)

    if len(files_exists) > 0:
        print ("These files exist:")
        for f in files_exists:
            print(f)
    else:
        print ("No files exist")
