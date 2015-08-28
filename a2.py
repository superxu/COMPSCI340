#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Name: Shupeng Xu  UPI: sxu487   Student ID: 8260026


import sys
import os
import hashlib
import json


def check_dir(dirname):
    # python3 -O a2.py dir1 dir2, __debug__ will be false.
    if __debug__:
        return True
         
    if not os.path.exists(dirname): 
        print(dirname + " does not exist.")
        return False
    else:
        if not os.path.isdir(dirname):
            print(dirname + " is not a directory.")
            return False

    return True

   


def check_syncfile_in_dir(dirname):
    if __debug__:
        return True

    if not os.path.exists(dirname + "/" + ".sync"): 
        print(dirname + "/" + ".sync file does not exist.")
        return False

    return True




def gen_file_sha256(filename):
    print("gen_file_sha256")
    f = open(filename, "rb")
    sh = hashlib.sha256()
    sh.update(f.read())
    SHA256_VALUE = sh.hexdigest()
    f.close()
    return SHA256_VALUE




def gen_dir_sha256(dirname):
    print("gen_file_sha256")
    filelist = os.listdir(dirname)

    print("filelist = %s" % filelist)
    print("length = %s" % len(filelist));
    if len(filelist) == 0:
        return

    for i in range(0, len(filelist)):
        print("name = %s" % filelist[i])
        if (os.path.isfile(dirname + "/" + filelist[i])):
            # do not calculate SHA256 of .sync file
            if filelist[i] == ".sync":   
                pass
            else: 
                print(filelist[i])
                value = gen_file_sha256(dirname + "/"+ filelist[i])
                # write SHA256 value to .sync file
                with open(dirname + "/"+ ".sync", "a") as outfile:
                    json.dump(value, outfile)

        # How to deal with this?
        elif (os.path.isdir(dirname + "/" + filelist[i])):
            print("sub directory name: %s" % dirname + "/" + filelist[i])
        else:
            pass




def create_sync_file(dirname):
    pre_position = os.popen("pwd").read().rstrip('\n')
    os.chdir(dirname)
    os.system("touch .sync")
    os.chdir(pre_position)









def main():

    # check number of arguments
    if (len(sys.argv) < 3):
        print("Usage: ./sync dir1 dir2")
        if __debug__:
            pass
        else:
            return

    # check if directory exists
    if not check_dir(sys.argv[1]):
        return
    
    if not check_dir(sys.argv[2]):
        return

    # check if .sync file exists
    if not check_syncfile_in_dir(sys.argv[1]):
        # create .sync file
        create_sync_file(sys.argv[1])
    
    # generate SHA256 of files in the directory
    gen_dir_sha256(sys.argv[1])


    if not check_syncfile_in_dir(sys.argv[2]):
        # create .sync file
        create_sync_file(sys.argv[2])

    
    # generate SHA256 of files in the directory
    gen_dir_sha256(sys.argv[2])
    


if __name__ == "__main__":
    main()

