#!/usr/bin/env python3
# A2 for COMPSCI340/SOFTENG370 2015
# Author: Name: Shupeng Xu  UPI: sxu487   Student ID: 8260026


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


def compare_digest(old, new):
    print(old == new)
    if old == new:
        return True

    return False




def compare_mtime():
    pass



def write_sha256_tofile(dirname, new_values):
    filelist = os.listdir(dirname)
    syncfile = dirname + "/"+ ".sync"
    #filedata = {}
    print("file size = %s" % os.stat(syncfile).st_size)
    #print("values = %s" % values)
    # get history values first
    if not os.stat(syncfile).st_size == 0:
        fd_read =  open(syncfile, "r")
        old_values = json.load(fd_read)
        fd_read.close()


    if os.stat(syncfile).st_size == 0:
        fd_write_first =  open(syncfile, "w")
        json.dump(new_values, fd_write_first, indent=8)
        fd_write_first.close()
    else:
        fd_write =  open(syncfile, "w")
        for i in range(0, len(filelist)):
            if (os.path.isfile(dirname + "/" + filelist[i])):
                # do not calculate SHA256 of .sync file
                if filelist[i] == ".sync":   
                    pass
                else: 
                    # check if file(key) exisits
                    if not (filelist[i] in old_values):
                        print("Not exists!")
                        old_values[filelist[i]] = new_values[filelist[i]]
                    else:
                        print("Already exists!")
                        # compare digest
                        if not compare_digest(old_values[filelist[i]][0][1], new_values[filelist[i]][0][1]):
                            print("new digest = %s" % new_values[filelist[i]][0][1])
                            print("old digest = %s" % old_values[filelist[i]][0][1])

                            old_values[filelist[i]].extend(new_values[filelist[i]]) 
                            old_values[filelist[i]].reverse()

                    
        json.dump(old_values, fd_write, indent=8)
        fd_write.close()



def gen_dir_sha256(dirname):
    filelist = os.listdir(dirname)

    if len(filelist) == 0:
        return

    print(filelist)

    syncfile = dirname + "/"+ ".sync"
    sha256_values = {}



    for i in range(0, len(filelist)):
        if (os.path.isfile(dirname + "/" + filelist[i])):
            # do not calculate SHA256 of .sync file
            if filelist[i] == ".sync":   
                pass
            else: 
            
                # No time zone info now (pytz seems good, but it's third party)and time format does not seem good...
                #print(time.tzname)
 
                t = (os.path.getmtime(dirname + "/"+ filelist[i]))  
                last_modified = datetime.datetime.fromtimestamp(t)
                #print(last_modified)
                valuelist = []
                valuelist.append(last_modified.isoformat())
                valuelist.append(gen_file_sha256(dirname + "/"+ filelist[i]))

              #  sha256_values[filelist[i]] = valuelist
                sha256_values.setdefault(filelist[i], []).append(valuelist)
             

         # How to deal with this?
        elif (os.path.isdir(dirname + "/" + filelist[i])):
            print("sub directory name: %s" % dirname + "/" + filelist[i])
        else:
            pass

    # write SHA256 value to .sync file
    print("sha256_values = %s" % sha256_values)
    write_sha256_tofile(dirname, sha256_values)








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

