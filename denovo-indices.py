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

def supported(s):
    return re.match('^([ 0-9acgtACGT$]|\\^.)+$', s)

for line in fileinput.input(sys.argv[1]):
    fields = line.strip().split()
    if not supported(fields[2]) or not supported(fields[3]) or not supported(fields[4]):
        continue

    father = to_dict(fields[2].lower())
    mother = to_dict(fields[3].lower())
    child_bases = fields[4].lower()
    child = to_dict(child_bases)

    for x in 'acgt':
        # If there is nucluotide that exists in child but not in parents and number
        # of accurences of this nucleotide is greater than MIN_ALT_FREQ (i.e. 20%)
        # of total number of nucleotides from child reads that span actual position
        # than we print all indices (sixth column from read name - 0 based).
        if child[x] > sum(child.values()) * MIN_ALT_FREQ and not father[x] and not mother[x]:
            readname = fields[5].split(',')
            for i, b in enumerate(re.sub('\^.','',child_bases).replace('$','')):
                if b == x:
                    print(readname[i].split(':')[6])

