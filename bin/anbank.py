#!/usr/bin/python
#coding:UTF-8

import os
import sys
import click

reload(sys)
sys.setdefaultencoding('utf-8')
folder_here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, folder_here)
sys.path.insert(0, folder_here[:-3])


from anbank.main import run_main,run_merge,run_extract,run_split
import anbank

@click.group()
def cli1():
    pass

@cli1.command()
@click.option('--input', help=unicode('包含fasta文件的文件夹，包含测序文件',errors='ignore'))
@click.option('--excel', help=unicode('excel文件名，默认的是跟fasta文件放在一个文件夹下，包含 片段大小 和 反应结果这两列',errors='ignore'))
@click.option('--qual_length', help=unicode('要求测序序列长度的最小值,默认是600',errors='ignore'),default=600 )
@click.option('--seq_start', help=unicode('保留序列的起始位置，默认是50',errors='ignore') ,default=50 )
@click.option('--seq_end', help=unicode('保留序列的终止位置，默认是600',errors='ignore') ,default=600 )
@click.option('--output', help=unicode("输出文件夹，默认data文件夹",errors='ignore')  )
@click.option('--user', help=unicode("raw_data文件夹下的子文件夹，默认biogas",errors='ignore') ,default ='biogas' )
@click.option('--filter_identity', help=unicode("相似性判断，默认小于97的相似性判断为比对失败的序列",errors='ignore') ,default=97 )
@click.option('--version',nargs=0, default='.', help='程序版本')
@click.option('--rdp', help=unicode('总的序列是否聚类,默认的是True,如果False，则不聚类',errors='ignore'),default = 'True')
def run(excel,input,output,version,qual_length,seq_start,seq_end,filter_identity,user,rdp):
   """run pipeline"""
   if len(version) == 0:
        print anbank.__version__
        exit()
   run_main(excel,input,output,qual_length,seq_start,seq_end,filter_identity,user,rdp)

   pass


@click.group()
def cli2():
    pass

@cli2.command()
@click.option('--excel',help=unicode("输入的excel文件,默认测序编号跟物种比对结果的名字要一致", errors='ignore'))
@click.option('--user', help=unicode("raw_data文件夹下的子文件夹，默认biogas",errors='ignore') ,default ='biogas' )
# @click.option('--input',help=unicode("物种比对结果",errors='ignore'))
@click.option('--output',help=unicode("excel结果汇总",errors='ignore'))
# @click.option('--excel',help="input excel")
# @click.option('--input',help="blast resutl")
# @click.option('--output',help="excel merge result")
def merge(excel,output,user):
    """merge excel information with result"""
    input = ''
    run_merge(excel,user,input,output)
    pass
 


@click.group()
def cli3():
    pass
 
 
@cli3.command()
@click.option('--input',help=unicode("输入的excel文件", errors='ignore'))
@click.option('--output',help=unicode("输出的excel文件", errors='ignore'))
def extract(input,output):
    """extract information"""
    run_extract(input,output)
    pass



@click.group()
def cli4():
    pass

@cli4.command()
@click.option('--fasta',help=unicode("输入fasta文件", errors='ignore'))
@click.option('--otu',help=unicode("输入otu文件", errors='ignore'))
@click.option('--outdir',help=unicode("输出文件夹", errors='ignore'))
def splitotu(fasta,otu,outdir):
    """split otu"""
    run_split(fasta,otu,outdir)
    pass





@click.group()
def cli5():
    pass

@cli5.command()
@click.option('--output', help='excel')
def install():
    """install programs"""
    pass




main  = click.CommandCollection(sources=[cli1, cli2, cli3,cli4,cli5])
 
if __name__ == "__main__":
    main()