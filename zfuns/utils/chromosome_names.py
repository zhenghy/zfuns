def chromosome_names(cl: list[int] | None = None) -> dict:
    """_summary_:
        Returns a dictionary mapping chromosome numbers to chromosome names.

    Args:
        cl (list[int] | None, optional):
            chromosome id list.\n
            Defaults to None for all chromosomes.

    Returns:
        dict:
            {1: "chr1", 2: "chr2", ..., 23: "chrX", 24: "chrY", 25: "chrM"}
    """
    # todo: get other chromosomes info from the internet
    chromosomes_info = """
        chr1	249250621
        chr2	243199373
        chr3	198022430
        chr4	191154276
        chr5	180915260
        chr6	171115067
        chr7	159138663
        chr8	146364022
        chr9	141213431
        chr10	135534747
        chr11	135006516
        chr12	133851895
        chr13	115169878
        chr14	107349540
        chr15	102531392
        chr16	90354753
        chr17	81195210
        chr18	78077248
        chr20	63025520
        chr19	59128983
        chr22	51304566
        chr21	48129895
        chrX	155270560
        chrY	59373566
        chrM	16571"""
    chromosomes_dict = {
        i + 1: tuple(n.strip().split())
        for i, n in enumerate(chromosomes_info.strip().splitlines())
    }

    if not cl:
        return chromosomes_dict
    else:
        return {i: chromosomes_dict[i] for i in cl}


if __name__ == "__main__":
    print(chromosome_names(list(range(1, 25))))
