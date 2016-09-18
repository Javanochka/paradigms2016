#!/usr/bin/python3
import argparse
import os
from hashlib import sha1 as niceHasher 
import re

def getAllFiles(dirpath):
    res = []
    pattern = re.compile(r"~|\.")
    for dirp, _, files in os.walk(dirpath):
        res += [os.path.join(dirp, f) for f in files if not pattern.match(f)]
    return res

def getHashOfFile(filepath):
    hasher = niceHasher()
    with open(filepath, mode='rb') as f:
        dose = 0
        while dose != b'':
            dose = f.read(1024)
            hasher.update(dose)
    return hasher.hexdigest()

def getDictOfFiles(listOfFiles, fullpath, fplen):
    res = {}
    for f in listOfFiles:
        hashf = getHashOfFile(f)
        if not hashf in res:
            res[hashf] = []
        res[hashf].append(f if fullpath else f[fplen:])
    return res

def printSimilarities(dirpath, fullpath, fplen):
    dic = getDictOfFiles(getAllFiles(dirpath), fullpath, fplen)
    res = [l for l in dic.values() if len(l) > 1]
    for l in res:
        print(":".join(l))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="finds in directory all equal files")
    parser.add_argument("-f", "--fullpath", action="store_true") #else path in given directory
    parser.add_argument("path", type=str)
    args = parser.parse_args()
   # res = getEquals(args.path) 
    pathdir = os.path.abspath(args.path)
    printSimilarities(pathdir, args.fullpath, len(pathdir)+1)
"""    
    if args.fullpath:
        pass
    else:
        pass
"""
