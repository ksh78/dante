import sys
import fileinput
import re

MIN_ALT_FREQ = float(sys.argv[2])

def to_dict(s):
    '''
    Convert nucleotide string to nucleotide dict with number of accurences.
    'aa^]cgta$g' -> {'a': 3, 'c': 1, 'g': 2, 't': 1}
    '''
    res = {'a':0,'c':0,'g':0,'t':0}
    for c in re.sub('\^.','',s).replace('$',''): # Remove ^ with following quality sign and remove $ sign.
        res[c] += 1
    return res

for line in fileinput.input(sys.argv[1]):
    fields = line.strip().split()
    father = to_dict(fields[2])
    mother = to_dict(fields[3])
    child = to_dict(fields[4])

    for x in 'acgt':
        # If there is nucluotide that exists in child but not in parents and number
        # of accurences of this nucleotide is greater than MIN_ALT_FREQ (i.e. 20%)
        # of total number of nucleotides from child reads that span actual position
        # than we print incoming input line. Otherwise not.
        if child[x] > sum(child.values()) * MIN_ALT_FREQ and not father[x] and not mother[x]:
            print(line, end='')
            break # We need only one of acgt nucleotides to meet criteria for line to be printed.
    



