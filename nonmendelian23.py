import sys

def acceptable(genotype):
    return genotype in ('A', 'C', 'G', 'T', 'AA', 'AC', 'AG', 'AT', 'CC', 'CG', 'CT', 'GG', 'GT', 'TT')


def denovo(chrom, father, mother, child):
    if not acceptable(father) or not acceptable(mother) or not acceptable(child):
        return False
    if len(child) == 2:
        for father_allele in father:
            for mother_allele in mother:
                if child == ''.join(sorted([father_allele, mother_allele])):
                    return False
    else:
        if chrom == 'Y':
            for father_allele in father:
                if child == father_allele:
                    return False
        else:
            for mother_allele in mother:
                if child == mother_allele:
                    return False
    return True


def genotypes(file):
    genotypes = {}
    with open(file) as fp:
        for line in fp:
            if not line.startswith('#'):
                rs, chrom, pos, genotype = line.strip().split()
                if acceptable(genotype):
                    genotypes[(rs, chrom, pos)] = genotype
    return genotypes


if __name__ == "__main__":
    father_genotypes = genotypes(sys.argv[1])
    mother_genotypes = genotypes(sys.argv[2])
    with open(sys.argv[3]) as fp:
        print('rsid', 'chromosome', 'position', 'father', 'mother', 'child')
        for line in fp:
            if not line.startswith('#'):
                rs, chrom, pos, child_genotype = line.strip().split()
                key = (rs, chrom, pos)
                if key in father_genotypes and key in mother_genotypes:
                    father_genotype = father_genotypes[key]
                    mother_genotype = mother_genotypes[key]
                    if acceptable(child_genotype) and denovo(chrom, father_genotype, mother_genotype, child_genotype):
                        print(rs, chrom, pos, father_genotypes[key], mother_genotypes[key], child_genotype, sep='\t')
