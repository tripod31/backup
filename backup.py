#!/usr/bin/env python3

import os
import sys
import argparse
import re
from datetime import datetime
import tarfile
import configparser
import glob
import shutil

CONF_FILE=".config/backup.conf"
LIST_FILE="files.txt"

def read_config(path,args):
    '''
    read ini file and add value to args

    :param  path:   path of config file
    :param  args:   returned object from configparser.parse_args()
    '''

    if not os.path.exists(path):
        return
    config = configparser.ConfigParser()
    with open(path,'r') as f:
        config.read_file(f)
        f.close()

    d = vars(args)
    for (k,v) in config.items('settings'):
        d[k]=v

def find_all_files(directory):
    '''
    returns files under directory
    '''
    for root, _dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def is_word_contained_in_file(path,regex):
    #print(path)
    try:
        fi = open(path,'r')
        bHit = False
        line = fi.readline()
        while line:
            if regex.match(line):
                bHit = True
                break
            line = fi.readline()
        return bHit
    except Exception:
        #in case we can't read the file,etc
        return False

def search_files(keyword):
    '''
    :param    :keyword    regexp string
    '''
    print("=== searching files that contains keyword ===")
    regex = re.compile(keyword)
    arr =[]
    dirs=args.search_dir.split(',')
    for d in dirs:
        files = find_all_files(d)
        for path in files:
            if os.path.islink(path):
                continue
            if args.verbose:
                print(path)
            if is_word_contained_in_file(path,regex):
               arr.append(path) 
    return arr

def read_files():
    '''
    read LIST_FILE
    '''
    files =[]
    files_err =[]
    try:
        fi = open(LIST_FILE,'r')
    except Exception:
        print("can't read " + LIST_FILE)
        return files,files_err

    line = fi.readline()
    while line:
        path = line.strip()
        if line[0] != '#' and len(path)>0:
            try:
                ft=open(path)
                files.append(path)
                ft.close()
            except Exception:
                files_err.append(path)
        line = fi.readline()

    return files,files_err

def to_boolean(arg):
    ret = None
    if type(arg)==bool:
        ret = arg
    elif type(arg)==str:
        if arg.lower() in ["yes","true"]:
            ret = True
        elif arg.lower() in ["no","false"]:
            ret = False
    elif type(arg)==int:
        if arg == 1:
            ret = True
        elif arg ==0:
            ret = False
    return ret

def update_file_list(files):
    #update LIST_FILE
    files_found = search_files(args.keyword)
    files_diff = set(files_found).difference(set(files))
    if len(files_diff)==0:
        print("=== found nothing to add to {} ===".format(LIST_FILE))
        return

    files_found = sorted(list(files_diff))
    print("=== added these files that contains keywords to {} ===>".format(LIST_FILE))
    for f in files_found:
        print(f)
    print("<=====")

    #write to LIST_FILE
    if os.path.exists(LIST_FILE):
        shutil.copy(LIST_FILE,LIST_FILE+".old")

    with open(LIST_FILE, 'a+') as f:
        f.write("#append these files\n")
        for line in files_found:
            f.write(line+"\n")

if __name__ == '__main__':
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dst_dir',   default='.')
    parser.add_argument('--prefix',	default='backup',
                        help='prefix of tar file')
    parser.add_argument('-u','--update',     action='store_true',
                        help="search files that contains keyword search_dir.add those files to {},and exit.".format(LIST_FILE))
    parser.add_argument('--search_dir',
                        help="specify where to search files that contains keyword.")
    parser.add_argument('--keyword',
                        help='in /etc or home directory,if one line in flie starts with this keyword,the files are appended to tarfile.This is valid when search option is specified.')
    parser.add_argument('-v','--verbose',   action='store_true')
    parser.add_argument('-k','--keep_old',  action='store_true',
                        help="does'nt delete old tar file.")    

    args=parser.parse_args()

    #chdir to script dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    read_config(CONF_FILE,args)  #read args from config file

    #argument check
    if not os.path.exists(args.dst_dir):
        print("dst_dir %s not exists." % args.dst_dir)
        os.sys.exit(0)

    #list files to backup
    files,files_err = read_files()   #from LIST_FILE
    if len(files_err) >0:
        print ("=== can't read these files ====")
        for path in files_err:
            print(path)

        print("input 'y' to continue:",end="")
        ans = input()
        if ans != 'y':
            print("quit")
            sys.exit()

    if args.update and args.keyword and args.search_dir:
        update_file_list(files)
        os.sys.exit(0)

    if to_boolean(args.keep_old) == False:
        #delete old tar file
        for path in glob.glob("%s/%s_*.tar.gz" % (args.dst_dir,args.prefix)):
            os.remove(path)

    #write to tarfile
    now = datetime.now()
    tarfname  = "%s/%s_%s.tar.gz" % (args.dst_dir,args.prefix,now.strftime('%Y%m%d'))
    tar = tarfile.open(tarfname,'w:gz')
    print("=== backup these files ===")
    for file in files:
        print (file)
        tar.add(file)
