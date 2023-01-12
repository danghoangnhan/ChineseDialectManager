from rules.models import rules
class Dictionary:

    def __init__(self, ruleList: list[rules]):
        self.ipaList = None
        self.vowels = []
        self.consonants = []
        self.list = []
        self.map = dict()

        for rule in ruleList:
            self.map[rule.name] = self.uni2str(rule.unicode_repr)

    def  chaoshan2IPA(self, data) -> str:
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