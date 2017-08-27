import subprocess
size = 20
command = "python Ginnungagap2.py"
for i in range(size):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print("done " + str(i))
print("finished")