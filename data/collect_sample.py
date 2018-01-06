import subprocess
import sys

def collect_sample_data(filename):
    screencap_cmd = "adb shell screencap -p /sdcard/"+filename
    print("running cmd: "+screencap_cmd)
    complete_process = subprocess.run(screencap_cmd, shell=True)
    print("screencap return:", complete_process.stdout)
    complete_process.check_returncode()
    pull_cmd = "adb pull /sdcard/"+filename+"  . "
    complete_process = subprocess.run(pull_cmd, shell=True)
    complete_process.check_returncode()
    print("pull cmd return:", complete_process.stdout)

if __name__ == '__main__':
    filename = sys.argv[1]
    collect_sample_data(filename)
    