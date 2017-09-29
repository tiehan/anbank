
## 项目需求--20170506
根据序列质量（如测序结果20170420文件夹里的“TSS20170421-028-2239.xls”），剔除文件夹中的套峰序列和短序列（如低于600 bp的序列）。

根据测序公司提供的测序结果（.ab1格式），批量截取其中的一段序列（可设置，如第50-600 bp位置的序列），导出序列为.fasta文件，并把多条序列合并为一个.fasta文件（如20170420.fasta文件）。
利用ncbi离线数据库，查找每条序列最相似的模式菌株，显示（相似菌株的种属名、16S rRNA基因的NCBI登录号，相似度），并生成excel文件，生产的excel文件能与我们的其它excel文件（记录每个序列的来源等信息）合并，并一一对应（如信息汇总表.xlsx）
OTU聚类分析序列，按照97%相似性聚类，并标示出代表性序列。
建立一个新的文件夹，命名“序列信息汇总”，把每次测序分析后的.fasta序列和对应的excle表格备份一份到该文件夹下面；
将“序列信息汇总”文件夹中多次累计测序获得的序列.fasta序列信息合并为一个数据集，以用于后面的新增序列比对。
每次出现新增序列都要重复步骤1~5，并将.fasta序列信息自动追加到上述数据集中，并将新获得的测序序列与之前完成的测序序列进行比对，显示最相似序列及相似性。

### 讨论 (已解决)
1. 项目名？
bimicro 可否？

microbe-res （microbe-res）

2. 输入和输出文件是单独存放，还是合并在一起存放


3. 输入？
    - excel文件1 （片段大小这列 >600 反应结果这一列仅且为“成功”）
    - excel文件2 （序列实验信息，提供一个合并命令，分析结果与提供的excel2文件合））
    - 测序结果文件夹

4. 汇总信息总表
    这个总表的列是的行数和名字是一定的吗？
    
5. OTU聚类分析序列，按照97%相似性聚类，并标示出代表性序列。
    每一批样本都要聚类吗？
    需要跟之前的序列聚类吗？
    聚类后的文件放在哪？

6. 第8条“每次出现新增序列都要重复步骤1~5，并将.fasta序列信息自动追加到上述数据集中，
并将新获得的测序序列与之前完成的测序序列进行比对，显示最相似序列及相似性。”
跟之前的序列比对？需要跟nr库比对一样
    
7. 文件夹层次
- raw_data  存放原始文件
    - 20170505 存放每次的分析数据（以日期命名文件夹）
        - excel文件（需要有“片段大小”和“反应结果”这两列）
        - 测序结果的文件夹（包含seq和ab1文件）

- data 分析以后的数据
    - 20170505 存放每次的分析数据（以日期命名文件夹）
        - 合并的fasta文件（20170505.fa）
        - 比对原始的结果(20170505_blast_result.tsv)
        - 比对提取结果（20170505_result.tsv 序列名称，最相似相似菌株的种属名、16S rRNA基因的NCBI登录号，相似度）
    
    - 20170405
      - 同上
    
    - Total 分析结果的汇总
        - 所有fasta文件（total.fa）
        - 比对提取结果汇总（total_result.tsv 序列名称，最相似相似菌株的种属名、16S rRNA基因的NCBI登录号，相似度）
        - otu聚类
        

### 讨论2 （已解决）
 物种相似的结果提取
 1。目前来说去获得序列对应的物种可以通过blast，也可以通过rdp ，为什么我们选择的是blast，不是rdp
 2。比对结果的输出（选取最佳的比对结果，并输出4列）：序列名称，最相似相似菌株的种属名、16S rRNA基因的NCBI登录号，相似度
    有时候一条序列99%相似性的有好几条，例如：
    仅仅只输出第一条的结果吗？

## 讨论3（用什么数据库）
nr库的两个问题 ： 1.因为nr是蛋白序列，我们比对的序列是fasta序列，所以需要用blastx 但用blastx比对的时候 速度很慢。   2.nr库没有过滤，所以比对的最好的结果，可能是hypothetical protein RUMTOR_02907 [Ruminococcus torques ATCC 27756]  

