
import inspect
import os
import glob
import sys
import copy

from ._filetracker import nc_created
from ._filetracker import nc_safe
from ._remove import nc_remove
from ._session import session_stamp
from ._session import session_info

# keep is a file you do not want to delete

def cleanup(keep = None):
    """
    Temp file cleaner

    Remove all files created during the session that are now out of use
    """

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nchack has either created or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = copy.deepcopy(nc_created)
    # nc_created needs to only be files on the system for speed purposes
    for x in candidates:
        if os.path.exists(x) == False:
            nc_created.remove(x)

    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    #mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]

    other_files = []
    for ff in mylist:
        for cc in candidates:
            if cc in ff:
                other_files.append(ff)
      
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    #mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if session_stamp["stamp"] in f]
    for ff in mylist:
        other_files.append(ff)

    candidates = list(set(candidates + other_files))
    candidates = [x for x in candidates if os.path.exists(x)]
    candidates

    # Step 2 is to find the trackers in the locals
    
    valid_files = []
    valid_files = valid_files + nc_safe
    objects = dir(sys.modules["__main__"])
    for i in ([v for v in objects if not v.startswith('_')]):
        i_class = str(eval("type(sys.modules['__main__']." +i + ")"))
        if "NCData" in i_class and "List" not in i_class:
            i_current =eval("sys.modules['__main__']." +i + ".current")
            i_start = eval("sys.modules['__main__']." +i + ".start")
            # add the current files to valid_files
            if type(i_current) is str:
                valid_files.append(i_current)
            else:
                for ff in i_current:
                    valid_files.append(ff)

            # add the start files to valid_files
            if type(i_start) is str:
                if i_start not in nc_created:
                    valid_files.append(i_start)
            else:
                for ff in i_start:
                    if ff not in nc_created:
                        valid_files.append(ff)

            i_grid = eval("sys.modules['__main__']." +i + ".grid")
            i_weights = eval("sys.modules['__main__']." +i + ".weights")
            if i_grid is not None:
                valid_files.append(i_grid)
                valid_files.append(i_weights)
    valid_files = list(set(valid_files))

    delete_these = [v for v in candidates if v not in valid_files]            
    if keep is not None:
        if type(keep) is str:
            keep = (keep)
        delete_these = [v for v in delete_these if v not in keep]            

    delete_these = set(delete_these)
    delete_these = list(delete_these)

    # finally, to be ultra-safe, we will make sure all of the files to be deleted are in the temporary folder

    delete_these = [v for v in delete_these if v.startswith("/tmp/") or v.startswith("/var/tmp/") or v.startswith("/usr/tmp/")]
    
    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd)

    result = os.statvfs("/tmp/")
    result = result.f_frsize * result.f_bavail 
    if result > session_info["size"]:
        if session_stamp["temp_dir"] == "/var/tmp/":
            session_stamp["temp_dir"] = "/tmp/"
    session_info["size"] = result

    if session_info["size"] > 1.5 * session_info["latest_size"]:
            session_stamp["temp_dir"] = "/tmp/"


def clean_all():
    """
    Remove all temporary files created by nchack in the present session
    """

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nchack has either created or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = nc_created
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    other_files = []
    for ff in mylist:
        for cc in candidates:
            if cc in ff:
                other_files.append(ff)
      
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if session_stamp["stamp"] in f]

    for ff in mylist:
        other_files.append(ff)

    candidates = list(set(candidates + other_files))
    candidates = [x for x in candidates if os.path.exists(x)]
    candidates
    delete_these = set(candidates)
    delete_these = list(delete_these)

    # finally, to be ultra-safe, we will make sure all of the files to be deleted are in a temporary folder

    delete_these = [v for v in delete_these if v.startswith("/tmp/") or v.startswith("/var/tmp/") or v.startswith("/usr/tmp/")]

    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd)

            
    

def deep_clean():
    """
    Deep temp file cleaner
    Remove all temporary files ever created by nchack across all previous and current sesions
    """
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    ##mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if "nchack" in f]
    for ff in mylist:
        os.remove(ff)

def temp_check():
    """
    Function to do a deep clean of all temporary files ever created by nchack
    """
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if "nchack" in f]

    if len(mylist) > 0:
        if len(mylist) == 1:
            print(str(len(mylist)) +  " file was created by nchack in prior or current sessions. Consider running deep_clean!")
        else:
            print(str(len(mylist)) +  " files were created by nchack in prior or current sessions. Consider running deep_clean!")




def disk_clean(self, method = "year"):
    """
    Method to make sure /tmp is not clogged up after running an operation 
    """

    # get files as a list

    if type(self.current) is str:
        ff_list = [self.current]
    else:
        ff_list = self.current

    # First step is to figure out how much space is in /tmp
    # Do nothing if it is less than 0.5 GB

    if session_stamp["temp_dir"] == "/tmp/":
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail 

        if result > 0.5 * 1e9:
            return None

    # at this point we want to change the temp dir, though it probably has been already
    session_stamp["temp_dir"] = "/var/tmp/"
    # get a list of the new file names


    # loop through the existing ones
    for ff in ff_list:
    # check if the file is in /var/tmp
    # if it is, keep it that way
    # check the space remaining the /tmp
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail 
    # if there is less than 0.5 GB left, move the file to /var/tmp
        if result < 0.5 * 1e9:
            if ff.startswith("/tmp/"):
                new_ff =  ff.replace("/tmp/", "/var/tmp/")
                nc_created.append(new_ff)
                shutil.copyfile(ff, new_ff) 
                self.current = [new_ff if file == ff else file for file in ff_list]
        cleanup()

    if type(self.current) is str:
        self.current = self.current
    else:
        self.current = self.current[0]


    return None

            
