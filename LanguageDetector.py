import lizard
from lizard_languages import languages, get_reader_for, CLikeReader

def detect(filename):
    for lan in languages():
        if lan.match_filename(filename):
            return lan.language_names[0]