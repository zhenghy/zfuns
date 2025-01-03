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
    if not cl:
        cl = list(range(1, 23))
    d = {i: f"chr{i}" for i in cl}
    if 23 in cl:
        d[23] = "chrX"
    if 24 in cl:
        d[24] = "chrY"
    if 25 in cl:
        d[25] = "chrM"
    return d
