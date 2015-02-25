#!/usr/bin/python

import sys

import pprint

from pyparsing import nestedExpr


def depgen(parse, parent, memory):
    if not isinstance(parse[1], list):
        return [(parse[0], memory, parent)]
    else:
        def determine_parent_memory(x):
            if '-H' in x[0]:
                return [parent, memory]
            else:
                return [memory, object()] 
        return sum([depgen(x,*determine_parent_memory(x)) 
                    for x in parse[1:]],[])
    return []


def output(line):
    txt = line.strip()

    parse = nestedExpr('(',')').parseString(txt).asList()[0]
    
    #pprint.pprint(parse)

    depstruct = depgen(parse, None, object())
    
    #pprint.pprint(depstruct)

    parents = [x[2] for x in depstruct]
    ids = [None] + [x[1] for x in depstruct]

    deps = [ids.index(p) for p in parents]


    #assert deps[1::2]==deps[::2], deps
    #deps = [(d+1)/2 for d in deps[::2]]

    for i in range(0, len(deps)):
        if deps[i] > 0:        
            deps[i] = (deps[i]+1)/2
    print ' '.join(map(str,deps[::2]))


def main():
    in_path = sys.argv[1]
    
    fin = open(in_path, 'r')
    
    while True:
        s = fin.readline()
        if len(s) is 0:
            break
        if not s[0] is '(':
            t = ''
            s = s.split()
            if s:
                s = [t for t in s[3:]]
                print '0 ' * (len(s)/2)
        else:
            output(s)


if __name__ == '__main__':
	main()
