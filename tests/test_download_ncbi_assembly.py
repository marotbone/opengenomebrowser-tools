import shutil
from unittest import TestCase

import os
import logging
from opengenomebrowser_tools.download_ncbi_assembly import download_ncbi_assembly, convert_ncbi_assembly, download_and_convert_ncbi_assembly
from opengenomebrowser_tools.rename_genbank import GenBankFile, GenomeFile
from opengenomebrowser_tools.rename_fasta import FastaFile
from opengenomebrowser_tools.rename_gff import GffFile

logging.basicConfig(level=logging.INFO)

ROOT = os.path.dirname(os.path.dirname(__file__))
GENOMIC_DATABASE = f'{ROOT}/database'
ORAGNISMS_DIR = f'{GENOMIC_DATABASE}/organisms'

ASSEMBLIES = [('FAM3257', 'GCF_005864195.1', 'FEZ40_RS')]
DOWNLOAD_DIR = f'{ROOT}/test-data/ncbi-download'
CONVERT_DIR = f'{ROOT}/test-data/ncbi-convert'

assert os.path.isdir(GENOMIC_DATABASE)


def remove_if_exists(file: str):
    if os.path.isfile(file):
        os.remove(file)


def cleanup(files: [str]):
    [remove_if_exists(f) for f in files]


def get_paths(dir: str, prefix: str) -> (str, str, str, str, str, str):
    fna = f'{dir}/{prefix}.fna'
    gbk = f'{dir}/{prefix}.gbk'
    gff = f'{dir}/{prefix}.gff'
    ffn = f'{dir}/{prefix}.ffn'
    faa = f'{dir}/{prefix}.faa'
    return fna, gbk, gff, ffn, faa


class Test(TestCase):
    def test_download_FAM3257(self):
        # cleanup(get_paths(dir=DOWNLOAD_DIR, prefix='GCF_005864195.1'))
        fna, gbk, gff = download_ncbi_assembly(assembly_name='GCF_005864195.1', out_dir=DOWNLOAD_DIR)
        for file in (fna, gbk, gff):
            self.assertTrue(os.path.isfile(file), f'Expected outfile does not exist: {file=}')

    def test_convert_FAM3257(self):
        raw_fna, raw_gbk, raw_gff, _, _ = get_paths(dir=DOWNLOAD_DIR, prefix='GCF_005864195.1')
        out_fna, out_gbk, out_gff, out_ffn, out_faa = get_paths(dir=CONVERT_DIR, prefix='FAM3257')
        cleanup([out_fna, out_gbk, out_gff, out_ffn, out_faa])
        convert_ncbi_assembly(
            raw_fna, raw_gbk, raw_gff,
            out_fna, out_gbk, out_gff, out_ffn, out_faa,
            new_locus_tag_prefix='FAM3257_',
            old_locus_tag_prefix='FEZ40_RS',
            validate=True
        )

    def test_download_and_convert_FAM3257(self):
        # cleanup(get_paths(dir=DOWNLOAD_DIR, prefix='FAM3257'))
        download_and_convert_ncbi_assembly(assembly_name='GCF_005864195.1', new_locus_tag_prefix='FAM3257_', out_dir=DOWNLOAD_DIR)
        for file in get_paths(dir=DOWNLOAD_DIR, prefix='FAM3257'):
            self.assertTrue(os.path.isfile(file), f'Expected outfile does not exist: {file=}')