如果定义97%的相似性为阈值，57序列中有8条是需要人工来做nr比对矫正的,这个工作量有些大
然后我用greegene的数据库通过rdp来注释，这8条序列注释的属名都是一致的
因为rdp也是下载的ncbi的16s数据库中的序列，然后聚成Otu，选择一条代表序列作为参比序列



NCBI做blast的地址：    
https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&BLAST_SPEC=TargLociBlast

数据库下载地址：

ftp://ftp.ncbi.nlm.nih.gov/blast/db/16SMicrobial.tar.gz
tar -zxvf 16SMicrobial.tar.gz 

blast最新程序
ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
linux程序
ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.6.0+-x64-linux.tar.gz

Judge microbial species after sequencing and store information for microbial resources.

log管理


讨论三：

1. 为什么只提第50-600 bp位置的序列，而不考虑测通整个16s，序列越长，比对结果越可信（Uniting the classification of cultured and uncultured bacteria and archaea using 16S rRNA gene sequences）
2. 没有做嵌合体的检查？这个单菌的应该不用做吧？
3. 数据库与软件的自动更新，后续待完成


## 20170522提出的需求
1.blast数据库16sMicro换成nr库  ==》服务器下载Nr数据(已下载78%，待跟踪？？) 替换成rdp + 16s比对
2.登陆号只要NR_11780 ，不需要.或其他信息  （已修正）
3.分离菌株 ==》属种 （前两个字符）        （已修正）
4.每次结果有一个otu分类的结果               （已修正）
5.分类地位 ==》师兄提供，我这边整合        (待跟踪？？)
6.小数点到个数                            （已修正）
7.total_otus.txt中加入一列，计算多少个序列，每个序列跟这个otu的相似性  （已修正）

下载nr库
weget -c -i nr_download.list

ls *.tar.gz | xargs -n1 tar xzvf

## 20170524解决的问题
- 提供了filter_identity  提出比对结果相似性很低的序列，进行人工矫正
- 合并rdp和blast的结果，界门纲目科属的信息有rdp提供（有冲突的需要人工矫正额）


## 20170531 解决的问题

1）对测序质量列表中所有成功序列进行分析（包括成功/成功，双峰/成功，杂合位点/成功，信号中断等），这样的话在最终汇总表中也会需要显示测序质量这一列信息；
答复：可以

2）考虑到anBank使用的广泛性，存在不同的用户在同一天（raw_data中日期文件名相同）进行数据分析的情况，应该怎样区分命名？
答复：建议是以日期来命名，也可以不以日期来命名的，或者在整个日期后面加一个用户名，例如：20170522_cl

3）在多人使用的时候我们希望每次分析的数据只跟自己的数据进行汇总分析的情况，而不是将文件夹中所有用户之前运行过的数据进行汇总；
答复：不是太理解，不是要建立一个总库么？

4）我们的数据存在同一天送多个96孔板测序的情况，就会出现测序编号20170531-1-A1以及20170531-2-A1的情况，这样对运行有没有影响，或是需要固定成一个怎样的测序编号模板？
答复：没影响。我分字符的是按_来划分的，所以名字里面只要不含有_就可以。若果有问题，再反馈给我。

5）麻烦师兄运行一下raw_data中20170506文件夹中的数据，我下午运行了一下出现了错误，但是不太看得懂哪里的问题；
# 输入说明：a.input文件夹为测序结果文件，解压缩，需要放置在raw_data文件夹下面
   b.excel为input下面的文件,excel文件中包含三列：样品名称（用于找序列，
   需要跟input_dir中的序列文件名保持一致），片段大小(用于过滤序列)，反应结果（仅且仅当成功才提取这个序列
   20170506中的片段大小这一列没有内容，所以跑不出结果


