from facial_recognition import FaceRecognition

fr = FaceRecognition() # instantiate facial recognition object
newUser = "newUsername" # create new username

fr.setup_2fa(newUser) # take a photo of new user and store the username and face encodings. Eventually will add this info to db

print("Verification passed: " + str(fr.verify_user(newUser))) # whenever a returning user logs in, verify_user
# will return a boolean value indicating whether this is the correct person for that account
