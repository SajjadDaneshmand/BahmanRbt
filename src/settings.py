import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(BASE_DIR, 'data.json')
FILES_FOLDER = os.path.join(BASE_DIR, 'files/')

delay = 60
SITE = 'Bahman'
INFO_FILE_NAME = 'info.conf'
BAHMAN_ID = 1
status_file_name = 'status.json'
INFO_FiLE_PATH = os.path.join(BASE_DIR, INFO_FILE_NAME)
URL = 'https://bsrv.bahman.ir/Part.aspx?company=bm&AspxAutoDetectCookieSupport=1'
persian_letters = ['ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش',
                   'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی']
