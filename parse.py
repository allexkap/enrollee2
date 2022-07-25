class Handler:


    def __init__(self, parser, uid):
        self.parser = parser
        self.uid = uid


    def compare(self, scores):
        total = 0
        order = True
        equality = True

        for this, other in zip(self.scores, scores):
            total += this - other
            if order and total < 0:
                order = False
            if equality and total != 0:
                equality = False
        if equality: print('=')
        return total > 0 or order and not equality


    def __call__(self, url):
        for data, scores in self.parser(self.uid, url):
            if 'total' in data:
                self.data = data
                self.scores = scores
                self.data['bvi'] = 0
                self.data['sgl'] = 0
                self.data['ege'] = 0
            elif data['bvi']:
                self.data['bvi'] += 1
            elif not self.compare(scores):
                if data['sgl']:
                    self.data['sgl'] += 1
                else:
                    self.data['ege'] += 1
        return self.data
