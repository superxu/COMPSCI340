#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Name: Shupeng Xu  UPI: sxu487   Student ID: 8260026


import sys
import os
import hashlib
import json
import time
import datetime


def check_dir(dirname):
    # python3 -O a2.py dir1 dir2, __debug__ will be false.
    if not os.path.exists(dirname): 
        print(dirname + " does not exist.")
        return False
    else:
        if not os.path.isdir(dirname):
            print(dirname + " is not a directory.")
            return False

    return True

   


def check_syncfile_in_dir(dirname):
    if not os.path.exists(dirname + "/" + ".sync"): 
        print(dirname + "/" + ".sync file does not exist.")
        return False

    return True




def gen_file_sha256(filename):
    f = open(filename, "rb")
    sh = hashlib.sha256()
    sh.update(f.read())
    SHA256_VALUE = sh.hexdigest()
    f.close()
    return SHA256_VALUE


def compare_digest():
    pass




def compare_mtime():
    pass



def write_sha256_tofile(dirname, values):
    filelist = os.listdir(dirname)
    syncfile = dirname + "/"+ ".sync"
    #filedata = {}
    print("file size = %s" % os.stat(syncfile).st_size)
    #print("values = %s" % values)
    # get history values first
    if not os.stat(syncfile).st_size == 0:
        fd_read =  open(syncfile, "r")
        filedata = json.load(fd_read)
        print("filedata = %s"  % filedata)
        fd_read.close()


    if os.stat(syncfile).st_size == 0:
        fd_write_first =  open(syncfile, "w")
        json.dump(values, fd_write_first, indent=8)
        fd_write_first.close()
    else:
        fd_write =  open(syncfile, "w")
        json.dump(values, fd_write, indent=8)
        for i in range(0, len(filelist)):
            if (os.path.isfile(dirname + "/" + filelist[i])):
                # do not calculate SHA256 of .sync file
                if filelist[i] == ".sync":   
                    pass
                else: 
                    print("filename = %s new value = %s" % (filelist[i], values[filelist[i]]))
                    print("filename = %s old value = %s" % (filelist[i], filedata[filelist[i]]))

        '''
        if not (filelist[i] in d):
            print("Not exists!")
            d[filelist[i]] = values
        else:
            print("Already exists!")
        '''
        json.dump(values, fd_write, indent=8)
        fd_write.close()



def gen_dir_sha256(dirname):
    filelist = os.listdir(dirname)

    if len(filelist) == 0:
        return

    syncfile = dirname + "/"+ ".sync"
    sha256_values = {}


    for i in range(0, len(filelist)):
        if (os.path.isfile(dirname + "/" + filelist[i])):
            # do not calculate SHA256 of .sync file
            if filelist[i] == ".sync":   
                pass
            else: 
                print(filelist[i])
                # No time zone info now (pytz seems good, but it's third party)and time format does not seem good...
                #print(time.tzname)
 
                t = (os.path.getmtime(dirname + "/"+ filelist[i]))  
                last_modified = datetime.datetime.fromtimestamp(t)
                #print(last_modified)
                valuelist = []
                valuelist.append(last_modified.isoformat())
                valuelist.append(gen_file_sha256(dirname + "/"+ filelist[i]))
                sha256_values[filelist[i]] = valuelist
             
                # write SHA256 value to .sync file
                print("sha256_values = %s" % sha256_values)
                write_sha256_tofile(dirname, sha256_values)

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

