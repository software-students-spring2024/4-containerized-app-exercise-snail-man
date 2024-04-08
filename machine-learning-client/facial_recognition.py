import time
import face_recognition
import os, sys
import cv2
import numpy as np

def take_photo(username):
    """
    Helper method. Captures a photo using the default camera when the spacebar is pressed, then saves
    the photo with a filename based on the provided username. A rectangle with instructions
    is drawn at the bottom of the video feed to guide the user.

    Parameters:
    - username (str): The username to use in creating the filename for the saved photo.
                    The photo is saved as "{username}.png" within a directory named 'faces'.

    Note:
    - Relies on existence of faces directory. Otherwise will fail.
    - This method will continue to run indefinitely until a frame is successfully captured
    and saved when the spacebar is pressed, or if an error occurs in grabbing a frame from
    the camera.
    """
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Take photo")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break

        # Dimensions of the frame
        height, width = frame.shape[:2]

        # Coordinates and size of the rectangle
        rect_start_point = (0, height - 50)  # Starting point (bottom left)
        rect_end_point = (width, height)     # Ending point (bottom right)
        rect_color = (255, 255, 255)         # Rectangle color (white)
        rect_thickness = -1                  # Rectangle filled

        # Draw the rectangle
        cv2.rectangle(frame, rect_start_point, rect_end_point, rect_color, rect_thickness)

        # Text settings
        text = "Hit space to take photo"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 0, 0)  # Text color (black)
        line_type = 2
        text_size = cv2.getTextSize(text, font, font_scale, line_type)[0]
        text_x = (width - text_size[0]) // 2  # Center the text
        text_y = height - 25  # Position from the bottom

        # Put the text
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, line_type)

        # Show the frame
        cv2.imshow("Take photo", frame)

        k = cv2.waitKey(1)
        if k % 256 == 32:
            # SPACE pressed
            img_name = f"faces/{username}.png"
            cv2.imwrite(img_name, frame)
            break
    # Release handle to the webcam        
    cam.release()
    cv2.destroyAllWindows()

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_locations = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def setup_2fa(self, username):
        """
        Sets up two-factor authentication (2FA) for a user by capturing their photo, encoding
        their face, and storing this information for future authentication attempts.

        This method first captures a photo of the user by calling the `take_photo` method,
        using the provided username to save the photo with a corresponding filename.
        It relies on the face_encodings library to encode it.

        Parameters:
        - username (str): The username of the user setting up 2FA. This is used both for naming
                          the photo file and for associating the face encoding with the user.
        """
        take_photo(username)
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}") 
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding) 
            self.known_face_names.append(username)
        # once db is set up, replace the previous two lines with:
        # db.Images.insert_one({"username": username, "face_encoding": face_encoding})
    
    def verify_user(self, username):
        """
        Attempts to verify a user's identity using face recognition within a limited time window.

        This method opens the default camera and captures video frames for a short period
        (currently hardcoded to 3 seconds). 

        Parameters:
        - username (str): The username of the user attempting to verify their identity. 

        Returns:
        - bool: True if the user is successfully verified within the time window, False
                otherwise.
        """
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        t_end = time.time() + 3

        while time.time() < t_end: # open camera for three seconds
            ret, frame = video_capture.read()
            if not ret:
                sys.exit("Failed to capture frame.")

            # Process every other frame to make if faster
            if self.process_current_frame:
                if frame is not None and len(frame) > 0:
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Resize frame to 1/4 for faster processing
                else:
                    sys.exit("Frame is empty or not loaded correctly.")

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_frame = small_frame[:, :, ::-1]

                # Find faces from current video and get encoding
                self.face_locations = face_recognition.face_locations(rgb_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)

                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    # once db is set up, replace the following line of code with something of the sort:
                    # user  = db.Images.find_one({"username": username})
                    # known_face_encoding = user['face_encoding']
                    # matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    username = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    # Find smallest distance, which will be our best match
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        username = self.known_face_names[best_match_index]

            self.process_current_frame = not self.process_current_frame
            
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        
        if username == 'Unknown':
            return False
        
        return True
        # print(self.face_names)


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.verify_user()