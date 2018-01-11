import subprocess
import sys
import random


def capturescreen_and_pull(filename, target_dir='./data/'):
    screencap_cmd = "adb shell screencap -p /sdcard/"+filename
    print("running cmd: "+screencap_cmd)
    complete_process = subprocess.run(screencap_cmd, shell=True)
    print("screencap return:", complete_process.stdout)
    complete_process.check_returncode()
    pull_cmd = "adb pull /sdcard/"+filename+" "+target_dir+filename
    complete_process = subprocess.run(pull_cmd, shell=True)
    complete_process.check_returncode()
    print("pull cmd return:", complete_process.stdout)
    return True


def simulate_swipe_ms(ms):
    startx = random.randint(100,200)
    starty = random.randint(300,400)
    endx = random.randint(200,300)
    endy = random.randint(400,500)
    swipe_cmd = "adb shell input touchscreen swipe "+str(startx)+" "+str(starty)+" "+str(endx)+" "+str(endy)+" "+str(ms)
    complete_process = subprocess.run(swipe_cmd, shell=True)
    complete_process.check_returncode()
    return True


if __name__ == '__main__':
    filename = sys.argv[1]
    capturescreen_and_pull(filename)
    simulate_swipe_ms(1000)

    