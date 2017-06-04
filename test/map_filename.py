
import argparse
import os

def read_list(input_file):
    files_map = {}
    with open(input_file) as data1:
        for each_line in data1:
            if each_line.strip() == '':
                continue
            cnt = each_line.strip().split()
            file_name = cnt[0]
            changed_name = cnt[1]
            if file_name not in files_map.keys():
                files_map[file_name] = changed_name
    return files_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help="filename list")
    parser.add_argument("-i", help="input folder which has fastq files")
    args = parser.parse_args()

    result_dir = 'mapped_fa'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    input_dir = args.i
    input_file = args.l

    files_map = read_list(input_file)
    for fn in os.listdir(input_dir):
        if not fn.endswith('.fastq'):
            continue
        file_name = fn.replace('.fastq','')
        changed_name = files_map[file_name]
        cmd = 'sh FqtoFa.sh %s/%s.fastq %s >%s/%s.fasta '%(input_dir,file_name,
                                                           changed_name,result_dir,changed_name)
        print cmd
        os.system(cmd)

    # print files_map

    # print args.square**2


if __name__ == '__main__':
    main()