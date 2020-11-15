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
    parser.add_argument('--preview',    action='store_true',default=False,
                                    help="do not change files when specified")
    
    args=parser.parse_args()
    
    try:
        tar = tarfile.open(args.in_file,'r')
        os.chdir(args.dist_dir)
        for info in tar:
            if info.isfile():
                org_file = info.name
                bak_file = org_file +".bak"
                if os.path.exists(org_file):
                    if os.path.exists(bak_file):
                        print ("[%s]exists.skip renaminig"%bak_file)
                    else:
                        print( "rename:[%s]->[%s]"% (org_file,bak_file))
                        if not args.preview:
                            shutil.move(org_file,bak_file)
    except Exception as e:
        print(e)