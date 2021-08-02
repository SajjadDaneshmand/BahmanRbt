import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(BASE_DIR, 'data.json')
FILES_FOLDER = os.path.join(BASE_DIR, 'files/')

URL = 'https://bsrv.bahman.ir/Part.aspx?company=bm&AspxAutoDetectCookieSupport=1'
persian_ascii_letters = 'ا'
delay = 60
COMPANY = 'Bahman'
