import subprocess
import time
command = "python3 haptic.py 60 5"
while True:

    ps = subprocess.Popen(command, shell = True)
    print(ps)
    print(ps.pid)
    tic = time.time()

    time.sleep(5)
    toc = time.time()
    print(toc - tic)
    ps.kill()
