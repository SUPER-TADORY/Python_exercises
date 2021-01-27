def main():
    from argparse import ArgumentParser
    parser=ArgumentParser()
    parser.add_argument("--blast",default="/home/common/packages/blast/blast-2.2.26/bin/blastall")
    parser.add_argument("--database",default="/home/common/db/blastdb/uniprot/uniprot")
    parser.add_argument("inputfile",help="input filename")
    args=parser.parse_args()

    import subprocess
    p=subprocess.Popen([args.blast,"-i",args.inputfile,"-d",args.database,"-p","blastp"],stdout=subprocess.PIPE)
    for x in p.stdout:
        print(x.decode().rstrip())

if __name__=="__main__":
    main()
