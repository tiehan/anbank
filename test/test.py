# coding:utf-8
import os
import sys
import time


import os
base_dir = os.path.dirname(os.path.realpath(__file__))[:-5]

sys.path.insert(0, base_dir)
from anbank.blast_seq import analysis_blast_result_xml


def test1():
    input_xml = '../data/20170420/20170420.blast_result.xml'
    result_fp = '../test/test_result.tsv'
    analysis_blast_result_xml(input_xml,result_fp)



if __name__ == '__main__':
    test1()