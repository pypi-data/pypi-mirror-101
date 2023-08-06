# low coverage hard filtering

def input_createMaskConsensus(wildcards):
    files = {}
    files['bam'] = os.path.join(DATAFOLDER["mapping"], wildcards.sample, wildcards.sample + ".sort.bam")
    if not CNS_GT_ADJUST:
        files['vcf'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.del_adjust.vcf.gz")
    else:
        files['vcf'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.gt_adjust.del_adjust.vcf.gz")
    return files

rule createMaskConsensus:
    input:
        unpack(input_createMaskConsensus)
    output:
        tmp_bed = temp(os.path.join(DATAFOLDER["masking"], "{sample}", "{sample}.lowcov.tmp")),
        final_bed = os.path.join(DATAFOLDER["masking"], "{sample}", "{sample}.lowcov.bed")
    params:
        cov = CNS_MIN_COV
    conda:
        "../envs/bedtools.yaml"
    singularity:
        "docker://rkibioinf/bedtools:2.29.2--0bfe8ac"
    log:
        os.path.join(DATAFOLDER["logs"], "masking", "{sample}.consensus_mask.log")
    shell:
        r"""
            bedtools genomecov -bga -ibam {input.bam} | awk '$4 < {params.cov}' | bedtools merge > {output.tmp_bed}
            bedtools intersect -v -a {output.tmp_bed} -b {input.vcf} > {output.final_bed}
        """

## var hard filtering
rule filterVarsConsensus:
    input:
        os.path.join(DATAFOLDER["variant_calling"], "{sample}", "{sample}.vcf")
    output:
        os.path.join(DATAFOLDER["variant_calling"], "{sample}", "{sample}.filtered.vcf.gz")
    params:
        mqm = VAR_FILTER_MQM,
        sap = "" if VAR_FILTER_SAP == -1 else  "| INFO/SAP > {sap}"
                                               "".format(sap=VAR_FILTER_SAP),
        qual = VAR_FILTER_QUAL
    conda:
        "../envs/bcftools.yaml"
    singularity:
        "docker://rkibioinf/bcftools:1.11--19c96f3"
    log:
        os.path.join(DATAFOLDER["logs"], "variant_calling", "{sample}.filtered.vcf.log")
    shell:
        r"""
			temp_out="{output}"
			temp_out="${{temp_out%%.vcf.gz}}.vcf"
			{{
				set -x
				bcftools filter -e \
					"INFO/MQM < {params.mqm} {params.sap} | QUAL < {params.qual}" \
					 -o "{output}" -O z "{input}"
			}} |& tee {log}
        """

## genotype adjustment
rule adjustGtConsensus:
    input:
        vcf = os.path.join(DATAFOLDER["variant_calling"], "{sample}", "{sample}.filtered.vcf.gz")
    output:
        vcf = os.path.join(DATAFOLDER["variant_calling"], "{sample}", "{sample}.filtered.gt_adjust.vcf.gz")
    params:
        frac = CNS_GT_ADJUST,
        vcf = os.path.join(DATAFOLDER["variant_calling"], "{sample}", "{sample}.filtered.gt_adjust.vcf")
    conda:
        "../envs/bcftools.yaml"
    script:
        "../scripts/adjust_gt.py"

## deletion adjustment
rule adjustDeletionConsensus:
    input:
        vcf = "{fname}.vcf.gz"
    output:
        vcf = "{fname}.del_adjust.vcf.gz"
    conda:
        "../envs/bcftools.yaml"
    script:
        "../scripts/adjust_dels.py"

## create ambig consensus
def input_createAmbiguousConsensus(wildcards):
    files = {}
    files['fasta'] = REFERENCE
    files['mask'] = os.path.join(DATAFOLDER["masking"], wildcards.sample, wildcards.sample + ".lowcov.bed")
    if not CNS_GT_ADJUST:
        files['vcf'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.del_adjust.vcf.gz")
        files['vcf_index'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.del_adjust.vcf.gz.tbi")
    else:
        files['vcf'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.gt_adjust.del_adjust.vcf.gz")
        files['vcf_index'] = os.path.join(DATAFOLDER["variant_calling"], wildcards.sample, wildcards.sample + ".filtered.gt_adjust.del_adjust.vcf.gz.tbi")
    return files

rule createAmbiguousConsensus:
    input:
        unpack(input_createAmbiguousConsensus)
    output:
        temp(os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.tmp"))
    log:
        os.path.join(DATAFOLDER["logs"], "consensus", "{sample}.iupac_consensus.tmp.log")
    conda:
        "../envs/bcftools.yaml"
    singularity:
        "docker://rkibioinf/bcftools:1.11--19c96f3"
    shell:
        r"""
            ( bcftools consensus \
                -I \
                -o {output} \
                -f {input.fasta} \
                -m {input.mask} \
                --sample {wildcards.sample} \
                {input.vcf} ) &> {log}
        """

## adapt consensus header
rule createHeaderConsensus:
    input:
        fasta = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.tmp"),
        version = os.path.join(PROJFOLDER, "pipeline.version")
    output:
        os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.fasta")
    singularity:
        "docker://rkibioinf/general:3.6.0--28150df"
    log:
        os.path.join(DATAFOLDER["logs"], "consensus", "{sample}.iupac_consensus.fasta.log")
    shell:
        r"""
            VERSION=$(cat {input.version})
            head -n 1 {input.fasta} | sed "s/.*/>{wildcards.sample}_iupac_consensus_$VERSION/" 1> {output} 2> {log}
            tail -n +2 {input.fasta} | tr -d "?\r\n" | fold -w 80 1>> {output} 2>> {log}
            # force new line at end of file to enable concatenation
            echo >> {output}
        """

## create masked consensus
rule createMaskedConsensus:
    input:
        fasta = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.tmp"),
        version = os.path.join(PROJFOLDER, "pipeline.version")
    output:
        os.path.join(MASKED_CNS_FOLDER, "{sample}.masked_consensus.fasta")
    log:
        os.path.join(DATAFOLDER["logs"], "consensus", "{sample}.masked_consensus.log")
    conda:
        "../envs/bcftools.yaml"
    singularity:
        "docker://rkibioinf/bcftools:1.11--19c96f3"
    shell:
        r"""
            VERSION=$(cat {input.version})
            echo ">{wildcards.sample}_masked_consensus_$VERSION" 1> {output} 2> {log}
            tail -n +2 {input.fasta} | tr "RYSWKMBDHVN" "N" | tr -d "?\r\n" | fold -w 80 1>> {output} 2>> {log}
            # force new line at end of file to enable concatenation
            echo >> {output}
        """