## 20170601 
1）运行20170504文件夹时，出现index Errow:list index out of range
答复： 1.建议问题可以更具体一些的，你输入的命令是什么?  运行到哪一步出问题？ 屏幕上会有最后一行的运行记录。
      2.因为rdp注释结果中有只到门水平的，bugs已修复                 
                
2）我在docs文件夹下新放了一个汇总表20170601summary.xlsx,但是在合并的时候出现unbound Local Errow:local variable 'seq_col_loc' referenced before assignment
答复： excel文件sheet名字为analyis，默认"测序编号"这一列 跟序列名字一致
      20170601summary.xlsx并没有'测序编号'这一列

3)希望为不同用户设置不同子文件（rawdata→wq→20170420，data→wq→运行结果）
答复：已修改，新增--user这个参数，如果跟wq  就是在rawdata→wq→20170420，data→wq→运行结果 ,如果不加，就是默认的rawdata/biogas下面的文件夹
     例如：20170420文件夹放在radata/biogas文件夹下面，运行python anbank.py run --excel TSS20170421-028-2239.xls --input 20170420 --user biogas 即可
      
4）能否设置反应结果这项当成功，就提取这个序列，不用精确等于成功，最终合并表中反应结果与测序公司给的反应结果这两列匹配
答复：已修改

## 20170614
1) 合并文件失败

## 20160629 
反馈：
我合并测序结果和原表格后，未进行PCR测序的数据全被删除了，这是为什么呢？
python anbank.py merge  --excel ../raw_data/zwq/ZWQPCR20170629.xlsx --output ../data/zwq/result_2017062901.xlsx --user zwq
原因：
我默认的就是   测序编号那一个  一旦为空  就不在最后的结果里面出现
解决：
现在已经改了  即使为空，也在最后的结果中出现

