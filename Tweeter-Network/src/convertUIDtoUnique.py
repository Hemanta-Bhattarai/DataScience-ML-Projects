import sys
import argparse
from argparse import RawDescriptionHelpFormatter
import textwrap
try:
    import pickle
except ImportError as e:
    print("Pickle is required for correct execution of program. Please install pickle")
    sys.exit(3)


tqdm_exist = True
try:
    from tqdm import tqdm
except ImportError as e:
    print("tqdm package not found. Its good to install it to see progress bar")
    tqdm_exist = False
    pass



def usage():
    print (__doc__)



def safe_run(func):
    def func_wrapper(*args, **kwargs):
        try:
            return int(func(*args, **kwargs))
        except Exception as e:
            print(e)
        

    return func_wrapper


@safe_run
def friend_list(count):
    infile = open(str(count)+".ntwk",'rb')
    return len(pickle.load(infile))




@safe_run
def ntwk2dat(count,node_dict, output):
    infile = open(str(count)+".ntwk",'rb')
    list_node = list(pickle.load(infile))
    infile.close()
    fileIn = open(output + str(count)+".dat","w")
    if tqdm_exist:
        for nodes in tqdm(list_node):
            if isinstance(nodes, int):
                fileIn.write("\t")
    else:
        for nodes in list_node:
            if isinstance(nodes, int):
                fileIn.write(str(node_dict[nodes]))
                fileIn.write("\t")
    
    fileIn.close()



@safe_run
def getAllNodes(N_limit):
    count = 0
    node = 0
    while count < N_limit:
        count = count + 1
        num = friend_list(count)
        if isinstance(num, int):
            node = node + num - 1  

        if (node % 1000) == 0:
            print("Nodes: %d"%(node))

    return(node)



def convertNtwkFiles(N_start, N_end, node_dict, output):
    if tqdm_exist:
        for count in tqdm(range(N_start, N_end + 1)):
            ntwk2dat(count, node_dict, output)
    else:
        for count in range(N_start, N_end + 1):
            ntwk2dat(count, node_dict, output)
        
            
@safe_run
def get_distinct_nodes_dict(N_start, N_end):
    distinct = []
    if tqdm_exist:
        for count in tqdm(range(N_start, N_end+1)):
            try:
                infile = open(str(count)+".ntwk","rb")
                list_node = list(pickle.load(infile))
                distinct = list(set(distinct + list_node))
            except:
                continue
    else:
        for count in range(N_start, N_end+1):
            try:
                infile = open(str(count)+".ntwk","rb")
                list_node = list(pickle.load(infile))
                distinct = list(set(distinct + list_node))
                if count%1000 == 0:
                    print(" %d .ntwk files read." %(count))
            except:
                continue
                
    return dict(zip(distinct, range(len(distinct))))





def main(argv):
    parser = argparse.ArgumentParser(
        description='Change the actual user id to some garbage value to preserve the user identity',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""
                    Example: python convertUIDtoUnique.py -s 1 -e 13271 -o ../data/ 
                    
                    """)

    parser.add_argument("-s","--start=", action="store",
                        dest="N_start", default = 1, type = int, help="first .ntwx file")
    parser.add_argument("-e","--end=", action="store", type=int,
                        dest="N_end", help="last .ntwx file")
    parser.add_argument("-o","--output_folder=", action="store", type=str,
                        dest="output", default = "./", help="Output folder for converted .ntwk file to .dat files")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(2)

    args=parser.parse_args()

    if (not args.N_end):
        parser.error("Last number of .ntwk file missing")
    N_end = args.N_end
    N_start = args.N_start
    output_folder = args.output
    print("Dictonary for all avaible distinct nodes generating")
    node_dict = get_distinct_nodes_dict(N_start, N_end)
    convertNtwkFiles(N_start, N_end, node_dict, output_folder)

if __name__ == "__main__":
    main(sys.argv[1:])

