#!/usr/bin/python2 -u
from sys import argv
from time import time
from datetime import timedelta
from logic.cube2x2x2 import Cube2x2x2
from logic.cube3x3x3 import Cube3x3x3


def reset_console():
    print '\033[H\033[2J'


def print_ihelp():
    reset_console()
    print '''Cube is represented as:
          U
        L F R B
          D
Here are allowed commands:
U - Rotate (U)p layer clockwise.
U'- Rotate (U)p layer counterclockwise
D - Rotate (D)own layer clockwise.
D'- Rotate (D)own layer counterclockwise
L - Rotate (L)eft layer clockwise.
L'- Rotate (L)eft layer counterclockwise
R - Rotate (R)ight layer clockwise.
R'- Rotate (R)ight layer counterclockwise
F - Rotate (F)ront layer clockwise.
F'- Rotate (F)ront layer counterclockwise
B - Rotate (B)ack layer clockwise.
B'- Rotate (B)ack layer counterclockwise

> command_1 [command_2 ... command_n] <ENTER>
'''
    raw_input('Press ENTER to return to cube view.')


def game(cube, max_time_sec, flag):
    commands = {"U": cube.up_clockwise,     "U'": cube.up_counterclockwise,
                "D": cube.bottom_clockwise, "D'": cube.bottom_counterclockwise,
                "L": cube.left_clockwise,   "L'": cube.left_counterclockwise,
                "R": cube.right_clockwise,  "R'": cube.right_counterclockwise,
                "F": cube.front_clockwise,  "F'": cube.front_counterclockwise,
                "B": cube.back_clockwise,   "B'": cube.back_counterclockwise,
                "help": print_ihelp}
    solved_goal = 10
    solved_cnt = 0
    
    start_time_sec = int(time())
     
    cube.shuffle()
    while True:
        if cube.is_completed():
            solved_cnt += 1
            if solved_cnt is not solved_goal:
                cube.shuffle()
        
        reset_console()
        print 'Solved: {}/{}'.format(solved_cnt, solved_goal)
        print cube

        if solved_cnt is solved_goal:
            duration = int(time()) - start_time_sec
            if duration <= max_time_sec:
                print flag
            else:
                print 'It took you too much time: {}s. At most: {}s'.format(duration, max_time_sec)
            return

        cmd_list = raw_input('[{}]> '.format('/'.join(sorted(commands)))).split()
        for cmd in cmd_list:
            if cmd in commands:
                commands[cmd]()


if __name__ == '__main__':
    try:
        if len(argv) != 2:
            print "usage: ./game.py <2x2x2|3x3x3>"
            exit(0)
        if argv[1] == '2x2x2':
            game(Cube2x2x2(), 30, r'flag{flagflag}')
        elif argv[1] == '3x3x3':
            game(Cube3x3x3(), 30, r'flag{flagflagflag}')
        else:
            print 'Unknown game type: ' + argv[1]
    except:
        print 'bye!'
    exit(0)
