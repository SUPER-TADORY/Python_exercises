import sys

inputfile=sys.argv[1]

def trans(seq): #塩基配列を受け取り、相補鎖を作る処理
    s=seq.translate(str.maketrans("acgtmrwsykvhdbnACGTMRWSYKVHDBN","tgcakyswrmbdhvnTGCAKYSWRMBDHVN"))
    return s

def out_clean(seq): #塩基配列を受け取り、出力を整える（空白と改行の挿入）処理
    out=""
    st=trans(seq)
    for i in range(len(st)//10):
        out+=st[i*10:(i+1)*10-1]
        if i%5==0:
            out+="\n"
        else:
            out+=""
    out+=st[len(st)//10:]
    return out

def main_clean(st):
    header,seq="",""
    for l in st:
        l=l.rstrip("\r")
        l=l.replace('"','')
        if l[0]==">":
            print(header,":REVERSE COMPLEMENT")
            print(out_clean(seq))
            header=l
            seq=""
        else:
            seq+=l
    print(header,":REVERSE COMPLEMENT")
    print(out_clean(seq))


def main():
    with open(inputfile) as f:
        main_clean(f)

if __name__=="__main__":
    main()