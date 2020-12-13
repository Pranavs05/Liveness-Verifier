import sys

def main():

    cval=0          #initialize counter value
    interval=2     # counter interval 
    count = int(sys.argv[1])            # takes user count 
    for i in range(0,(count),3):
        #print("here")
        nextval = cval+interval
        #print("R"+str(i)+" true"+" 100 "+" (SMTP.MTA="+str(i)+")"+" add(R"+str((i+1))+")"+",add(R"+str((i+2))+")"+",delete("+"R"+str(i)+")"+",send()"+"\n" ,%(i,i,i+1,i+2,i))
        print("R{0} true 100 (SMTP.MTA={1}) add(R{2}),add(R{3}),delete(R{4}),send()".format(i,i,(i+1),(i+2),i))
        print("R{0} false 100 (SMTP.MTA={1}),{2}≤c{3}<{4} send()".format(i+1,i,cval,i,nextval))
        print("R{0} false 100 (SMTP.MTA={1}),{2}≤c{3}<{4} drop()".format(i+2,i,nextval,i,(nextval+interval)))
        #print("R"+rnext2+"\t"+"false"+"100"+"(SMTP.MTA="+i+"),"+cval"<="+c+i+"<"+nextval+"\t"+"drop()"+"\n")
        cval=nextval+interval


if __name__ == "__main__":
    main()