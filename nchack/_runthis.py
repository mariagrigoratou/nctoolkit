import os
import copy
import multiprocessing
import math
import subprocess

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._session import session_stamp
from ._session import session_info


def split_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def run_cdo(command, target):
    command = command.strip()
    if command.startswith("cdo ") == False:
        raise ValueError("The command does not start with cdo!")

    out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    result,ignore = out.communicate()

    if "(Abort)" in str(result):
        raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))

    if str(result).startswith("b'Error") or "HDF error" in str(result):
       if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/") 
            command = command.replace(target, new_target)
            target = new_target
            nc_created.append(target)
            out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            result1,ignore = out.communicate()
            if str(result1).startswith("b'Error"):
                raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))
            session_stamp["temp_dir"] = "/var/tmp/"
            if "Warning:" in str(result1):
                print("CDO warning:" + str(result1))
    else:
        if "Warning:" in str(result):
            print("CDO warning:" + str(result))
            
    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target

def run_this(os_command, self, silent = False, output = "one", cores = 1, n_operations = 1, zip = False):

    if self.run == False:
        if len(self.hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")

    if self.run:

        if (output == "ensemble" and type(self.current) == list) or (output == "ensemble" and type(self.current) == str):
            new_history = self.hold_history

            if type(self.current) == str:
                file_list = [self.current]
                cores = 1
            else:
                file_list = self.current

            if len(self.hold_history) < len(self.history):
                os_command = os_command + " " + self.history[-1].replace("cdo ", " ")

            pool = multiprocessing.Pool(cores)
            target_list = []
            results = dict()

            self.history = new_history

            for ff in file_list:
    
                if silent:
                    ff_command = os_command.replace("cdo ", "cdo -s ")
                else:
                    ff_command = copy.deepcopy(os_command)
    
                target = temp_file("nc")
                nc_created.append(target)
                ff_command = ff_command + " " + ff + " " + target
    
                self.history.append(ff_command)
                temp = pool.apply_async(run_cdo,[ff_command, target])
                results[ff] = temp
    
            pool.close()
            pool.join()
            new_current = []
            for k,v in results.items():
                target_list.append(v.get())

            if type(self.current) == str:
                target_list = target_list[0]
    
            self.current = copy.deepcopy(target_list)

            
            return None


        if (output == "one" and type(self.current) == list):

            new_history = self.hold_history

            file_list = [self.current]

            if len(self.history) > len(self.hold_history):

                os_command = os_command + " " + self.history[-1].replace("cdo ", " ")

            target = temp_file("nc")
            os_command = os_command + str_flatten(self.current, " ") + " " + target
            target = run_cdo(os_command, target)
            self.current = target
            self.history = new_history
            self.history.append(os_command)




