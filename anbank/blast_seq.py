#coding:UTF-8
from __future__ import division
import subprocess
import time
import os
import sys
sys.path.append("/home/sam/anBank/lib/miniconda2/pkgs/biopython-1.70-np112py27_0/lib/python2.7/site-packages")

from Bio.Blast import NCBIXML

from log_anbank import logger
from anbank import base_dir
db_16s = os.path.join(base_dir,'database/16SMicrobial')
db_nr = os.path.join(base_dir,'database/nr/nr')

class BlastConfig(object):
    def __init__(self):
        self.bin = "blastn"
        # self.bin = "blastx"
        self.db = db_16s
        # self.db = db_nr
        self.word_size = 28  # tblastn and blastp can be 2
        self.outfmt = 5
        self.max_target_seqs = 15
        self.num_threads = 20
        self.evalue = 0.0001
        self.gapopen = 6
        self.gapextend = 2


def blast_input(input_fp, output_fp, blastconfig=BlastConfig()):
    cmd = "{0.bin} -task megablast -query {input} -db {0.db}  -evalue {0.evalue} " \
          "-num_threads {0.num_threads} -outfmt {0.outfmt} -gapopen {0.gapopen} " \
          "-gapextend {0.gapextend} -max_target_seqs {0.max_target_seqs} " \
          "-word_size {0.word_size} -out {output} ".format(blastconfig,
                                                           output=output_fp,
                                                           input=input_fp)

    # cmd = "{0.bin} -query {input} -db {0.db}  -evalue {0.evalue} " \
    #       "-num_threads {0.num_threads} -outfmt {0.outfmt} -gapopen {0.gapopen} " \
    #       "-gapextend {0.gapextend} -max_target_seqs {0.max_target_seqs} " \
    #       "-word_size {0.word_size} -out {output} ".format(blastconfig,
    #                                                        output=output_fp,
    #                                                        input=input_fp)
    out, error = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()

    logger.warn(cmd)


def analysis_blast_result_xml(input_xml,result_fp,fasta_file,fail_fasta_file,filter_identity):
    data2 = open(result_fp, "w")
    data2.write("#seq\tgenus\taccession\tquery_len\thit_len\tidentity1\tidentity2\tidentity3\tmismatch\tscore\tevalue\n")
    data3 = open(fail_fasta_file,'w')

    result_handle = open(input_xml)
    blast_records = NCBIXML.parse(result_handle)
    blast_records = list(blast_records)

    for blast_record in blast_records:
        query_id = blast_record.query  # query的名字
        query_length = blast_record.query_length
        query_seq = blast_record.query_letters

        if len(blast_record.alignments) == 0:
            continue
        for aligment in [blast_record.alignments[0]]:
            hsp_length = aligment.length

            for hsp in [aligment.hsps[0]]:
                align_title = aligment.title.split()
                align_accession = align_title[0].split('ref|')[1].split('.')[0]

                genus = ' '.join(align_title[1:3]).replace('[','').replace(']','')
                identity_len = hsp.identities
                gaps = hsp.gaps
                align_score = hsp.score
                align_evalue = hsp.expect
                identity_len = hsp.identities
                hsp_score = hsp.score
                query_seq = hsp.query

                align_len = len(query_seq) - int(gaps)
                identity_1 = '%.1f'% (int(identity_len) / int(align_len) * 100) #比对上的序列的相似性
                identity_2 = '%.1f' % (int(identity_len) / int(query_length) * 100 )#全长比对的百分比
                identity_3 = '%.1f' % (int(identity_len) / int(hsp_length) * 100 )#占比对序列的百分比
                mismatch = int(query_length) - int(identity_len)
                result = [query_id, genus,align_accession, str(query_length), str(identity_len),
                          identity_1,identity_2,identity_3,str(mismatch),align_score,align_evalue]

                if float(identity_1) < filter_identity:
                    data3.write('>%s\n' %query_id)
                    data3.write('%s\n'% query_seq)
            data2.write("%s\n" % "\t".join([str(jj) for jj in result]))

    data2.close()
    data3.close()


if __name__ == "__main__":
    input_xml = '../data/20170420/20170420.blast_result.xml'
    result_fp = 'test_result.tsv'
    analysis_blast_result_xml(input_xml,result_fp)

