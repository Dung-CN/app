import os

WINDOWN_WIDTH = 700
WINDOWN_HEIGHT = 500
WINDOWN_POSION_RIGHT = 420
WINDOWN_POSION_DOWN = 110

USERS_FILE = "users.json"
PROFILE_FILE = "profile.json"
STUDY_RESULT = "study_result.json"
LEARNING_STATISTICS =  "learning_statistics.json"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AVATAR = os.path.join(BASE_DIR, "..", "Images", "nv.png")
DEFAULT_AVATAR = os.path.abspath(DEFAULT_AVATAR)

