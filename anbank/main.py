#coding:UTF-8
import os
import glob
import xlwt


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from anbank import base_dir,config
from anbank.log_anbank import logger,create_base_logger,setup_local_logging
from anbank.filehandler import safe_makedir, merge_blast_rdp_file
from anbank.blast_seq import blast_input,analysis_blast_result_xml
from anbank.filehandler import ReadFiles,WriteFiles
from anbank.get_otu import get_otu_by_rdp,get_taxonomy_info_by_rdp

data_dir = os.path.join(base_dir,'data')

def run_main(excel,input_dir,output_dir,qual_length,seq_start,seq_end,filter_identity,user,rdp):
    parallel = create_base_logger()
    setup_local_logging(config)

    fasta_file,fasta_info_file = get_fasta_seq(user,excel,input_dir,output_dir,qual_length,seq_start,seq_end)

    fasta_dir = os.path.dirname(fasta_file)
    fasta_base_name = os.path.basename(fasta_file)
    blast_dir = os.path.join(fasta_dir,'blast')
    safe_makedir(blast_dir)
    blast_output = os.path.join(blast_dir,fasta_base_name.replace('.fa','_blast_result.xml'))
    analysis_result = os.path.join(blast_dir,fasta_base_name.replace('.fa','_blast_result.tsv'))
    fail_fasta_file = fasta_file.replace('.fa','_fail_blast.fa')
    rdp_result_file = os.path.join(fasta_dir, 'rdp_assigned_taxonomy', fasta_base_name.replace('.fa','_tax_assignments.txt'))

    blast_rdp_file = fasta_file.replace('.fa','_blast_rdp_result.tsv')

    blast_input(fasta_file,blast_output)

    analysis_blast_result_xml(blast_output,analysis_result,fasta_file,fail_fasta_file,filter_identity)

    get_taxonomy_info_by_rdp(fasta_file)

    otu_dir = os.path.join(os.path.dirname(fasta_file),'otu')
    get_otu_by_rdp(otu_dir, fasta_file)

    merge_blast_rdp_file(analysis_result, rdp_result_file, blast_rdp_file)

    user_data_dir = os.path.join(data_dir,user)
    merge_result(user_data_dir)

    ## total seq otu
    if rdp == 'False':
        print 'We will skip total seqs otu analysis!'
        pass
    else:
        get_otu_by_rdp(os.path.join(user_data_dir,'Total','otu'),'../total.fa',genus_loc='Y')

    logger.warn('Finish analysis！ Thanks for using anBank')

def run_merge(excel,user,input,output):
    parallel = create_base_logger()
    setup_local_logging(config)

    input_file = os.path.join(base_dir,'data/%s/Total/total_genus_result.tsv' % user)
    seq_file = os.path.join(base_dir,'data/%s/Total/total_seq_info.tsv' % user)

    seqs_info = ReadFiles.read_excel_onesheet2(excel,sheet_name='analysis',same_line_debug=False)

    seqs_genus_info = ReadFiles.read_tsv(input_file)
    seqs_status_info = ReadFiles.read_tsv(seq_file)

    for one_key in seqs_info.keys():
        if one_key == 1:
            header = seqs_info[one_key]['one_line']
        else:
            seq_name = seqs_info[one_key]['seq_name']
            # print seq_name
            # seq_name2 = str(seq_name.encode('utf-8'))
            if seq_name in seqs_genus_info.keys():

                one_line1 = seqs_info[one_key]['one_line'][:-12]
                # print seqs_genus_info[seq_name]['genus']
                status =seqs_status_info[seq_name]['status'].decode('utf-8')
                # status =''
                one_line2 = [status,
                             seqs_status_info[seq_name]['result'],
                            seqs_genus_info[seq_name]['genus'],'.',

                             seqs_genus_info[seq_name]['identity3'],
                             seqs_genus_info[seq_name]['identity2'],
                             seqs_genus_info[seq_name]['accession'],
                             seqs_genus_info[seq_name]['kingdom'],
                             seqs_genus_info[seq_name]['phylum'],
                             seqs_genus_info[seq_name]['class'],
                             seqs_genus_info[seq_name]['order'],
                             seqs_genus_info[seq_name]['family'],
                             seqs_genus_info[seq_name]['genus2'],
                             seqs_genus_info[seq_name]['rdp_value']
                             # '.','.','.','.','.','.'
                             ]
                # one_line2 = []
                one_line = one_line1+one_line2
                seqs_info[one_key]['one_line'] = one_line

            elif seq_name in seqs_status_info.keys():
                one_line1 = seqs_info[one_key]['one_line'][:-12]
                status = seqs_status_info[seq_name]['status'].decode('utf-8')
                one_line2 = [status,seqs_status_info[seq_name]['result']]
                one_line = one_line1 + one_line2
                seqs_info[one_key]['one_line'] = one_line

    WriteFiles.write_excel(seqs_info,output)
    logger.warn('Finish merging！ Thanks for using anBank')

