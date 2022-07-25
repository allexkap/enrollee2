class Handler:


    def __init__(self, parser, **scores):
        self.parser = parser
        self.scores = scores


    def compare(self, other):
        total = 0
        order = True
        equality = True

        for subject in other:
            total += self.scores[subject]
            total -= other[subject]
            if order and total < 0:
                order = False
            if equality and total != 0:
                equality = False
        if equality: print('=')
        return total > 0 or order and not equality


    def __call__(self, page):
        self.data = {'bvi': 0, 'ege': 0, 'sgl': 0}
        self.metadata = None

        for data, score in self.parser(page):
            if 'total' in data:
                self.metadata = data
            elif data['bvi']:
                self.data['bvi'] += 1
            elif not self.compare(score):
                if data['sgl']:
                    self.data['sgl'] += 1
                else:
                    self.data['ege'] += 1
