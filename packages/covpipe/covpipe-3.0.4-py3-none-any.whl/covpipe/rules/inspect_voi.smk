# check, if variants of interest locate to low coverage regions

rule inspect_variants_of_interest:
    input:
        bed = os.path.join(DATAFOLDER["masking"], "{sample}", "{sample}.lowcov.bed"),
        voi = VAR_VOI
    output:
        vcf = os.path.join(DATAFOLDER["masking"], "{sample}", "{sample}.lowcov.voi.vcf")
    conda:
        "../envs/bedtools.yaml"
    singularity:
        "docker://rkibioinf/bedtools:2.29.2--0bfe8ac"
    log:
        os.path.join(DATAFOLDER["logs"], "masking", "{sample}.check_voi.log")
    shell:
        r"""
            grep '^#' {input.voi} >> {output.vcf}
            bedtools intersect -a {input.bed} -b {input.voi} -wb >> {output.vcf} 2> {log}
        """