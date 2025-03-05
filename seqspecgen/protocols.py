import enum


class ProtocolsIO(enum.StrEnum):
    splitseq_100k_v2 = "https://www.protocols.io/view/evercode-wt-v2-2-1-eq2lyj9relx9/v1"
    splitseq_1M_v2 = "https://www.protocols.io/view/evercode-wt-mega-v2-2-1-8epv5xxrng1b/v1"
    ont_library_prep = "https://www.protocols.io/view/ont-library-prep-for-split-seq-cdna-eq2lyj1xmlx9/v1"
    splitseq_single_index = "https://www.protocols.io/view/evercode-single-index-pcr-5jyl82k9rl2w/v1"
    splitseq_dual_index = "https://www.protocols.io/view/evercode-dual-index-pcr-yxmvmeqe5g3p/v1"
    share_seq = "https://www.protocols.io/view/share-seq-protocol-v2-2-adapted-for-mortazavi-lab-difw4bpe"
    
    cdna_exome_capture = "https://www.protocols.io/view/cdna-exome-capture-v1-0-1-36wgq3b83lk5/v1"
    
    pbmc_cell_prep = "https://www.protocols.io/view/protocol-to-isolate-cryopreserve-and-fix-mouse-pbm-5qpvo3kx7v4o/v2"

    cortex_hipp_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-eq2lyj17rlx9/v1"
    left_cortex_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-cryopreser-4r3l22y2pl1y/v1"
    hypo_pit_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-n92ldm8b8l5b/v2"
    gastroc_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-n2bvj3noplk5/v2"
    heart_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-dm6gp3zedvzp/v2"
    liver_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-kxygx396zg8j/v2"
    kidney_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-14egn334ml5d/v2"
    adrenal_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-81wgbxzdylpk/v2"
    male_gonads_nuclei_prep ="https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-5qpvo3837v4o/v1"
    female_gonads_nuclei_prep = "https://www.protocols.io/view/protocol-to-isolate-and-fix-nuclei-from-flash-froz-36wgq3e3ylk5/v1"


single_cell_protocols = set([ProtocolsIO.pbmc_cell_prep])


single_nucleus_protocols = set([
    ProtocolsIO.cortex_hipp_nuclei_prep,
    ProtocolsIO.left_cortex_nuclei_prep,
    ProtocolsIO.hypo_pit_nuclei_prep,
    ProtocolsIO.gastroc_nuclei_prep,
    ProtocolsIO.heart_nuclei_prep,
    ProtocolsIO.liver_nuclei_prep,
    ProtocolsIO.kidney_nuclei_prep,
    ProtocolsIO.adrenal_nuclei_prep,
    ProtocolsIO.male_gonads_nuclei_prep,
    ProtocolsIO.female_gonads_nuclei_prep,
])


def filter_protocols_for_lookups(protocols):
    """Filter protocols from portal to ones used in table lookups

    There may be protocols not relevant for construction seqspecs
    so ignore them.
    """
    # Python 3.12 enums supports in directly
    protocols = [ProtocolsIO(p) for p in protocols if p in ProtocolsIO.__members__.values()]

    if len(protocols) == 0:
        raise ValueError(f"Unable to find information by {protocols}")

    return protocols


def get_template_from_protocols(protocols):
    # the only thing different between the 100k and 1M is the 1M has more round 1 barcodes
    # which is handled by get_barcodes_from_protocols
    # parse v2 mega 96 well
    if ProtocolsIO.splitseq_1M_v2 in protocols:
        if ProtocolsIO.splitseq_single_index in protocols:
            return "parse-wt-mega-v2-single-index-libspec-3.yaml.j2"
        elif ProtocolsIO.splitseq_dual_index in protocols:
            return "parse-wt-mega-v2-dual-index-libspec-3.yaml.j2"
        elif ProtocolsIO.ont_library_prep in protocols:
            return "parse-wt-mega-v2-nanopore.yaml.j2"
        else:
            raise ValueError("Unrecognized library protocol")

    # parse v2 48 well
    if ProtocolsIO.splitseq_100k_v2 in protocols:
        if ProtocolsIO.splitseq_single_index in protocols:
            return "parse-wt-v2-single-index-libspec-3.yaml.j2"
        elif ProtocolsIO.splitseq_dual_index in protocols:
            return "parse-wt-v2-dual-index-libspec-3.yaml.j2"
        elif ProtocolsIO.ont_library_prep in protocols:
            return "parse-wt-v2-nanopore.yaml.j2"
        else:
            raise ValueError("Unrecognized library protocol")

    # share-seq
    if ProtocolsIO.share_seq in protocols:
        return "uci-share-seq-rna.yaml.j2"
    
    raise ValueError("Unrecognized splitseq protocols {}".format(protocols))

def get_library_kit_from_protocols(protocols):
    if ProtocolsIO.ont_library_prep in protocols:
        return {
            "library_protocol": "Any",
            "library_kit": "cDNA Exome Capture v1.0.1",
            "sequence_kit": "ONT Ligation Sequencing Kit V14",
        }

    if ProtocolsIO.share_seq in protocols:
        # we need to tell rna & atac apart
        return {
            "library_protocol": "single-nucleus RNA sequencing assay (OBI:0003109)",
            "library_kit": "custom",
            "sequence_kit": "NextSeq 2000 P4 XLEAP-SBS Reagent Kit",
        }

    if ProtocolsIO.splitseq_100k_v2 in protocols:
        parse_kit_name = "Evercode WT v2.0.1"
    elif ProtocolsIO.splitseq_1M_v2 in protocols:
        parse_kit_name = "Evercode WT Mega v2.0.1"
    else:
        raise ValueError("Missing splitseq protocol")

    if ProtocolsIO.splitseq_single_index in protocols:
        illumina_kit_name = "single index"
    elif ProtocolsIO.splitseq_dual_index in protocols:
        illumina_kit_name = "dual index"
    else:
        raise ValueError("Missing illumina protocol")
        
    if len(set(protocols).intersection(single_cell_protocols)) > 0:
        library_protocol = "single-cell RNA sequencing assay (OBI:0002631)"
    elif len(set(protocols).intersection(single_nucleus_protocols)) > 0:
        library_protocol = "single-nucleus RNA sequencing assay (OBI:0003109)"
    else:
        raise ValueError("Unable to detect cell versus nucleus")

    context = {
        "library_protocol": library_protocol,
        "library_kit": f"{parse_kit_name} {illumina_kit_name}"
    }
    return context    
