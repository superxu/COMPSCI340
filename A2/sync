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
        #print(dirname + " does not exist.")
        return False
    else:
        if not os.path.isdir(dirname):
            #print(dirname + " is not a directory.")
            return False

    return True

   


def check_syncfile_in_dir(dirname):
    if not os.path.exists(dirname + "/" + ".sync"): 
        #print(dirname + "/" + ".sync file does not exist.")
        return False

    return True




def gen_file_sha256(filename):
    f = open(filename, "rb")
    sh = hashlib.sha256()
    sh.update(f.read())
    SHA256_VALUE = sh.hexdigest()
    f.close()
    return SHA256_VALUE



def compare_digest(value1, value2):
    #print(value1 == value2)
    if value1 == value2:
        return True

    return False



'''
def compare_mtime(t1, t2):
    print("compare_mtime")
    print("t1 = %s t2 = %s" % (t1, t2))
    print(t1 < t2)
    latest = max((t1, t2))
    print(latest)

    return latest
'''


def compare_mtime(t1, t2):
    #print("compare_mtime")
    #print("t1 = %s t2 = %s" % (t1, t2))
    return (t1 > t2)



# if a key is not in old_values, new file added
# if a key is in old_values, but not in new_values, this file is deleted
def check_file_deleted(old, new):
    for key in old.keys():
        if not (key in new.keys()):
            if not (old[key][0][1] == "deleted"):
                #print("Filename: %s is deleted." % key)
                # what's the modification time of a deleted file? Now?
                # build deleted information
                delete_info = []
                # you do not know when the file is deleted, so just use current time.
                deleted_time = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime())
                delete_msg = "deleted"
                delete_info.append(deleted_time)
                delete_info.append(delete_msg)

                old[key].extend([delete_info])
                old[key].reverse()





def get_syncfile_content(dirname):
    syncfile = dirname + "/"+ ".sync"
    values = {}

    if not os.stat(syncfile).st_size == 0:
        fd_read =  open(syncfile, "r")
        values = json.load(fd_read)
        fd_read.close()

    return values



def write_sha256_tofile(dirname, new_values):
    newfilelist = os.listdir(dirname)
    syncfile = dirname + "/"+ ".sync"

    # get history values first
    old_values = get_syncfile_content(dirname)
    #print("old_values = %s" % old_values)

    if os.stat(syncfile).st_size == 0:
        fd_write_first =  open(syncfile, "w")
        json.dump(new_values, fd_write_first, indent=8)
        fd_write_first.close()
    else:
        fd_write =  open(syncfile, "w")
        for i in range(0, len(newfilelist)):
            if newfilelist[i] == ".sync":   
                pass
            else: 
                # check if file(key) exisits
                if not (newfilelist[i] in old_values.keys()):
                    # new file added
                    #print("Not exists!")
                    old_values[newfilelist[i]] = new_values[newfilelist[i]]
                else:
                    #print("Already exists!")
                    # compare digest 
                    if not compare_digest(old_values[newfilelist[i]][0][1], new_values[newfilelist[i]][0][1]):
                        #print("new digest = %s" % new_values[newfilelist[i]][0][1])
                        #print("old digest = %s" % old_values[newfilelist[i]][0][1])

                        old_values[newfilelist[i]].extend(new_values[newfilelist[i]]) 
                        # it seems nothing wrong with reverse or sort. even I comment reverse() below, the position/order of keys may still change
                        old_values[newfilelist[i]].reverse()


        #check if files are deleted
        check_file_deleted(old_values, new_values)
        json.dump(old_values, fd_write, indent=8)
        fd_write.close()


# add new key/value pair
# find exisited key and extend it
def update_syncfile(dirname, key,  new_value):
    syncfile = dirname + "/"+ ".sync"

    # get history values first
    origin_values = get_syncfile_content(dirname)
    #print("origin_values = %s" % origin_values)


    if not (key in origin_values.keys()):
        fd_write_first =  open(syncfile, "w")
        origin_values[key] = [new_value]
        json.dump(origin_values, fd_write_first, indent=8)
        fd_write_first.close()

    else:
        fd_write =  open(syncfile, "w")
        origin_values[key].extend([new_value]) 
        # it seems nothing wrong with reverse or sort. even I comment reverse() below, the position/order of keys may still change
        origin_values[key].reverse()     
        json.dump(origin_values, fd_write, indent=8)
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
                last_modified = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(os.path.getmtime(dirname + "/"+ filelist[i])))

                #print(last_modified)
                valuelist = []
                valuelist.append(last_modified)
                valuelist.append(gen_file_sha256(dirname + "/"+ filelist[i]))

              #  sha256_values[filelist[i]] = valuelist
                sha256_values.setdefault(filelist[i], []).append(valuelist)
             

         # How to deal with this?
        elif (os.path.isdir(dirname + "/" + filelist[i])):
            subdir = dirname + "/" + filelist[i]
            print("sub directory name: %s" % subdir)
            gen_dir_sha256(subdir)
            
        else:
            pass

    # write SHA256 value to .sync file
    #print("sha256_values = %s" % sha256_values)
    write_sha256_tofile(dirname, sha256_values)








def create_syncfile(dirname):
    pre_position = os.popen("pwd").read().rstrip('\n')
    os.chdir(dirname)
    os.system("touch .sync")
    os.chdir(pre_position)