def get_fasta_seq(user,excel,input_dir_raw,output_dir,qual_length,seq_start,seq_end):

    input_dir = os.path.join(base_dir,'raw_data',user,input_dir_raw)
    if not os.path.exists(input_dir):
        logger.warn('We can not find sequences dir %s' % input_dir)
        exit()
    excel_file = os.path.join(input_dir,excel)

    seqs_info = ReadFiles.read_excel_onesheet(excel_file,sheet_name=' sheet1',same_line_debug=False)

    output_dir1 = os.path.join(base_dir, 'data', user)
    output_dir2 = os.path.join(base_dir, 'data', user,input_dir_raw)
    safe_makedir(output_dir1)
    safe_makedir(output_dir2)

    fasta_file = os.path.join(output_dir2, '%s.fa' % input_dir_raw)
    fasta_info_file = os.path.join(output_dir2, '%s_seq_info.tsv' % input_dir_raw)

    data2 = open(fasta_info_file,'w')
    header = ['#seq_name','status','result']
    data2.write('%s\n' % '\t'.join(header))
    sucessful_seqs = 0
    seqs_name = []
    for k1 in seqs_info:
        seq_name = seqs_info[k1]['样品名称']
        seq_length = seqs_info[k1]['片段大小']
        seq_status = seqs_info[k1]['反应结果']
        result = 0
        if int(seq_length)> qual_length and  '成功' in seq_status:
            sucessful_seqs += 1
            seqs_name.append(seq_name)
            result = 1
        info = [seq_name,seq_status,str(result)]
        data2.write('%s\n'% '\t'.join(info))

    data2.close()

    result_fp = open(fasta_file,'w')
    for one_file in os.listdir(input_dir):
        if one_file.endswith('seq'):
            seq_name2 = one_file.split('_')[0]
            if seq_name2 in seqs_name:
                with open(os.path.join(input_dir,one_file)) as data1:
                    seq = data1.read().strip()
                    seq2 = seq[seq_start:seq_end]
                result_fp.write('>%s\n' % seq_name2)
                result_fp.write('%s\n' % seq2)

    logger.info("%s has %s successful seqs" % (input_dir,sucessful_seqs))
    result_fp.close()
    if sucessful_seqs == 0:
        logger.info('There is no successful seqs,please check it!')
        exit()

    return fasta_file,fasta_info_file


def analysis_blast(blast_output,analysis_result):
    pass

def updata_db_files(fasta_file,analysis_result):
    pass

def merge_infomation(excel_file,tsv_file,out_excel):
    pass


