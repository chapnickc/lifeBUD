"""
convert the log file for later analysis
"""


import time
import csv

try:
    f = open('logfile.log')
except IOError as e:
    print (e)
    
else:
    out_file = f.name 
    dot_ix = out_file.find('.')
    out_file = out_file[:dot_ix] + '.csv' 
    
    with open(out_file, 'w', newline = '') as out_f:

        writer = csv.writer(out_f)

        t_0, heart_rate = f.readline().strip().split(',')
        t_0 = time.strptime(t_0)
        t_0 = time.mktime(t_0)
       
        
        writer.writerow([0, heart_rate])

        
        for line in f:
            t, heart_rate = line.strip().split(',')
            t = time.strptime(t)
            t = time.mktime(t)

            elapsed_time = t - t_0
            writer.writerow([elapsed_time, heart_rate]) 


    f.close()
    out_f.close()





