import sys

def main():

    cval=0          #initialize counter value
    interval=2     # counter interval 
    count = int(sys.argv[1])            # takes user count 
    port1 = sys.argv[2]
    port2 = sys.argv[3]
    pval = 1000
    #pval = chr(ord('a'))
    for i in range(0,(count),3):
        nextval = cval+interval
        if pval == 'k' or pval =='o':
             pval = chr(ord(pval)+1)
        #print("R"+str(i)+" true"+" 100 "+" (SMTP.MTA="+str(i)+")"+" add(R"+str((i+1))+")"+",add(R"+str((i+2))+")"+",delete("+"R"+str(i)+")"+",send()"+"\n" ,%(i,i,i+1,i+2,i))
        print("R{0} true 100 src={1},dstport={2} add(R{3}),add(R{4})".format(i,(pval),port1,(i+1),(i+2)))
        print("R{0} false 100 src={1},dstport={2} send()".format(i+1,(pval),port2))
        print("R{0} false 100 dst={1},dstport={2} send()".format(i+2,(pval),port2))
        pval =pval+1            # Update port value 
        #pval = chr(ord(pval)+1)
        #print("R"+rnext2+"\t"+"false"+"100"+"(SMTP.MTA="+i+"),"+cval"<="+c+i+"<"+nextval+"\t"+"drop()"+"\n")



if __name__ == "__main__":
    main()