def merge_result(data_dir):
    total_result = '%s/Total'%data_dir
    safe_makedir(total_result)
    total_fa = os.path.join(total_result,'total.fa')
    total_seq_info = os.path.join(total_result,'total_seq_info.tsv')

    total_genus_result = os.path.join(total_result,'total_genus_result.tsv')

    data1 = open(total_fa,'w')
    data2 = open(total_genus_result,'w')
    data6= open(total_seq_info,'w')
    data6.write('#seq_name\tstatus\tresult\n')
    if os.path.exists(total_result):
        pass
    else:
        safe_makedir(total_result)
    for fn in os.listdir(data_dir):
        if fn.startswith('Total'):
            continue
        fn_fa = os.path.join(data_dir,fn,'%s.fa'%fn)
        fn_seq = os.path.join(data_dir,fn,'%s_seq_info.tsv'%fn)

        blast_analysis_fp = os.path.join(data_dir,fn,'%s_blast_rdp_result.tsv'%fn)
        seqs_name = []
        skip_header = 0
        if os.path.exists(fn_fa):
            with open(fn_fa) as data3:
                for each_line in data3:
                    if each_line.strip() == '':
                        continue
                    if each_line.startswith('>'):
                        seq_name = each_line.replace('>','')
                        if seq_name not in seqs_name:
                            seqs_name.append(seq_name)
                        else:
                            # seqs_name.append(seq_name)
                            print 'You have same name %s please check it!' % seq_name
                            exit()
                    else:
                        pass
                    data1.write('%s\n' % (each_line.strip()))
        if os.path.exists(fn_seq):
            with open(fn_seq) as data5:
                for each_line in data5:
                    if each_line.strip() == '' or each_line.startswith('#'):
                        continue

                    data6.write('%s\n' % (each_line.strip()))
        if os.path.exists(blast_analysis_fp):
            with open(blast_analysis_fp) as data4:
                for each_line in data4:
                    if each_line.strip() == '' :
                        continue
                    elif each_line.startswith('#') and skip_header==0:
                        data2.write('%s\n' % (each_line.strip()))
                        skip_header =1
                    elif not each_line.startswith('#'):
                        data2.write('%s\n' % (each_line.strip()))

    data1.close()
    data2.close()
    data6.close()


def run_extract(input_excel,output_excel):
    excel_info = ReadFiles.read_excel_onesheet(input_excel, 'analysis')


    writebook = xlwt.Workbook()
    sheet_name = writebook.add_sheet('analysis',cell_overwrite_ok=True)
    header = ['ID','样品来源','Treatment','菌株编号',
              '测序质量','登录号','相似度','保菌等级']

    for ii in range(len(header)):
        nrow = 0
        sheet_name.write(nrow, ii, header[ii].decode('utf-8'))

    for k1 in excel_info.keys():
        identity = excel_info[k1]['相似度']
        seq_qual = excel_info[k1]['测序质量']

        if identity != '' and seq_qual =='成功' :
            identity2 = float(identity)
            if identity2 <= 97:
                nrow += 1
                if identity2 >94:
                    rank_info = 1
                elif identity2>90:
                    rank_info = 2
                else :
                    rank_info = 3
                info = [ nrow , excel_info[k1]['样品来源'],
                        excel_info[k1]['Treatment'],
                        excel_info[k1]['菌株编号'],
                        excel_info[k1]['测序质量'],
                        excel_info[k1]['登录号'],
                        excel_info[k1]['相似度'],
                        '%.2f' % rank_info
                        ]
                for ii in range(len(info)):
                    sheet_name.write(nrow, ii, info[ii].decode('utf-8'))
                    print info
            else:
                pass
                # print identity,identity2,type(identity2)

    print output_excel
    writebook.save(output_excel)
    # print excel_info

def run_split(fasta,otu_file,outdir):
    #otus = {}
    safe_makedir(outdir)
    with open(otu_file) as data1:
        for each_line in data1:
            if each_line.strip() == '':
                continue
            cnt = each_line.strip().split()
            otu_accession = cnt[0].split('|')[3].split('_')[1].split('.')[0]
            #otus[cnt] = cnt[1:]
            cmd = "extract_seqs_by_sample_id.py -i %s -o %s/%s.fa -s %s " % (fasta,outdir,otu_accession,','.join(cnt[1:]) )
            print cmd
            logger.info(cmd)
            os.system(cmd)

    pass
