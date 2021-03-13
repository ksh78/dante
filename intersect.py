import sys

if __name__ == "__main__":
    exomes = {}
    with open(sys.argv[1]) as fp:
        for line in fp:
            chr, begin, end = line.strip().split()
            if chr not in exomes:
                exomes[chr] = []
            exomes[chr].append((begin, end))

    with open(sys.argv[2]) as fp:
        for line in fp:
            chr, begin, end = line.strip().split()
            if chr in exomes:
                for segment in exomes[chr]:
                    if begin <= segment[1] and end >= segment[0]:
                        print(line, end='')
                        break
