#!/usr/bin/python3
import argparse
import os
from hashlib import sha1 as niceHasher 
from collections import defaultdict
import re

def getAllFiles(dirpath):
    pattern = re.compile(r"~|\.")
    for dirp, _, files in os.walk(dirpath):
        for f in files: 
            if not pattern.match(f) and not os.path.islink(f):
                yield os.path.join(dirp, f)

def getHashOfFile(filepath):
    hasher = niceHasher()
    with open(filepath, mode='rb') as f:
        dose = 0
        while dose != b'':
            dose = f.read(1024)
            hasher.update(dose)
    return hasher.hexdigest()

def getDictOfFiles(listOfFiles, fullpath, dirpath):
    res = defaultdict(list)
    for f in listOfFiles:
        hashf = getHashOfFile(f)
        res[hashf].append(f if fullpath else os.path.relpath(f, start=dirpath))
    return res

def printSimilarities(dirpath, fullpath):
    dic = getDictOfFiles(getAllFiles(dirpath), fullpath, dirpath)
    res = (l for l in dic.values() if len(l) > 1)
    for l in res:
        print(":".join(l))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="finds in directory all equal files")
    parser.add_argument("-f", "--fullpath", action="store_true") #else shortpath in given directory
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    pathdir = os.path.abspath(args.path)
    printSimilarities(pathdir, args.fullpath)

