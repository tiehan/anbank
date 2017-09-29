"""
/usr/lib/qiime/bin/pick_otus.py -i good.fasta -m cdhit -o cdhit_picked_otus/ -n 100


export RDP_JAR_PATH=/sam/rdp_classifier_2.2/rdp_classifier-2.2.jar;

export RDP_JAR_PATH=/sam/rdp_classifier_2.2/rdp_classifier-2.2.jar;

/usr/lib/qiime/bin/assign_taxonomy.py -i %s -m rdp --rdp_max_memory 20000 -o rdp_assigned_taxonomy
-r /sam/qiime/qiime_software/gg_12_10_otus/rep_set/97_otus.fasta -t
/sam/qiime/qiime_software/gg_12_10_otus/taxonomy/97_otu_taxonomy.txt


/usr/lib/qiime/bin/assign_taxonomy.py -i 20170420.fa -m rdp --rdp_max_memory 20000 -o rdp_assigned_taxonomy
-r /sam/qiime/qiime_software/gg_12_10_otus/rep_set/97_otus.fasta -t
/sam/qiime/qiime_software/gg_12_10_otus/taxonomy/97_otu_taxonomy.txt

"""
import os

from log_anbank import logger
from anbank import base_dir
from anbank.filehandler import safe_makedir

db_16s = os.path.join(base_dir,'database/16SMicrobial')
greengene_fa = os.path.join(base_dir,'database/greengene/gg_13_8_otus/rep_set/97_otus.fasta')
greengene_taxonomy = os.path.join(base_dir,'database/greengene/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt')
rdp_path = os.path.join(base_dir,'lib/rdp_classifier_2.2/rdp_classifier-2.2.jar')

def analysis_otu_info(blast_result,otu_result,analysis_result):
    seqs_info = {}
    with open(blast_result) as data1:
        for each_line in data1:
            if each_line.strip() == '' or each_line.startswith('#'):
                continue
            cnt = each_line.strip().split('\t')
            seq_name = cnt[0]
            ident = cnt[5]
            seqs_info[seq_name] = ident
    data3 = open(analysis_result,'w')
    # header = ['#genus','seq_num',]
    with open(otu_result) as data2:
        for each_line in data2:
            if each_line.strip() == '' or each_line.startswith('#'):
                continue
            cnt = each_line.strip().split()
            blast_name = cnt[0].split('ref|')[1].split('.')[0]
            seq_num = len(cnt) - 1

            one_line_info = [blast_name,str(seq_num)]
            for ii in range(1,len(cnt)):
                one_seq = '%s(%s)' % (cnt[ii],seqs_info[cnt[ii]])
                one_line_info.append(one_seq)
            data3.write('%s\n' % '\t'.join(one_line_info))

    data3.close()


def get_taxonomy_info_by_rdp(input_fasta):
    work_here = os.getcwd()
    fasta_dir = os.path.dirname(input_fasta)
    fasta_base_name = os.path.basename(fasta_dir).split('.')[0]
    os.chdir(fasta_dir)
    cmd1 = "source /sam/anBank/lib/miniconda2/bin/activate qiime1;"
    cmd = "export RDP_JAR_PATH=%s;" \
          "assign_taxonomy.py -i %s -m rdp --rdp_max_memory 40000 -o  rdp_assigned_taxonomy -r %s -t %s " % (rdp_path,input_fasta,greengene_fa,greengene_taxonomy)

    # print cmd

    logger.warn(cmd)
    os.system(cmd)

    # exit()

    os.chdir(work_here)

    # rdp_result_file = os.path.join(fasta_dir,'rdp_assigned_taxonomy','%s_tax_assignments.txt' %fasta_base_name)
    # return rdp_result_file

def get_otu_by_rdp(workdir,input_fa,genus_loc = '.'):
    safe_makedir(workdir)
    now_dir = os.getcwd()
    os.chdir(workdir)

    fasta_dir = os.path.dirname(input_fa)
    fasta_base_name = os.path.basename(input_fa)
    if genus_loc == '.':
        blast_dir = os.path.join(fasta_dir,'blast')
        genus_result = os.path.join(blast_dir, fasta_base_name.replace('.fa', '_blast_result.tsv'))
    else:
        blast_dir = fasta_dir
        genus_result = os.path.join(blast_dir,fasta_base_name.replace('.fa','_genus_result.tsv'))

    otu_result = os.path.basename(input_fa).replace('.fa','_otus.txt')

    analysis_result = os.path.basename(input_fa).replace('.fa','_otus_result.tsv')

    #/usr/lib/qiime/bin/ old path
    cmd1 = 'pick_otus.py -i %s -m blast -o ./ -b %s' %(input_fa,db_16s)
    cmd2 = 'pick_rep_set.py -i %s -f %s -o rep.fna' % (otu_result,input_fa)
    # cmd3 = "source /sam/anBank/lib/miniconda2/bin/deactivate"
    logger.info(cmd1)
    logger.info(cmd2)
    os.system(cmd1)
    os.system(cmd2)
    # try:
    #     os.system(cmd3)
    # except:
    #     pass

    analysis_otu_info(genus_result, otu_result, analysis_result)

    os.chdir(now_dir)


