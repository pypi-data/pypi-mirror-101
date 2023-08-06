import os

def test_0():
    for (dirpath, dirnames, filenames) in os.walk('./openitcr'):
        for f in filenames:
            if f.endswith('.py'):
                exit_code  = os.system( f'python3 ./{dirpath}/{f} t' )
                print(('\u2705' if exit_code == 0 else '\u274c' )\
                    + f' {dirpath}/{f}' )
    pass