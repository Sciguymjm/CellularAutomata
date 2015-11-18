# Based on Matthew Taylor's MIT-Licensed automatatron (https://github.com/rhyolight/automatatron)
# modified by 7yl4r 09-2015
#

import math


def default_string_formatter(row, width=0):
    side_padding = int(math.floor((width - len(row) )/ 2)) * " "
    out = side_padding
    for v in row:
        if v:
            cell = "#"
        else:
            cell = " "
        out += cell
    out += side_padding
    return out


class EdgeType:  # (Enum)
    INF = 0
    LOOP = 1
    BOUNDED = 2  # TODO: implement this


class Engine(object):

    # I'm sure there's a clever programmatic way to generate these rules, but I'm
    # lazy.
    rules = [
        [True,  True,  True],
        [True,  True,  False],
        [True,  False, True],
        [True,  False, False],
        [False, True,  True],
        [False, True,  False],
        [False, False, True],
        [False, False, False],
    ]

    @classmethod
    def get_rule(cls, number):
        rules_to_apply = [bool(int(i)) for i in list('{0:08b}'.format(number))]
        rules = []
        for i, rule in enumerate(rules_to_apply):
            if rule:
                rules.append(cls.rules[i])
        return rules

    def __init__(self, rule_number, init_row=[False, True, False], edge_type=EdgeType.LOOP):
        self.rule_number = rule_number
        self.rule = self.get_rule(rule_number)
        self.rows = [init_row]
        self.edge_type = edge_type

    def __step_inf(self):
        next_row = []
        last_row = list(self.rows[-1])
        # Pad the row with two false values on each side. This allows us to more
        # easily match the expected state with the upward row (which is now padded).
        for i in xrange(2):
            last_row.insert(0, False)
            last_row.append(False)

        for index, value in enumerate(last_row):
            # skip first and last values (because of the padding)
            if index == 0 or index == len(last_row) - 1:
                continue
            # Upward state is the three cells above this one.
            upward_state = last_row[index - 1 : index + 2]
            match = upward_state in self.rule
            next_row.append(match)
        self.rows.append(next_row)
        return next_row

    def __step_loop(self):
        next_row = []
        last_row = list(self.rows[-1])

        if len(last_row) < 2:
            raise AssertionError("Bounded rows must be at least 3 cells wide")

        for index, value in enumerate(last_row):
            # skip first and last values (because of the padding)
            if index == 0:
                # wrap boundary
                upward_state = [last_row[-1], last_row[index], last_row[index+1]]
            elif index == len(last_row) - 1:
                # wrap boundary
                upward_state = [last_row[index-1], last_row[index], last_row[0]]
            else:
                # no wrap needed
                upward_state = last_row[index - 1 : index + 2]
            match = upward_state in self.rule
            next_row.append(match)
        self.rows.append(next_row)
        return next_row

    def __step_bound(self):
        next_row = []
        last_row = list(self.rows[-1])
        for index, value in enumerate(last_row):
            # skip first and last values (because of the padding)
            if index == 0:
                # end left side
                upward_state = [0, last_row[index], last_row[index+1]]
            elif index == len(last_row) - 1:
                # end right side
                upward_state = [last_row[index-1], last_row[index], 0]
            else:
                # no wrap needed
                upward_state = last_row[index - 1 : index + 2]
            match = upward_state in self.rule
            next_row.append(match)
        self.rows.append(next_row)
        return next_row


    def step(self):
        if self.edge_type == EdgeType.INF:
            self.__step_inf()
        elif self.edge_type == EdgeType.LOOP:
            self.__step_loop()
        elif self.edge_type == EdgeType.BOUNDED:
            self.__step_bound()
        else:
            raise AttributeError('unknown edge type:', self.edge_type)

    def retrieve(self, number):
        return self.rows[number]

    def run(self, handler=None, width=None, iterations=None):
        def run_one_iteration():
            row = self.step()
            if width is not None:
                # Pad the row till it reaches the specified width
                if width > len(row):
                    padding = int((width - len(row)) / 2)
                    for i in xrange(0, padding):
                        row.insert(0, False)
                        row.append(False)
                # Trim the row to the center rows
                half = int(math.floor(width/2))
                midpoint = int(math.floor(len(row)/2))
                row = row[midpoint - half : midpoint + half + 1]
            if handler is not None:
                handler(row, len(self.rows)-1)
    
        if iterations is None:
            while True:
                run_one_iteration()
        else:
            for i in xrange(iterations):
                run_one_iteration()

    def __str__(self, formatter=default_string_formatter):
        out = "Rule %i, %i iterations:" % (self.rule_number, len(self.rows) - 1)
        width = len(self.rows[-1])
        for row in self.rows:
            out = "%s\n%s" % (out, formatter(row, width))
        return out
