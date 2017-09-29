# encoding=utf8
import xlrd
import xlwt
import os
import time
from collections import OrderedDict as Od

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class WriteFiles(object):
    def __init__(self):
        pass

    @staticmethod
    def write_excel(hash,output_file):
        writebook = xlwt.Workbook()
        sheet_name = writebook.add_sheet('analysis',cell_overwrite_ok=True)
        for one_key in hash.keys():
            one_line = hash[one_key]['one_line']
            for ii in range(len(one_line)):
                if isinstance(one_line[ii],float):
                    result = one_line[ii]
                else:
                    result = one_line[ii]
                sheet_name.write(one_key,ii,result)
        writebook.save("%s" % output_file)


class ReadFiles(object):
    def __init__(self):
        pass

    @staticmethod
    def read_one_line(fd):
        with open(fd) as data1:
            for each_line in data1:
                result = each_line.strip()
        return result

    @staticmethod
    def read_tsv(input_file):
        seqs_info = {}
        with open(input_file) as data1:
            for each_line in data1:
                if each_line.strip() == '':
                    continue
                elif each_line.strip().startswith('#'):
                    header = each_line.strip().split('\t')

                else:
                    cnt = each_line.strip().split('\t')

                    seq_name = cnt[0]
                    seqs_info[seq_name] = {}
                    for ii in range(len(header)):
                        seqs_info[seq_name][header[ii]] = cnt[ii]
        return seqs_info



    @staticmethod
    def read_excel_onesheet(fd, sheet_name,same_line_debug=False):
        """:
        第一列必须唯一，且为英语，作为第一层键；
        第一行必须唯一，且为英语，作为二层键
        返回dict
        """
        if os.path.exists(fd):
            pass
        else:
            print '@Error:We can not find file :%s'%fd

        excel_hash = Od()
        workbook = xlrd.open_workbook(fd)
        worksheets = workbook.sheet_names()

        worksheet = workbook.sheet_by_name(sheet_name)
        num_rows = worksheet.nrows
        num_cols = worksheet.ncols
        for rown in range(1, num_rows):
            row_name = worksheet.cell_value(rown, 0)
            if same_line_debug:
                if row_name not in excel_hash.keys():
                    excel_hash[row_name] = Od()
                    key1 = row_name
                else:
                    print 'Same line %s' % row_name
                    exit()
            else:
                if rown not in excel_hash.keys():
                    excel_hash[rown] = Od()
                    key1 = rown
            for coln in range(0, num_cols):
                col_name = str(worksheet.cell_value(0, coln))
                if col_name not in excel_hash[key1].keys():
                    pass
                else:
                    print 'The same clown %s' % col_name
                excel_hash[key1][col_name] = worksheet.cell_value(rown, coln)
        return excel_hash

    @staticmethod
    def read_excel_onesheet2(fd, sheet_name,seq_name = '测序编号',same_line_debug=False):
        """:
        第一列必须唯一，且为英语，作为第一层键；
        第一行必须唯一，且为英语，作为二层键
        返回dict
        """
        if os.path.exists(fd):
            pass
        else:
            print '@Error:We can not find file :%s'%fd

        excel_hash = Od()
        workbook = xlrd.open_workbook(fd)
        worksheets = workbook.sheet_names()

        # print worksheets #.decode('utf-8')

        worksheet = workbook.sheet_by_name(sheet_name)
        num_rows = worksheet.nrows
        num_cols = worksheet.ncols
        num = 0
        for rown in range(0, num_rows):
            one_line_info = []
            for coln in range(0, num_cols):
                col_name = str(worksheet.cell_value(0, coln))
                if col_name == seq_name:
                    seq_col_loc = coln
                one_line_info.append(worksheet.cell_value(rown, coln))

            seq_name_line = worksheet.cell_value(rown, seq_col_loc)
            if seq_name_line != "pass" :
                num += 1
                excel_hash[num] = {}
                excel_hash[num]['seq_name'] = seq_name_line
                excel_hash[num]['one_line'] = one_line_info

        # print excel_hash.keys()
        return excel_hash


