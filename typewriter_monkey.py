#!/usr/bin/env python3

import random,string,argparse

def main(args):
    charset=str()
    if args.charset == 'print':
        charset = string.printable
    elif args.charset == 'lower':
        charset = string.ascii_lowercase + ' '
    elif args.charset == 'upper':
        charset = string.ascii_uppercase + ' '

    match_length = len(args.match)
    charset_length = len(charset) - 1

    monkey_word = str()
    attempts = 0
    while monkey_word != args.match:
        monkey_word = str()
        for _ in range(0,match_length):
            monkey_word += charset[random.randint(0,charset_length)]
        attempts+=1
    print(f"Matched {monkey_word} in {attempts} tries.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="You can't expect to recreate a work of Shakespeare because some philosopher threw a monkeys at a room full of typewriters...",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m','--match',type=str,default='cat',help='Word or phrase to match.')
    parser.add_argument('-c','--charset',choices=['print','lower','upper'],default='print',help="""Character set.
 print: Monkey has full access to keyboard.
 lower: Monkey only uses a-z + space
 upper: Monkey is using capslock, A-Z + space.
    """)
    args = parser.parse_args()
    main(args)
