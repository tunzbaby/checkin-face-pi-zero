open('/home/pi/build-checkFace-Desktop-Debug/log_data/notification.txt', 'w').close
from utils.config import *
with open(notification_file, 'w') as f:
    f.write(startup)
print('Warming up')
import time
from utils.register import register
from utils.facerec import facerec

while True:

    duc = open('log_data/switch.txt', 'r')
    if (duc.read() == '0'):
        facerec()
    else:
        register()
