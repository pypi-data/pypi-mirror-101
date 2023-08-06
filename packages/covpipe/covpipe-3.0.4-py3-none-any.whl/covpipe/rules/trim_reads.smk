singularity: "docker://rkibioinf/fastp:0.20.1--f3e7ab3"

def input_trimReads(wildcards):
    if ADAPTERS:
        return [os.path.join(DATAFOLDER["trimmed"], wildcards.sample, wildcards.sample + ".R1.ac.fastq.gz"), os.path.join(DATAFOLDER["trimmed"], wildcards.sample, wildcards.sample + ".R2.ac.fastq.gz")]
    else:
        return list(getFastq(wildcards))

rule trimReads:
    input:
        getFastq
    output:
        PE1 = temp(os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.R1.fastq.gz")),
        PE2 = temp(os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.R2.fastq.gz")),
        SE1 = temp(os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.SE.R1.fastq.gz")),
        SE2 = temp(os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.SE.R2.fastq.gz")),
        json = os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.fastp.json"),
        html = os.path.join(DATAFOLDER["trimmed"], "{sample}", "{sample}.fastp.html")
    log:
        os.path.join(DATAFOLDER["logs"], "trimming", "{sample}.log")
    params:
        adapters = "--adapter_fasta " + ADAPTERS if ADAPTERS else "",
        reqlen = ("--length_required {}".format(READ_FILTER_LEN) 
                  if READ_FILTER_LEN != -1
                  else ""),
        qualfilter = "--qualified_quality_phred {}".format(READ_FILTER_QUAL) 
    conda:
        "../envs/fastp.yaml"
    threads:
        1
    shell:
        r"""
            ( fastp \
                --in1 {input[0]} \
                --out1 {output.PE1} \
                --in2 {input[1]} \
                --out2 {output.PE2} \
                --unpaired1 {output.SE1} \
                --unpaired2 {output.SE2} \
                --json {output.json} \
                --html {output.html} \
                {params.adapters} \
                {params.qualfilter} \
                {params.reqlen} \
                --low_complexity_filter \
                --overrepresentation_analysis \
                --thread {threads} ) &> {log}
        """
