

import sys
from argparse import ArgumentParser
import exercise2

"""
parser=ArgumentParser()
parser.add_argument('-3','--three',help='option',action='store_true')
parser.add_argument('-6','--six',help='option',action='store_true')
parser.add_argument('filename',help='input filename')
args=parser.parse_args()

frametype=0
if args.three:
    frametype=3
elif args.six:
    frametype=6

inputfile=args.filename
"""

def clean_and_torna(file):#入力を整えて、そのままのコードと転写したコードを辞書型で返す
    seq_dict={}
    header,seq="",""
    for l in file:
        l=l.rstrip("\n")
        l=l.replace(' ','')
        if l[0]==">":
            if not header=="":
                seq_dict[header]=(seq,exercise2.trans(seq))
            header=l
            seq=""
        else:
            seq+=l
    seq_dict[header]=(seq,exercise2.trans(seq))
    return seq_dict


def codon_trans(s):#一つのコドンに対応するアミノ酸、ストップコドンならばbool型で返す
    st=s.upper()
    codon_dict={'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V','TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A','TAT':'Y','TAC':'Y','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E','TGT':'C','TGC':'C','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}
    stop=False
    st_a=""
    if st=="TAA" or st=="TAG" or st=="TGA":
        stop=True
        #↓追加
        st_a="-"
    else:
        st_a=codon_dict[st]

    return (st_a,stop)


def seq_trans(seq):#塩基配列を入れると同じ向きの3つのフレームタイプのアミノ酸配列に翻訳してリスト型で返す
    seq_list=[]
    for i in range(3):
            count=i
            out_seq=""
            while count+3<len(seq):
                #↓ストップコドンも追加するようにした
                """
                if not codon_trans(seq[count:count+3])[1]:
                    out_seq+=codon_trans(seq[count:count+3])[0] 
                else:
                    break
                """
                out_seq+=codon_trans(seq[count:count+3])[0]
                count+=3
            
            seq_list.append(out_seq)
    return seq_list


def seq_trans_(dic,frametype):#フレームタイプに応じて出力するアミノ酸配列を返す
    out_dict={}
    for key in dic.keys():
        seq_list=dic[key]
        out_dict[key]=seq_trans(seq_list[0])
        if frametype==6:
            out_dict[key].extend(seq_trans(seq_list[1]))
    return out_dict


def output(dic):
    for key in dic.keys():
        count=1
        for obj in dic[key]:
            print(f"{key}:frame{count}")
            print(obj)
            count+=1


def main():
    #↓この部分はmain()の中に入れないと、別のプログラムにimportするときにエラーが起きてしまうかもしれない
    parser=ArgumentParser()
    parser.add_argument('-3','--three',help='option',action='store_true')
    parser.add_argument('-6','--six',help='option',action='store_true')
    parser.add_argument('filename',help='input filename')
    args=parser.parse_args()

    frametype=0
    if args.three:
        frametype=3
    elif args.six:
        frametype=6

    inputfile=args.filename

    with open(inputfile) as f:
        out=seq_trans_(clean_and_torna(f),frametype)
        output(out)
    """
      for l in f:
        l=l.rstrip("\n")
        l=l.replace(' ','')
        print(l)
    """
        


if __name__=="__main__":
    main()


