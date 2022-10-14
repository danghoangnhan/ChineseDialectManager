from ipapy import UNICODE_TO_IPA
from ipapy.ipachar import IPAVowel


class Dictionary:
    def __init__(self):
        self.vowels = {
            "a՜":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0251\u02D0"),
            "ɑ":    UNICODE_TO_IPA[u"\u0258"],
            "e":    UNICODE_TO_IPA[u"\u0065"],
            "i":    IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0069\u02D0"),
            "o":    UNICODE_TO_IPA[u"\u006F"],
            "o՜":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0254\u02D0"),
            "u":    IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0075\u02D0"),
            "W":    UNICODE_TO_IPA[u"\u0077"],
            "ai":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0061\u026A"),
            "ao":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0061\u028A"),
            "iu":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u006A\u0075\u02D0"),
            "oi":   IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u006F\u026A"),
            "Y": UNICODE_TO_IPA[u"\u0069"]
        }
        self.consonants = {
            "ch": UNICODE_TO_IPA[u"\u0074\u0073"],
            "s": UNICODE_TO_IPA[u"\u0073"],
            "l": UNICODE_TO_IPA[u"\u006C"],
            "n": UNICODE_TO_IPA[u"\u006E"],
            "ng": UNICODE_TO_IPA[u"\u014B"]
        }


dict = Dictionary()
print(dict)