def safe_makedir(dname):
    """Make a directory if it doesn't exist, handling concurrent race conditions.
    """
    if not dname:
        return dname
    num_tries = 0
    max_tries = 5
    while not os.path.exists(dname):
        # we could get an error here if multiple processes are creating
        # the directory at the same time. Grr, concurrency.
        try:
            os.makedirs(dname)
        except OSError:
            if num_tries > max_tries:
                raise
            num_tries += 1
            time.sleep(2)
    return dname


def merge_blast_rdp_file(blast_fp,rdp_fp,result_fp):
    blast_info = Od()
    rdp_info = {}
    data3 = open(result_fp,'w')
    with open(rdp_fp) as data2:
        header2 = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus2', 'rdp_value']
        for each_line2 in data2:
            if each_line2.strip() == '':
                continue
            cnt2 = each_line2.strip().split('\t')

            seq2 = cnt2[0]
            taxon_speies = cnt2[1].split(';')
            rdp_value = cnt2[2]

            taxon_num = len(taxon_speies)

            rdp_kindom = '.'
            rdp_phylum = '.'
            rdp_class = '.'
            rdp_order = '.'
            rdp_family = '.'
            rdp_genus = '.'

            if taxon_num == 1:
                rdp_kindom = taxon_speies[0].replace('k__', '')
            elif taxon_num == 2:
                rdp_kindom = taxon_speies[0].replace('k__', '')
                rdp_phylum = taxon_speies[1].replace('p__', '')
            elif taxon_num == 3:
                rdp_kindom = taxon_speies[0].replace('k__', '')
                rdp_phylum = taxon_speies[1].replace('p__', '')
                rdp_class = taxon_speies[2].replace('c__', '')
            elif taxon_num == 4:
                rdp_kindom = taxon_speies[0].replace('k__', '')
                rdp_phylum = taxon_speies[1].replace('p__', '')
                rdp_class = taxon_speies[2].replace('c__', '')
                rdp_order = taxon_speies[3].replace('o__', '')
            elif taxon_num == 5:
                rdp_kindom = taxon_speies[0].replace('k__', '')
                rdp_phylum = taxon_speies[1].replace('p__', '')
                rdp_class = taxon_speies[2].replace('c__', '')
                rdp_order = taxon_speies[3].replace('o__', '')
                rdp_family = taxon_speies[4].replace('f__', '').replace('[', '').replace(']', '')
            elif  taxon_num >= 6:
                rdp_kindom = taxon_speies[0].replace('k__', '')
                rdp_phylum = taxon_speies[1].replace('p__', '')
                rdp_class = taxon_speies[2].replace('c__', '')
                rdp_order = taxon_speies[3].replace('o__', '')
                rdp_family = taxon_speies[4].replace('f__', '').replace('[', '').replace(']', '')
                rdp_genus = taxon_speies[5].replace('g__', '')

            if rdp_kindom == '':
                rdp_kindom = '.'
            if rdp_phylum == '':
                rdp_phylum = '.'
            if rdp_class == '':
                rdp_class = '.'
            if rdp_order == '':
                rdp_order = '.'
            if rdp_family == '':
                rdp_family = '.'
            if rdp_genus =='' :
                rdp_genus = '.'

            rdp_info[seq2] = [rdp_kindom, rdp_phylum, rdp_class, rdp_order, rdp_family,
                              rdp_genus, rdp_value]

    with open(blast_fp) as data1:
        for each_line in data1:
            if each_line.strip == '' :
                continue
            elif each_line.startswith('#'):
                header1 = each_line.strip().split('\t')
                header = header1 +header2
                data3.write('%s\n' % '\t'.join(header))
                continue
            cnt = each_line.strip().split('\t')
            seq = cnt[0]
            blast_info[seq] = cnt[1:]
            if seq in rdp_info.keys():
                info = cnt + rdp_info[seq]
            else:
                info = cnt + ['.', '.', '.', '.', '.', '.', '.']
            data3.write('%s\n' % '\t'.join(info))

    data3.close()


if __name__ == '__main__':
    pass
