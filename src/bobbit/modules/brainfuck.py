# brainfuck.py

''' brainfuck interpreter

https://en.wikipedia.org/wiki/Brainfuck#Language_design

- Does not support getting input from user (, command)
- Only do 10000 array/cells
- Cap number of cycles/instructions
'''

# Metadata

NAME    = 'brainfuck'
ENABLE  = True
PATTERN = r'^!bf\s+(?P<program>[^ ]+)$'
USAGE   = '''Usage: !bf [program]
    !bf ++>+++++[<+>-]++++++++[<++++++>-]<.
    7

    !bf ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
    Hello World!
'''

# Constants

ARRAY_MAX = 10000
CYCLE_MAX = ARRAY_MAX # Cap number of cycles to prevent DOS

# Functions

def evaluate_brainfuck(program):
    array    = [0]*ARRAY_MAX
    pc       = 0
    index    = 0
    cycle    = 0
    loops    = []
    response = ''

    while pc < len(program) and cycle < CYCLE_MAX:
        command = program[pc]
        pc_next = pc + 1

        if command == '>':
            index += 1
        elif command == '<':
            index -= 1
        elif command == '+':
            array[index] += 1
        elif command == '-':
            array[index] -= 1
        elif command == '.':
            response += chr(array[index])
        elif command == '[':
            if array[index]:
                loops.append(pc)
            else:
                brackets = 1
                pc_next  = pc + 1
                while pc_next < len(program) and brackets:
                    if program[pc_next] == '[':
                        brackets += 1
                    elif program[pc_next] == ']':
                        brackets -= 1
                    pc_next += 1
        elif command == ']':
            pc_next = loops.pop()
        else:
            response = f'Unknown command: {command}'
            break

        pc     = pc_next
        cycle += 1

    return response

# Command

async def brainfuck(bot, message, program=''):
    try:
        response = evaluate_brainfuck(program)
    except IndexError:
        response = 'Segmentation fault: invalid memory access'

    if response:
        return message.with_body(response)

# Register

def register(bot):
    return (
        ('command', PATTERN, brainfuck),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
