import sys

def main():

    cval=0          #initialize counter value
    interval=2     # counter interval 
    count = int(sys.argv[1])            # takes user count 
    source=1000
    for i in range(0,(count),3):
        #print("R"+str(i)+" true"+" 100 "+" (SMTP.MTA="+str(i)+")"+" add(R"+str((i+1))+")"+",add(R"+str((i+2))+")"+",delete("+"R"+str(i)+")"+",send()"+"\n" ,%(i,i,i+1,i+2,i))
        print("R{0} true 100 src={1},0≤c{2}<400 send()".format(i,source,i))
        print("R{0} true 100 src={1},400≤c{2}<800 send(rate limiter)".format(i+1,source,i))
        print("R{0} true 100 src={1},800≤c{2}<1200 drop()".format(i+2,source,i))
        #print("R"+rnext2+"\t"+"false"+"100"+"(SMTP.MTA="+i+"),"+cval"<="+c+i+"<"+nextval+"\t"+"drop()"+"\n")
        source=source+1


if __name__ == "__main__":
    main()