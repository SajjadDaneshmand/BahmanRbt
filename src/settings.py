import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(BASE_DIR, 'data.json')

URL = 'https://bsrv.bahman.ir/Part.aspx?company=bm&AspxAutoDetectCookieSupport=1'
persian_ascii_letters = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
delay = 60
COMPANY = 'Bahman'

