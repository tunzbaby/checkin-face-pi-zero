import face_recognition
import cv2
from annoy import AnnoyIndex
import time
import numpy as np
import math
from imutils.video import FPS

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
fps = FPS().start()

#Load Annoy tree
f = 128
u = AnnoyIndex(f, 'euclidean')
u.load('all_hyper1.ann')

#Person list
def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words

known_face_names = readFile('hyper_id1.txt')

# Initialize some variables
face_locations = []
face_encodings = []
# face_names = []
process_this_frame = True

#Enhanchement frames
def Adjust_Gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Ham nay de kiem tra do mo (blur) cua frame
# input: image (numpy array)
# ouput: blur score (unsigned int)
def blur_count(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if cv2.Laplacian(gray, cv2.CV_64F) is None:
        return 0
    else:
        return cv2.Laplacian(gray, cv2.CV_64F).var()

def crop_face(frame, h1, h2, w1, w2):
    # print(h1, h2, w1, w2)
    if h2 - h1 < 400:
        hr = (400 - h2 + h1) / 2
        h1 = np.maximum(h1 - hr, 1)
        h2 = np.minimum(h2 + hr, frame.shape[0])
    if w2 - w1 < 300:
        wr = (300 - w2 + w1) / 2
        w1 = np.maximum(w1 - wr, 1)
        w2 = np.minimum(w2 + wr, frame.shape[1])

    # print(h1, h2, w1, w2)
    frame = frame[int(h1):int(h2), int(w1):int(w2)]
    # print("new_frame({}) = {}".format(frame.shape, frame))
    return frame

#Blur Checking
#Input: frame, face_locations = [(x1,y1,x2,y2)]
def blur_check(rgb_small_frame, face_locations):
    ident_face = crop_face(rgb_small_frame, face_locations[0][1], face_locations[0][3],
                           face_locations[0][0], face_locations[0][2])
    fm = blur_count(ident_face)
    if fm > 500:
        return True  # Good enough
    else:
        return  False  # Too Blurry


while True:
    print("Capturing image.")
    # time.sleep(1)
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # time.sleep(1)
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # print(face_locations)
        # Choose the face with largest area if there are more than 1
        # More than 1 face
        if (len(face_locations) > 0):
            dists = []
            # largest_face_location = []
            print("Number of Faces: {}".format(len(face_locations)))
            for i in range(len(face_locations)):
                p = face_locations[i]
                # dist = sqrt((p[2] - p[0]) ** 2 + (p[3] - p[1]) ** 2)
                dist = math.hypot(p[2] - p[0], p[3] - p[1])
                dists.append(dist)
            largest_face_id = np.argmax(dists)
            # largest_face_location.append(face_locations[np.argmax(areas)])
            # print(largest_face_location[0])
            # if blur_check(rgb_small_frame, [face_locations[largest_face_id]]):
            face_encodings = face_recognition.face_encodings(rgb_small_frame, [face_locations[largest_face_id]])
            # Just for displaying bbox
            face_locations = [face_locations[largest_face_id]]

    face_names = []
    diffs = []

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]
        # Lấy index của vector trong annoy
        matches_id, diff = u.get_nns_by_vector(face_encoding, 1, include_distances=True)
        matches_id = matches_id[0]
        diff = diff[0]
        # print("Merry Christmas! " + str(matches_id))

        # Lấy vector ra  từ index tương ứng đã lấy ở trên
        known_face_encoding = np.array(u.get_item_vector(matches_id))
        # print(known_face_encoding)
        # Create arrays of known face encodings and their names

        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=0.375)
        name = "Unknown"
        #
        # # If a match was found in known_face_encodings, just use the first one.
        if (True in matches) and (diff<0.375):
            # first_match_index = matches.index(True)
            name = known_face_names[matches_id]
            print(diff)

        print("Happy New Year,     {}!".format(name))
        diff = str(round(1-diff, 2))
        diffs.append(diff)
        face_names.append(name)
        # time.sleep(1.2)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name, diff in zip(face_locations, face_names, diffs):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.rectangle(frame, (left, top + 35), (right, top), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, diff, (left + 6, top + 28), font, 1.0, (255, 255, 255), 1)



    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