## 20170707 
1.报错
运行：
python anbank.py run --excel TSS20170704-028-0360.xls --input 2017070402 --user zwq
报错原因：
export RDP_JAR_PATH=/sam/rdp_classifier_2.2/rdp_classifier-2.2.jar;
/usr/lib/qiime/bin/assign_taxonomy.py -i /sam/anBank/data/zwq/2017070402/2017070402.fa -m rdp --rdp_max_memory 40000 -o  rdp_assigned_taxonomy -r /sam/anBank/database/greengene/gg_13_8_otus/rep_set/97_otus.fasta -t /sam/anBank/database/greengene/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt 
Traceback (most recent call last):
  File "/usr/lib/qiime/bin/assign_taxonomy.py", line 15, in <module>
    from qiime.util import (parse_command_line_parameters,
ImportError: cannot import name get_tmp_filename

解决策略：
用conda 来安装以及更新qiime
wget -c https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh

阅读最新的qiime流程
python anbank.py run --excel TSS20170706-028-0603.xls --input test --user test

测试assign这一步
查看assign_taxonomy.py脚本跟之前的有什么不一样 

python /sam/anBank/lib/miniconda2/pkgs/qiime-1.9.1-np110py27_0/bin/assign_taxonomy.py -i /sam/anBank/data/test/test/test.fa -m rdp --rdp_max_memory 40000 -o  rdp_assigned_taxonomy -r /sam/anBank/database/greengene/gg_13_8_otus/rep_set/97_otus.fasta -t /sam/anBank/database/greengene/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt


conda remove –name qiime1 –all
报错：

UnicodeEncodeError: 'ascii' codec can't encode character u'\u2013' in position 0: ordinal not in range(128


注释掉qiime的全局环境
sudo vim /etc/profile

 source /sam/anBank/lib/miniconda2/bin/activate 
 
 bioconda安装。。
 
 然后安装qiime
 
export RDP_JAR_PATH=/sam/rdp_classifier_2.2/rdp_classifier-2.2.jar;
export qiime=/sam/anBank/lib/miniconda2/pkgs/qiime-1.9.1-np110py27_0/lib/python2.7/site-packages/qiime；

/sam/anBank/lib/miniconda2/pkgs/qiime-1.9.1-np110py27_0/bin/assign_taxonomy.py  -i /sam/anBank/data/zwq/2017070402/2017070402.fa -m rdp --rdp_max_memory 40000 -o  rdp_assigned_taxonomy -r /sam/anBank/database/greengene/gg_13_8_otus/rep_set/97_otus.fasta -t /sam/anBank/database/greengene/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt 

2.程序比对出来的相似性比blast出来的结果要小


### 20170723
cd  /sam/anBank/bin
source /sam/anBank/lib/miniconda2/bin/activate qiime1
python anbank.py run --excel TSS20170704-028-0359.xls --input 2017070401 --user zwq

### 20170806
服务器系统更新
将anBank移动到了/home/sam/anBank下面来了
- 将miniconda中qiime对应的脚本修改了解释器的路径
- 增加ncbi数据库路径文件
- 将rdp移动到了lib中

### 20170817
因为所有序列聚类otu太慢，所以增加一个参数，选择是否进行所有序列的otu聚类
-rdp  False则是不进行所有序列的otu聚类，默认的是True
 

### 20170926
需求：

从最终合并的结果表中直接提取以下信息汇成表格（根据重新给你表格进行）
表头字段：
分离菌株，筛选测序质量字段仅且仅等于“成功”；
相似度，要求相似度≤97%；
保菌等级，对于相似度≤97%这一区间数值再进行等级区分，例：94%<相似度≤97%为等级1；90%<相似度≤94%为等级2；相似度<94%为等级3；
登录号（OTU）
菌株编号
样品来源
Treatment

要求：

1. 测试文件第一行不能为空行，必须为表头（删除了提供文件的第一空行）
2. 每一列都需要有表头 (在提供的文件中加了Genus	score 这两列的名字)
3. 每一列的表头不能重复（比如：有两个孔位，已经修改了其中的一个）

另：对total中每一个OTU分类的序列能否汇总成一个fasta文件

已解决：
新增extract和splitotu两个功能


## 使用说明：
(序列相似性技术路线是blast+ NCBI 16S数据库；
otu 聚类技术路线是rdp，算法为blast，97%的相似性)

原始数据解压缩放在raw_data下面，以时间来命名文件

1.序列相似性结果分析
   a.input文件夹为测序结果文件，解压缩，需要放置在raw_data文件夹下面
   b.excel为input下面的文件,excel文件中包含三列：样品名称（用于找序列，
   需要跟input_dir中的序列文件名保持一致），片段大小(用于过滤序列)，反应结果（仅且仅当成功才提取这个序列）

cd  /sam/anBank/bin
python anbank.py run --help

source /sam/anBank/lib/miniconda2/bin/activate qiime1
python anbank.py run --excel TSS20170421-028-2239.xls --input 20170420 --user biogas
 te
比对结果说明:
identity1  代表输入序列比对到数据库中的那部分序列跟参比序列的相似性（ncbi默认的相似性）	
identity2  代表整个输入序列跟参比序列的相似性
identity3  代表输入序列比对到数据库中的那部分序列除以整个参比序列的长度

2.合并excel文件和测序结果文件
 excel文件sheet名字为analyis，默认"测序编号"这一列跟序列名字一致,文件中的是20170420，我改为了20170406）
python anbank.py merge --help
python anbank.py merge  --excel ../docs/summary_info.xlsx --output ../docs/result.xlsx --user zmq




## 测试命令
cd  /home/sam/anBank/bin
source /home/sam/anBank/lib/miniconda2/bin/activate qiime1

## 1.序列分析
python anbank.py run --excel test.xls --input test --user test
### 不进行所有序列的Otu聚类
python anbank.py run --excel test.xls --input test --user test --rdp False

## 2.合并序列分析结果与样本记录信息
python anbank.py merge  --excel ../docs/summary_info.xlsx --output ../docs/result.xlsx --user zmq

## 3.提取相似性不高的序列
python anbank.py extract --input input.xlsx --output output.xlsx

## 4.获取每个otu中的fasta序列
python anbank.py splitotu --fasta input.fasta --otu out_file --outdir outputdir