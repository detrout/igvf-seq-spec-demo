from unitest import TestCase

from ..protocols import (
    filter_protocols_for_lookups,
    get_template_from_protocols,
    get_library_kit_from_protocols,
    ProtocolsIO,
)


class TestProtocols(TestCase):
    def test_filter_protocols_for_lookups(self):
        p = [ProtocolsIO.adrenal_nuclei_prep, "asdf"]
        r = filter_protocols_for_lookups(p)
        self.assertEqual(r, [ProtocolsIO.adrenal_nuclei_prep])

    def test_get_template_from_protocls(self):
        parse_single_1M_v2 = [
            ProtocolsIO.splitseq_1M_v2,
            ProtocolsIO.splitseq_single_index,
            ProtocolsIO.female_gonads_nuclei_prep,
        ]
        parse_dual_1M_v2 = [
            ProtocolsIO.splitseq_1M_v2,
            ProtocolsIO.splitseq_dual_index,
            ProtocolsIO.male_gonads_nuclei_prep,
        ]
        parse_single_100k_v2 = [
            ProtocolsIO.splitseq_1M_v2,
            ProtocolsIO.splitseq_single_index,
            ProtocolsIO.heart_nuclei_prep,
        ]
        parse_dual_100k_v2 = [
            ProtocolsIO.splitseq_100k_v2,
            ProtocolsIO.splitseq_dual_index,
            ProtocolsIO.pbmc_cell_prep,
        ]
        parse_ont_100k_v2 = [
            ProtocolsIO.splitseq_100k_v2,
            ProtocolsIO.ont_library_prep,
            ProtocolsIO.pbmc_cell_prep,
        ]
        uci_share_seq = [
            ProtocolsIO.share_seq,
            ProtocolsIO.pbmc_cell_prep,
        ]

        data = [
            (parse_single_1M_v2, "parse-wt-mega-v2-single-index-libspec-3.yaml.j2"),
            (parse_dual_1M_v2, "parse-wt-mega-v2-dual-index-libspec-3.yaml.j2"),
            (parse_single_100k_v2, "parse-wt-single-index-libspec-3.yaml.j2"),
            (parse_dual_100k_v2, "parse-wt-v2-dual-index-libspec-3.yaml.j2"),
            (parse_ont_100k_v2, "parse-wt-v2-nanopore.yaml.j2"),
            (uci_share_seq, "uci-share-seq-rna.yaml.j2"),
        ]
        for p, e in 
