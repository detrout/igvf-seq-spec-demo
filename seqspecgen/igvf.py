"""Utilities that make requests to the IGVF portal for information
"""
import gzip
from pathlib import Path


def get_read_lengths(server, accession, reads_to_check=100, verbose=False):
    """Read some of the fastq and get the read lengths

    Somewhat replaced by the server offering min/max read length
    attribute
    """
    url = "/sequence-files/{accession}/@@download/{accession}.fastq.gz".format(
        accession=accession)
    lengths = set()
    resp = server.get_response(url, stream=True)
    if resp.status_code == 200:
        with gzip.GzipFile(fileobj=resp.raw) as stream:
            for i, line in enumerate(stream):
                header = line.decode("utf-8").strip()
                sequence = stream.readline().decode("utf-8").strip()
                lengths.add(len(sequence))
                qual_header = stream.readline().decode("utf-8").strip()
                quality = stream.readline().decode("utf-8").strip()
                if verbose:
                    print(header)
                if i > reads_to_check:
                    break
    resp.close()
    return lengths

def get_sequence_file_info(server, accession, read):
    url = f"/sequence-files/{accession}"
    sequence_file = server.get_json(url)

    if sequence_file is not None:
        return {
            f"{read}_file_id": accession,
            f"{read}_file_name": Path(sequence_file["href"]).name,
            f"{read}_min_len": sequence_file.get("minimum_read_length"),
            f"{read}_max_len": sequence_file.get("maximum_read_length"),
            f"{read}_file_type": sequence_file["file_format"],
            f"{read}_file_size": sequence_file["file_size"],
            f"{read}_url": server.prepare_url(sequence_file["href"]),
            f"{read}_md5sum": sequence_file["md5sum"],
        }

#get_sequence_file_info(server, "IGVFFI8222YBZL", "R1")

def get_barcode_info(server, prefix, igvf_id):
    record = server.get_json(igvf_id)

    # check that the href is accessible
    url = server.prepare_url(record["href"])
    response = server._session.head(url)
    if response.status_code == 404:
        print("Unable to access {}".format(url))

    return {
        f"{prefix}_file_id": record["accession"],
        f"{prefix}_file_name": Path(record["href"]).name,
        f"{prefix}_file_size": record["file_size"],
        f"{prefix}_url": url,
        f"{prefix}_md5": record["md5sum"]
    }
