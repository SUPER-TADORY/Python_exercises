
from argparse import ArgumentParser
import subprocess

def main():
    parser=ArgumentParser()
    parser.add_argument("--blast",default="/home/common/packages/blast/blast-2.2.26/bin/blastall")
    parser.add_argument("--database",default="/home/common/db/blastdb/uniprot/uniprot")
    parser.add_argument("inputfile",help="input filename")
    args=parser.parse_args()

    p=subprocess.Popen([args.blast,"-i",args.inputfile,"-d",args.database,"-p","blastp","-m","7"],stdout=subprocess.PIPE)
    text, err = p.communicate()#blast検索のデータを変数に格納する

    import xml.etree.ElementTree as ET
    root=ET.fromstring(text)#XMLの情報を木構造にして読み込む

    for i,hit in enumerate(root.iter("Hit")):
        print(f"Alignment{i+1}",hit.find("Hit_def").text)
        for hsp in hit.iter('Hsp'):
            d={c.tag:c.text for c in hsp}
            print("Query\t{}\t{}\t{}\n\t\t{}".format(d["Hsp_query-from"],d["Hsp_qseq"],d["Hsp_query-to"],d["Hsp_midline"]))
            print('sbjct\t{}\t{}\t{}'.format(d["Hsp_hit-from"],d["Hsp_hseq"],d["Hsp_hit-to"]))
        print()
        if i==9:
            break


if __name__=="__main__":
    main()






    

