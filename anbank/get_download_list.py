
def test1():
    """
    download_api = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr.00.tar.gz'
    :return: 
    """
    download_api = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr'
    result_fp = '../database/nr_download.list'
    data = open(result_fp,'w')
    for ii in range(68):
        if len(str(ii)) == 1:
            ii = '0'+str(ii)
        download_api2 = '%s.%s.tar.gz' % (download_api ,ii)
        data.write('%s\n' % download_api2)
    data.close()

def main():
    test1()


if __name__ == '__main__':
    main()
