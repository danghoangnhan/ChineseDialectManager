class Dictionary:

    def __init__(self, ruleList):
        self.ipaList = None
        self.vowels = []
        self.consonants = []
        self.list = []
        self.map = dict()

        for rule in ruleList:
            self.map[str(rule.name)] = self.uni2str(rule.unicode_repr)

    def chaoshan2IPA(self, data) -> str:
        start: int = 0
        finish: int = len(data)
        result = ''
        data = data.lower()
        while start <= finish:
            sample = data[start:finish]
            token = self.map.get(sample)
            if token is not None:
                result += token
                start = finish
                finish = len(data)
            else:
                finish -= 1
        return result

    def word2IPA(self, data) -> str:
        data = data.lower()
        max_tokens = len(data)
        result = [None] * max_tokens
        length = len(data)
        start = length - 1
        finish = length
        index = 0

        while start >= 0:
            while start >= 0:
                sample = data[start:finish]
                token = self.map.get(sample)
                if token is not None:
                    result[index] = token
                    index += 1
                    finish = start
                    start -= 1
                else:
                    start -= 1
            finish = start + 1
            start = finish - 1

        return ''.join(result[:index][::-1])

    def uni2str(self, data) -> str:
        result = ''
        while data.__contains__('\\u'):
            index = data[2:6]
            index = chr(int(index, 16))
            result += index
            data = data[6:]
        return result