def create_syncfile_in_subdirectories():
    for dirname, dirnames, filenames in os.walk('.'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            subdir = os.path.join(dirname, subdirname)
            syncfile = subdir + "/" + ".sync"
            createfile = "touch %s" % syncfile
            os.system(createfile)

      

        # print path to all filenames.
        #for filename in filenames:
        #    print(os.path.join(dirname, filename))

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')




def create_syncfile_including_subdir(dirname):
    pre_position = os.popen("pwd").read().rstrip('\n')
    os.chdir(dirname)
    os.system("touch .sync")
    os.chdir(pre_position)
    # check if there are sub directories.
    create_syncfile_in_subdirectories()
  




def compare_syncfile_impl(dir1, dir2, file_a, file_b):

    for key in file_a.keys():
        file1 = dir1 + "/" + key
        file2 = dir2 + "/" + key
        if  key in file_b.keys():
            #print("digest1 = %s" % file_a[key][0][1])
            #print("digest2 = %s" % file_b[key][0][1])
            digest1 = file_a[key][0][1]
            digest2 = file_b[key][0][1]
            mtime1  = file_a[key][0][0]
            mtime2  = file_b[key][0][0]

            if compare_digest(digest1, digest2):
                #print("!!!!! Time1: %s !!!!!!" % (file_a[key][0][0] == file_b[key][0][0]))
                if not (mtime1 == mtime2):
                    if not compare_mtime(mtime1, mtime2):
                        # change mtime to the earlier mtime, how to change a file's modification time?
                        stinfo = os.stat(file1)
                        os.utime(file2, (stinfo.st_atime, stinfo.st_mtime))
                        # update sync file entry
                        #print("add new key value: modification time = %s" % file_a[key][0][1])
                        update_syncfile(dir2, key, file_a[key][0])


            # file content is different
            else:
                #print("!!!!!! Time2: %s !!!!!!" % (file_a[key][0][0] == file_b[key][0][0]))
                if (digest1 == "deleted") or (digest2 == "deleted"):
                    if digest1 == "deleted":
                        found_early_digest = False  
                        for i in range(len(file_a[key])):
                            if digest2 == file_a[key][i][1]:
                                found_early_digest = True

                        if found_early_digest == True:
                            os.system("rm %s" % file2)
                            # update sync file entry
                            update_syncfile(dir2, key, file_a[key][0])
                        else:
                            os.system("cp %s %s" % (file2, file1))
                            stinfo = os.stat(file2)
                            os.utime(file1, (stinfo.st_atime, stinfo.st_mtime))
                            # update sync file entry
                            update_syncfile(dir1, key, file_b[key][0]) 
                    else:
                        pass


                else:
                    if not (mtime1 == mtime2):
                        if not compare_mtime(mtime1, mtime2):
                            os.system ("cp %s %s" % (file2, file1))
                            stinfo = os.stat(file2)
                            os.utime(file1, (stinfo.st_atime, stinfo.st_mtime))
                            # update sync file entry
                            #print("add new key value = %s" % file_b[key][0])
                            update_syncfile(dir1, key, file_b[key][0])

                    # different content, same mtime
                    else:
                        found_early_digest = False  
                        for i in range(len(file_b[key])):
                            if digest1 == file_b[key][i][1]:
                                found_early_digest = True


                        if found_early_digest == True:
                            os.system ("cp %s %s" % (file2, file1))
                            stinfo = os.stat(file2)
                            os.utime(file1, (stinfo.st_atime, stinfo.st_mtime))
                            # update sync file entry
                            update_syncfile(dir1, key, file_b[key][0])


        else:
            # if a file does not exist in another directory, I need to copy it.
            os.system ("cp %s %s" % (file1, file2))
            stinfo = os.stat(file1)
            os.utime(file2, (stinfo.st_atime, stinfo.st_mtime))
            # update sync file entry
            update_syncfile(dir2, key, file_a[key][0])




def compare_syncfile(dir1, dir2):
    syncfile1 = get_syncfile_content(dir1)
    syncfile2 = get_syncfile_content(dir2)
    #print("syncfile1 = %s" % syncfile1)
    #print("syncfile2 = %s" % syncfile2)

    compare_syncfile_impl(dir1, dir2, syncfile1, syncfile2)


    syncfile1 = get_syncfile_content(dir1)
    syncfile2 = get_syncfile_content(dir2)

    compare_syncfile_impl(dir2, dir1, syncfile2, syncfile1)




def main():

    # check number of arguments
    if (len(sys.argv) < 3):
        print("Usage: sync directory1 directory2")
        return

    # check if directory exists and is directory
    if ((not check_dir(sys.argv[1])) and (not check_dir(sys.argv[2]))):
        print("Usage: sync directory1 directory2")
        return


    if not check_dir(sys.argv[1]):
        os.makedirs(sys.argv[1], exist_ok = True)
    else:
        os.makedirs(sys.argv[2], exist_ok = True)
    

    # check if .sync file exists
    if not check_syncfile_in_dir(sys.argv[1]):
        # create .sync file
        #create_syncfile(sys.argv[1])
        create_syncfile_including_subdir(sys.argv[1])
   
    # generate SHA256 of files in the directory
    gen_dir_sha256(sys.argv[1])


    if not check_syncfile_in_dir(sys.argv[2]):
        # create .sync file
        #create_syncfile(sys.argv[2])
        create_syncfile_including_subdir(sys.argv[2])
    
    # generate SHA256 of files in the directory
    gen_dir_sha256(sys.argv[2])


    compare_syncfile(sys.argv[1], sys.argv[2])
    


if __name__ == "__main__":
    main()

