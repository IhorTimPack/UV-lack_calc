import sys
import re

def repl(x):
    replace = x[0][1] + x[0][0]
    for i in x[0][2:]:
        replace += i
    return replace

for line in sys.stdin:
    line = line.rstrip()
    line_list = line.split()
    print(line_list)
    pattern = r"\b\w{2,}\b"
    # h = re.search(pattern, line)
    h = re.findall(pattern, line)
    line = re.sub(pattern, repl(h), line)
    print(line)
    # repl = r"argh"
    # f = re.sub(pattern, repl, line, )
    # print(f)