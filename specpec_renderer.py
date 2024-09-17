import enum
from pathlib import Path
import re

from flask import Flask, request, render_template

from encoded_client.encoded import ENCODED

ACCESSION_RE = re.compile("IGVF[A-Z0-9]+")
ALLOWED_READ_NAME = ["R1", "R2", "R3", "I1", "I2"]

ROOT = Path(__file__).parent
TEMPLATE_DIR = ROOT / "templates"

IGVF_SERVER = ENCODED("api.data.igvf.org")

app = Flask(
    __name__,
    # static_folder="path",
)


@app.route("/")
def index():
    return "\n".join((x.name for x in TEMPLATE_DIR.glob("*.j2")))


@app.route("/seqspec/", methods=["POST"])
def render(*args, **kwargs):
    measurement_set = None
    reads = {}

    if "measurement_set" in request.json:
        measurement_set = request.json["measurement_set"]
    if measurement_set is None or ACCESSION_RE.match(measurement_set) is None:
        return "Invalid accession {}", 400

    for read_name in ALLOWED_READ_NAME:
        if read_name in request.json:
            read_accession = request.json[read_name]
            if ACCESSION_RE.match(measurement_set) is None:
                return "Invalid accession {}", 400
            reads[read_name] = read_accession

    measurement_info = IGVF_SERVER.get_json(f"/measurement-sets/{measurement_set}")
    protocols = measurement_info.get("protocols", [])
    template = get_templates_by_protocols(protocols)
    print(template)

    context = get_library_kit_from_protocols(protocols)
    for read_name in reads:
        accession = reads[read_name]
        read_info = IGVF_SERVER.get_json(f"/sequence-files/{accession}/")
        context[f"{read_name}_accession"] = accession
        context[f"{read_name}_url"] = IGVF_SERVER.prepare_url(read_info["href"])
        context[f"{read_name}_min_length"] = read_info["minimum_read_length"]
        context[f"{read_name}_max_length"] = read_info["maximum_read_length"]
        context["sequence_kit"] = read_info.get("sequencing_kit", "")
        context["sequence_protocol"] = read_info.get("sequencing_platform", "")

    print(context)
    return render_template(template, **context)


class ProtocolsIO(enum.StrEnum):
    splitseq_100k_v2 = "https://www.protocols.io/view/evercode-wt-v2-2-1-eq2lyj9relx9/v1"
    splitseq_1M_v2 = "https://www.protocols.io/view/evercode-wt-mega-v2-2-1-8epv5xxrng1b/v1"
    ont_library_prep = "https://www.protocols.io/view/ont-library-prep-for-split-seq-cdna-eq2lyj1xmlx9/v1"
    splitseq_single_index = "https://www.protocols.io/view/evercode-single-index-pcr-5jyl82k9rl2w/v1"
    splitseq_dual_index = "https://www.protocols.io/view/evercode-dual-index-pcr-yxmvmeqe5g3p/v1"


def get_protocol_used_for_index(protocols):
    # Python 3.12 enums supports in directly
    protocols = [ProtocolsIO(p) for p in protocols if p in ProtocolsIO.__members__.values()]

    if len(protocols) == 0:
        raise ValueError(f"Unable to find information by {protocols}")

    return protocols


def get_library_kit_from_protocols(protocols):
    if ProtocolsIO.ont_library_prep in protocols:
        return {
            "library_protocol": "Any",
            "library_kit": "cDNA Exome Capture v1.0.1",
            "sequence_kit": "ONT Ligation Sequencing Kit V14",
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
    context = {
        "library_protocol": "Any",
        "library_kit": f"{parse_kit_name} {illumina_kit_name}"
    }
    return context

def get_templates_by_protocols(protocols):
    # the only thing different between the 100k and 1M is the 1M has more round 1 barcodes
    # which is handled by get_barcodes_from_protocols
    if ProtocolsIO.splitseq_1M_v2 in protocols:
        if ProtocolsIO.splitseq_single_index in protocols:
            return "parse-wt-mega-v2-single-index-libspec-1.yaml.j2"
        elif ProtocolsIO.splitseq_dual_index in protocols:
            return "parse-wt-mega-v2-dual-index-libspec-1.yaml.j2"
        elif ProtocolsIO.ont_library_prep in protocols:
            return "parse-wt-mega-v2-nanopore.yaml.j2"
        else:
            raise ValueError("Unrecognized library protocol")
    if ProtocolsIO.splitseq_100k_v2 in protocols:
        if ProtocolsIO.splitseq_single_index in protocols:
            return "parse-wt-v2-single-index-libspec-1.yaml.j2"
        elif ProtocolsIO.splitseq_dual_index in protocols:
            return "parse-wt-v2-dual-index-libspec-1.yaml.j2"
        elif ProtocolsIO.ont_library_prep in protocols:
            return "parse-wt-v2-nanopore.yaml.j2"
        else:
            raise ValueError("Unrecognized library protocol")
    else:
        raise ValueError("Unrecognized splitseq protocols {}".format(protocols))
    
