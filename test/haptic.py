import RPi.GPIO as GPIO
import time as time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("beat", help= "int number of beats", type = int)
parser.add_argument("time_sleep", help = "int timesleep", default = 5, type = int)
args = parser.parse_args()

print("args received", args.beat)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

bpm = args.beat
sleep_time = args.time_sleep

pwm = GPIO.PWM(18,bpm/60) #GPIO18
print(bpm / 60)
pwm.start(50)

time.sleep(sleep_time)
GPIO.cleanup()


