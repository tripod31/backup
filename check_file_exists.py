#!/usr/bin/env python3

import tarfile
import shutil
import os
import argparse

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file',    required=True)
    parser.add_argument('--dist_dir',   default='.')
    
    args=parser.parse_args()
    
    try:
        tar = tarfile.open(args.in_file,'r')
        os.chdir(args.dist_dir)
        for info in tar:
            if info.isfile():
                fname = info.name
                if os.path.exists(fname):
                    print ("{}:exists".format(fname))
    except Exception as e:
        print(e)