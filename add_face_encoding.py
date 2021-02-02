import timeit

start = timeit.default_timer()

import os
import glob
import face_recognition
import numpy as np
import os
import argparse
import tqdm
from annoy import AnnoyIndex


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default='/Users/duc/work_space/hyper/Annoy_face1/face_img/thang.jpg', help='add img path')
parser.add_argument('--name', type=str, default='new-guy', help='add img path')
args = parser.parse_args()
name = args.name


#generate annoy tree
NUMBER_OF_TREES = 100000
f = 128
t = AnnoyIndex(f, 'euclidean')

def listdirs(rootdir):
    rootdirs = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            listdirs(d)
            rootdirs.append(d)
    return rootdirs

def listfiles(rootdir):
    files = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)

        files.append(d)
    return files

def image_encoding(imagePath):
    filename = os.path.basename(imagePath)
    if ('.jpg' in filename) or ('.JPEG' in filename) or ('.jpeg' in filename) or ('.JPG' in filename):
        filename = filename.replace('.jpg', '')
        filename = filename.replace('.JPG', '')
        filename = filename.replace('.jpeg', '')
        filename = filename.replace('.JPEG', '')
        filename = filename.replace('.PNG', '')
        filename = filename.replace('.png', '')
        img = face_recognition.load_image_file(imagePath)
        img_ = face_recognition.face_locations(img)
        top, right, bottom, left = [ v for v in img_[0] ]
        face = img[top:bottom, left:right]
        img_emb = face_recognition.face_encodings(face)[0]
        if not os.path.exists('encode/' + name):
            os.mkdir('encode/{}'.format(name))
            with open('encode/{}/{}'.format(name, filename) + '.txt', 'w') as f:
                for item in img_emb:
                    f.write("%s\n" % item)
        else:
            path, dirs, files = next(os.walk('encode/' + filename))
            n = len(files)
            with open('encode/{}/{}({})'.format(name, filename, n) + '.txt', 'w') as f:
                for item in img_emb:
                    f.write("%s\n" % item)

        return img_emb
emb = image_encoding(args.path)

dirpaths = listdirs('encode')
print(os.path.basename(dirpaths[0]))

file1 = open("hyper_id1.txt", "w")
count = -1
for imagePaths in dirpaths:
    dirnames = os.path.basename(imagePaths)
    imagePaths = listfiles(imagePaths)
    for i, imagePath in tqdm.tqdm(enumerate(imagePaths)):
        if (".txt" in imagePath):
            filename11 = os.path.basename(imagePath)
            filename11 = filename11.replace(".txt","")
            # use directory name for person id
            file1.write(dirnames)
            file1.write("\n")
            with open(imagePath, 'r') as file_in:

                lines = []
                for line in file_in:
                    line = line.replace("\n","")
                    line = float(line)
                    lines.append(line)
                lines = np.array(lines)
                count += 1
            #add to tree
            t.add_item(count, lines)
t.build(NUMBER_OF_TREES,-1)

t.save(r'all_hyper1.ann')

stop = timeit.default_timer()
print('Encoding time: ' + str(stop - start))
