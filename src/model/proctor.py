

import numpy as np 
import cv2 
from PIL import Image 


FACE_CASCADE =cv2 .CascadeClassifier (cv2 .data .haarcascades +"haarcascade_frontalface_default.xml")


def check_face_in_image (uploaded_image ):



    pil_image =Image .open (uploaded_image ).convert ("RGB")
    image_array =np .array (pil_image )
    gray_image =cv2 .cvtColor (image_array ,cv2 .COLOR_RGB2GRAY )

    faces =FACE_CASCADE .detectMultiScale (gray_image ,scaleFactor =1.1 ,minNeighbors =5 ,minSize =(60 ,60 ))

    if len (faces )==0 :
        return "no_face","No face was detected in the frame. Please stay visible in the camera."
    elif len (faces )>1 :
        return "multiple_faces","More than one face was detected. Only the candidate should be visible."
    else :
        return "ok","Face verified."
