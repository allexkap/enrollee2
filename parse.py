class Handler:

    def __init__(self, scores):
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

        return total > 0 or order and not equality
