rule clipPrimer:
    input:
        bam = os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.bam"),
        bed = PRIMER
    output:
        sortbam = temp(os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.tmp.bam")),
        sortindex = temp(os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.tmp.bam.bai")),
        tempbam = temp(os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.tmp.primerclipped.bam")),
        bam = os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.primerclipped.bam"),
        bamindex = temp(os.path.join(DATAFOLDER["mapping"], "{sample}", "{sample}.tmp.primerclipped.bam.bai"))
    log:
        os.path.join(DATAFOLDER["logs"], "trimming", "{sample}.primerclipping.log")
    params:
        dir = os.path.join(DATAFOLDER["mapping"], "{sample}")
    conda:
        "../envs/bamclipper.yaml"
    threads: 10
    shell:
        r"""
            samtools sort -@ {threads} -o {output.sortbam} {input.bam} &> {log};
            samtools index {output.sortbam} &>> {log};
            cd {params.dir}
            bamclipper.sh -b {output.sortbam} -p {input.bed} -n {threads} &>> {log};
            cp {output.tempbam} {output.bam} &>> {log};
        """