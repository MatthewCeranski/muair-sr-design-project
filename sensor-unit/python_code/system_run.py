import subprocess
import time



subprocess.run('python tablestart.py', shell = True)

for i in range(1):

    subprocess.run('python record_run.py', shell=True)

    subprocess.run('python aqicalc.py', shell =True)

    subprocess.run('python aqicalcpm10.py', shell =True)

    subprocess.run('python mqtt_pullandsend.py', shell =True)
    #subprocess.run('python nano_run.py', shell=True)

    print("end")