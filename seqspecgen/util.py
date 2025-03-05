import json
from pathlib import Path
import seqspec
from seqspec.seqspec_check import check
from seqspec.seqspec_index import index as tool_index


def load_default_seqspec_schema():
    seqspec_path = Path(seqspec.__file__).parent
    schema_path = seqspec_path / "schema" / "seqspec.schema.json"
    with open(schema_path, "rt") as instream:
        seqspec_schema = json.load(instream)
    return seqspec_schema


def seqspec_validate(spec, schema=None):
    """Validate a yaml object against a json schema
    """
    if schema is None:
        schema = load_default_seqspec_schema()

    fake_fn = Path("test.yaml")
    return check(spec, fake_fn)


def generate_seqspec_tool_index(spec, row):
    tools = {
        "atac": "chromap",
        "rna": "kb",
        #("rna", "starsolo", ("RNA_fastq_R1", "RNA_fastq_R2")),
    }
    args = {}
    for modality in spec.modalities:
        tool = tools[modality]
        file_ids = [Path(row[x]["href"]).name for x in row]
        idtype = "file"

        args[tool] = tool_index(spec, modality, file_ids, idtype, tool)

    return args
        
