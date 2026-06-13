# distance.py

# Metadata

NAME    = 'distance'
ENABLE  = True
PATTERN = r'^!distance -s (?P<source>.*) -t (?P<target>.*)'
USAGE   = '''Usage: !distance -s <source_string> -t <target_string>
Computes the Levenshtein distance between the source and target strings. Ignores trailing whitespace.
'''

# Command

def levenshtein(source, target):

    if not source or not target:
        return 0

    matrix = [[0 for s in range(len(source) + 1)] for t in range(len(target) + 1)]

    for col_ind in range(1, len(source) + 1):
        matrix[0][col_ind] = col_ind
    for row_ind in range(1, len(target) + 1):
        matrix[row_ind][0] = row_ind

    for t in range(1, len(target) + 1):
        for s in range(1, len(source) + 1):

            if source[s - 1] == target[t - 1]:
                sub_cost = 0
            else:
                sub_cost = 1

            matrix[t][s] = min(matrix[t][s - 1] + 1,
                                matrix[t - 1][s] + 1,
                                matrix[t - 1][s - 1] + sub_cost)

    return matrix[-1][-1]

async def distance(bot, message, source, target):
    source, target = source.rstrip(), target.rstrip()
    response = f'Levenshtein distance: {levenshtein(source, target)}'

    return message.with_body(response)

# Register

def register(bot)
    return (
        ('command', PATTERN, distance)
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
