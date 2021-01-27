
import gzip
from argparse import ArgumentParser

aa_dict={"ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLN":"Q","GLU":"E","GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V"}
#out_dict={}


def out(file_,s):
    bool1=[0,0,0]
    loop_=False
    dict_={}
    entity_id=0
    asym_id=""
    seq_id=0
    pdb_id=""
    count=0
    out_dict={}
    
    #↓_entity_poly_seq,_atom_siteにいるかどうか
    at_s_a_bool=[0,0]

    #######↓リストのインデックス間違えていた
    for l in file_:
        l=l.rstrip("\n")
        l=l.rstrip(" ")
        if bool1[0] and "_entry.id" in l:
            pdb_id=l.split()[1]


        #↓#,loop_が続いた場合                                                                                                                                  
        if loop_:
            if l.startswith("_"):
                #↓辞書にタグを追加                                                                                                                                 
                if "." in l and l.split(".")[0]=="_entity_poly_seq" and s:
                    dict_[l.split(".")[1]]=count
                    count+=1
                    at_s_a_bool[0]=1
                elif "." in l and l.split(".")[0]=="_atom_site" and not s:
                    dict_[l.split(".")[1]]=count
                    count+=1
                    at_s_a_bool[1]=1
            
            else:
                #↓entity_poly_seqについて  
                if at_s_a_bool[0] and not "#" in l:
                    #↓dict.get(a,b)でkeyなかったときのdefault値設定                                                                                                                        
                #if s and len(dict_.keys())==4 and l.split()[-1]=="n":
                    if l.split()[dict_['entity_id']]==entity_id:
                    
                        out_dict[entity_id][0]+=aa_dict.get(l.split()[dict_["mon_id"]],"X")
                    else:
                        entity_id=l.split()[dict_["entity_id"]]
                   
                        out_dict[entity_id]=[aa_dict.get(l.split()[dict_["mon_id"]],"X"),pdb_id]
                
                #↓atom_siteについて
                elif at_s_a_bool[1] and not "#" in l and l.split()[dict_["group_PDB"]]=="ATOM":                                                                                                                                
                #elif not s and len(dict_.keys())==21 and l.split()[dict_["group_PDB"]]=="ATOM":
                    l_=l.split()
                    if l_[dict_["label_asym_id"]]==asym_id:
                        if l_[dict_["label_seq_id"]]==seq_id:
                            pass

                        else:
                            seq_id=l_[dict_["label_seq_id"]]
                   
                            out_dict[asym_id][0]+=aa_dict.get(l_[dict_["label_comp_id"]],"X")
                    else:
                        asym_id=l_[dict_["label_asym_id"]]
                        #######↓ここでseq_id設定しないと、最初のアミノ酸が二つ繰り返してしまう
                        seq_id=l_[dict_["label_seq_id"]]
                  
                        out_dict[asym_id]=[aa_dict.get(l_[dict_["label_comp_id"]],"X"),pdb_id]


        #↓#,loop_の判定                                                                                                                                        
        if bool1[0] and "loop_" in l:
            bool1[1]=1
            loop_=True

        elif l[0]=="#":
            bool1[0]=1
            loop_=False
            #######↓#が来る毎に辞書を初期化しないといけない
            dict_={}
            #↓どこにいるのか初期化
            at_s_a_bool=[0,0]

        else:
            bool1=[0,0]

    return out_dict


def output(file_,s,error_):
    if error_:
        print("ERROR")
    else:
        out_dict=out(file_,s)
        for key in out_dict.keys():
            print(">{}:{}".format(out_dict[key][1],key))
            print(out_dict[key][0])


def main():
    """                                                                                                                                                        
    #↓前置き                                                                                                                                                   
    import gzip                                                                                                                                                
    from argparse import ArgumentParser                                                                                                                        
    """


    parser=ArgumentParser()
    parser.add_argument("inputfile",help="input filename")
    parser.add_argument("-s",action="store_true")
    parser.add_argument("-a",action="store_true")
    args=parser.parse_args()
    inputfile=args.inputfile

    s=args.s
    a=args.a
    error_=False
    if (s and a) or (not s and not a):
        error_=True

    #↓処理                                                                                                                                                     
    if inputfile.endswith('.gz'):
        with gzip.open(inputfile,"rt") as f:
            output(f,s,error_)
    else:
        with open(inputfile) as f:
            output(f,s,error_)


if __name__=="__main__":
    main()



