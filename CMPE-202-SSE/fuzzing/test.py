import fuzzbang
import subprocess
import re
import datetime
import shutil
import time
from fuzzbang.alphanumericfuzzer import  AlphaNumericFuzzer
from fuzzbang.binaryfuzzer import  BinaryFuzzer

N = 10 # number of test cases

# bounds on length of strings
MIN_LEN = 0
MAX_LEN = 8

f1 = AlphaNumericFuzzer(MIN_LEN, MAX_LEN) # fuzzer object
f = BinaryFuzzer(MIN_LEN, MAX_LEN)


    # generate test cases
for i in range(N):
        time.sleep(2)
        with open("SCFFile.tlv","wb") as fp:
            for j in range(N):
                data = f.generate() # generate string
                fp.write(data)
                print("(" + str(len(data)) + ")") # print length of string
                print(data) # print string itself

        out=subprocess.run(["/home/psg/working/MS/MS/CMPE-202-SSE/fuzzing/scfprg"],stdout=subprocess.PIPE)
        print(out.stdout.decode('UTF-8'),end='\n')
        if re.search("Buffer Overflow",out.stdout.decode('UTF-8')):

            ts=time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            crash_summary_file_name="crash_summary"+str(st)+".txt"
            print("The sample caused buffer overflow.Crash summary in %s" %crash_summary_file_name )
            with open(crash_summary_file_name,"w") as fp1:
                fp1.write(out.stdout.decode('UTF-8'))
            shutil.move(crash_summary_file_name,"CRASH_INPUTS")
            target_name="CRASH_INPUTS\SCFFile"+str(st)+".tlv"
            shutil.move("SCFFile.tlv",target_name)







