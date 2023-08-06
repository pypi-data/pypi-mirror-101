singularity: "docker://rkibioinf/liftoff:1.5.1--78a2baa"

rule annotateAmbiguousConsensus:
    input:
        fasta = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.fasta"),
        annotation = CNS_ANNOT,
        ref = REFERENCE
    output:
        annotation_iupac = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.gff"),
        unmapped_features_iupac = os.path.join(IUPAC_CNS_FOLDER, "{sample}_unmapped_features_iupac_consensus.txt")
    log:
        os.path.join(DATAFOLDER["logs"], "annotate_ambiguous_consensus", "{sample}.log")
    conda:
        "../envs/liftoff.yaml"
    threads: 1
    shell:
        r"""
			intermediate="$(dirname {output.annotation_iupac})/{wildcards.sample}_liftoff_inter"
            mkdir -p "$intermediate"
			pushd "$intermediate"
			mkdir -p input
			ln -sfr "{input.annotation}" input/ref.gff
			ln -sfr "{input.ref}" input/ref.fasta
            liftoff -o {output.annotation_iupac} -dir "${{intermediate}}"\
                    -u {output.unmapped_features_iupac} -g input/ref.gff \
                    {input.fasta} input/ref.fasta  2> {log}
			popd
        """

rule annotateMaskedConsensus:
    input:
        fasta = os.path.join(MASKED_CNS_FOLDER, "{sample}.masked_consensus.fasta"),
        annotation = CNS_ANNOT,
        ref = REFERENCE
    output:
        annotation_masked = os.path.join(MASKED_CNS_FOLDER, "{sample}.masked_consensus.gff"),
        unmapped_features_masked = os.path.join(MASKED_CNS_FOLDER, "{sample}_unmapped_features_masked_consensus.txt")
    log:
        os.path.join(DATAFOLDER["logs"], "annotate_masked_consensus", "{sample}.log")
    conda:
        "../envs/liftoff.yaml"
    threads: 1
    shell:
        r"""
			intermediate="$(dirname {output.annotation_masked})/{wildcards.sample}_liftoff_inter"
            mkdir -p "$intermediate"
			pushd "$intermediate"
			mkdir -p input
			ln -sfr "{input.annotation}" input/ref.gff
			ln -sfr "{input.ref}" input/ref.fasta
            liftoff -o {output.annotation_masked} -dir "${{intermediate}}" \
                    -u {output.unmapped_features_masked} \
                    -g input/ref.gff \
                     {input.fasta} input/ref.fasta 2> {log}
			popd
        """
