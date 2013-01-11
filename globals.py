BORDER = 20
BUTTON_PADDING = 15
IMAGE_DIRECTORY = 'images/'
PREVIOUS_TIME = 0
SKIP_SECONDS = 3
SPEED_INCREMENT = 0.1
TITLE = 'Transcription Assistant'
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 800

BUTTON_IMAGES = ['button_play.png', 'button_rewind.png', 'button_stop.png', 'button_forward.png', '', '', '']
BUTTON_LABELS = ['Play', 'Rewind', 'Stop', 'Forward', 'Slower', 'Normal Speed', 'Faster']
BUTTON_TOOLTIPS = ['Play', 'Rewind ' + str(SKIP_SECONDS) + ' seconds', 'Stop', 'Forward ' + str(SKIP_SECONDS) + ' seconds', 'Slower ' + str(int(SPEED_INCREMENT * 100)) + '%', 'Normal Speed', 'Faster ' + str(int(SPEED_INCREMENT * 100)) + '%']
BUTTON_KEYS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7']

BUTTON_PLAY = 0
BUTTON_REWIND = 1
BUTTON_STOP = 2
BUTTON_FORWARD = 3
BUTTON_SLOWER = 4
BUTTON_NORMAL = 5
BUTTON_FASTER = 6