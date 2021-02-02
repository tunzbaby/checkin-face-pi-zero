import time
import picamera
import os
import face_recognition
import argparse

parser = argparse.ArgumentParser()
#parser.add_argument('--path', type=str, default='foo1.jpg', help='add img path')
parser.add_argument('--name', type=str, default='new-guy', help='id number')
args = parser.parse_args()
name = args.name

def listdirs(rootdir):
    rootdirs = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            listdirs(d)
            rootdirs.append(d)
    return rootdirs

def image_encoding(imagePath):
    filename = os.path.basename(imagePath)
    if ('.jpg' in filename) or ('.jpeg' in filename):
        filename = filename.replace('.jpg', '')
        filename = filename.replace('.jpeg', '')
        img = face_recognition.load_image_file(imagePath)
        img_ = face_recognition.face_locations(img)
        if (len(img_) > 0):
            top, right, bottom, left = [ v for v in img_[0] ]
            face = img[top:bottom, left:right]
            img_emb = face_recognition.face_encodings(face)[0]
            if not os.path.exists('encode/' + name):
                new_id = len(listdirs('encode')) + 1
                os.mkdir('encode/{}'.format(new_id))
                with open('encode/{}/{}'.format(new_id, filename) + '.txt', 'w') as f:
                    for item in img_emb:
                        f.write("%s\n" % item)
                print('Create ID: {} done'.format(new_id))
            else:
                _, _, files = next(os.walk('encode/' + name))
                n = len(files)
                with open('encode/{}/{}({})'.format(name, filename, n) + '.txt', 'w') as f:
                    for item in img_emb:
                        f.write("%s\n" % item)
                print('Added 1 image to id: {}'.format(name))
        else:
            print("There is no face")
            
# camera = picamera.PiCamera()
# camera.close()
with picamera.PiCamera() as camera:
    camera.resolution = (512, 512)
    camera.start_preview(fullscreen=False,window=(37,205,450,330))
    #camera.exposure_compensation = 2
    camera.brightness = 55
    camera.exposure_mode = 'sports'
    camera.meter_mode = 'matrix'
    camera.image_effect = 'saturation'
    # Give the camera some time to adjust to conditions
    time.sleep(6)
    camera.capture('images/foo1.jpg')
    camera.stop_preview()
    camera.close()
    image_encoding('images/foo1.jpg')
