""" example program to use the methods in facial_recognition"""

from facial_recognition import FaceRecognition

fr = FaceRecognition()  # instantiate facial recognition object
NEW_USER = "newUsername"  # create new username

# take a photo of new user and return face encodings.
face_encoding = fr.setup_2fa(NEW_USER)

# whenever a returning user logs in,
# verify_user will return a boolean value indicating
# whether this is the correct person for that account
print("Verification passed: " + str(fr.verify_user(face_encoding)))
