from ipapy import UNICODE_TO_IPA
from ipapy.ipachar import IPAVowel, IPAConsonant
from ipapy.ipastring import IPAString


class Dictionary:
    def __init__(self):
        self.vowels = {

            "a՜": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0251\u02D0"),
            "a‘": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0251\u02D0"),
            "a'": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0251\u02D0"),
            "a": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0251\u02D0"),
            "ɑ": UNICODE_TO_IPA[u"\u0258"],
            "e": UNICODE_TO_IPA[u"\u0065"],
            "i": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0069\u02D0"),
            "o": UNICODE_TO_IPA[u"\u006F"],
            "o՜": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0254\u02D0"),
            "o‘": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0254\u02D0"),
            "o'": IPAVowel(name="my_a_1", descriptors=u"open front unrounded",
                           unicode_repr=u"\u0254\u02D0"),
            "ó": IPAVowel(name="my_a_1", descriptors=u"open front unrounded",
                           unicode_repr=u"\u0254\u02D0"),


            "u": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u0075\u02D0"),
            "W": UNICODE_TO_IPA[u"\u0077"],
            "ai": IPAVowel(name="ai", descriptors=u"open front unrounded", unicode_repr=u"\u0061\u026A"),
            "ao": IPAVowel(name="ao", descriptors=u"open front unrounded", unicode_repr=u"\u0061\u028A"),
            "iu": IPAVowel(name="iu", descriptors=u"open front unrounded", unicode_repr=u"\u006A\u0075\u02D0"),
            "oi": IPAVowel(name="oi", descriptors=u"open front unrounded", unicode_repr=u"\u006F\u026A"),
            "Y": IPAVowel(name="Y",
                          descriptors=u"open front unrounded",
                          unicode_repr=u"\u0069"),
            "‘": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u02B0"),
            "'": IPAVowel(name="my_a_1", descriptors=u"open front unrounded", unicode_repr=u"\u02B0"),
        }
        self.consonants = {
            "ch": UNICODE_TO_IPA[u"\u0074\u0073"],
            "s": UNICODE_TO_IPA[u"\u0073"],
            "l": UNICODE_TO_IPA[u"\u006C"],
            "n": UNICODE_TO_IPA[u"\u006E"],
            "ng": UNICODE_TO_IPA[u"\u014B"],
            "b": UNICODE_TO_IPA[u"\u0062"],
            "g": UNICODE_TO_IPA[u"\u0067"],
            "ch": UNICODE_TO_IPA[u"\u0074\u0073"],
            "ch'": IPAConsonant(name='ch\'', descriptors=u"voiced bilabial non-sibilant-fricative",
                                unicode_repr=u"\u0074\u0073\u02B0"),
            "s": IPAConsonant(name='s', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u0073"),
            "l": IPAConsonant(name='l', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u006C"),
            "n": IPAConsonant(name='n', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u006E"),
            "k'": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                               unicode_repr=u"\u006B\u02B0"),
            "k": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u006B"),
            "p'": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                               unicode_repr=u"\u0070\u02B0"),
            "p": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u0070"),
            "t": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                              unicode_repr=u"\u0074"),
            "t'": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                               unicode_repr=u"\u0074\u02B0"),
            "ng": IPAConsonant(name='aa', descriptors=u"voiced bilabial non-sibilant-fricative",
                               unicode_repr=u"\u014B"),

        }
        self.ipaList = self.vowels.copy()
        self.ipaList.update(self.consonants)

    def chaoshan2IPA(self, data) -> IPAString:
        start: int = 0
        finish: int = len(data)
        result = []
        data = data.lower()
        lenght_size = len(data) * len(self.ipaList)
        while start <= finish:
            sample = data[start:finish]
            token = self.ipaList.get(sample)
            if token is not None:
                result.append(token)
                start = finish
                finish = len(data)
            else:
                finish -= 1
        return IPAString(ipa_chars=result)


dict = Dictionary()
print(dict.chaoshan2IPA("Chai"))
