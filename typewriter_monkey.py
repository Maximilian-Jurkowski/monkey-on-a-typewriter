#!/usr/bin/env python3

import random,string,argparse,concurrent.futures,multiprocessing,os

def monkey_typer(args,found_cat,charset,match_length,charset_length,p,t):
    monkey_word = str()
    attempts = 0
    while monkey_word != args.match and not found_cat.value:
        monkey_word = str()
        for _ in range(0,match_length):
            monkey_word += charset[random.randint(0,charset_length)]
        if monkey_word == args.match:
            found_cat.value = 1
        attempts+=1
    return attempts

def mProc(args,found_cat,charset,match_length,charset_length):
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.processes) as pexec:
        return [ pexec.submit(mThread,args,found_cat,charset,match_length,charset_length,p).result() for p in range(args.processes) ]

def mThread(args,found_cat,charset,match_length,charset_length,p):
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as texec:
        return [ texec.submit(monkey_typer,args,found_cat,charset,match_length,charset_length,p,t).result() for t in range(args.threads) ]

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
    manager = multiprocessing.Manager()

    found_cat = manager.Value(int,0)
    monkey_results = mProc(args,found_cat,charset,match_length,charset_length)

    total_attempts = 0
    for p in monkey_results:
        total_attempts += sum(p)
    print(f"Matched {args.match} in {total_attempts} tries.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="You can't expect to recreate a work of Shakespeare because some philosopher threw a monkeys at a room full of typewriters...",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m','--match',type=str,default='cat',help='Word or phrase to match.')
    parser.add_argument('-c','--charset',choices=['print','lower','upper'],default='print',help="""Character set.
 print: Monkey has full access to keyboard.
 lower: Monkey only uses a-z + space
 upper: Monkey is using capslock, A-Z + space.
    """)
    parser.add_argument('-T','--threads',type=int,default=4,help='Set number of threads. (Default 4)')
    parser.add_argument('-P','--processes',type=int,default=os.cpu_count(),help=f'Set number of processes. (Default {os.cpu_count()})')
                                                
    args = parser.parse_args()
    main(args)
