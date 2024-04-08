from facial_recognition import FaceRecognition

fr = FaceRecognition() # instantiate facial recognition object
NEW_USER = "newUsername" # create new username

# take a photo of new user and store the username and face encodings.
#Eventually will add this info to db
fr.setup_2fa(NEW_USER)

# whenever a returning user logs in,
# verify_user will return a boolean value indicating 
# whether this is the correct person for that account
print("Verification passed: " + str(fr.verify_user(NEW_USER)))
