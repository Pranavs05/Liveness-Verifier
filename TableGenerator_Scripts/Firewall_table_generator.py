import sys

def main():

    cval=0          #initialize counter value
    interval=2     # counter interval 
    count = int(sys.argv[1])            # takes user count 
    source=1000
    dst=100
    for i in range(0,(count),5):
        #print("R"+str(i)+" true"+" 100 "+" (SMTP.MTA="+str(i)+")"+" add(R"+str((i+1))+")"+",add(R"+str((i+2))+")"+",delete("+"R"+str(i)+")"+",send()"+"\n" ,%(i,i,i+1,i+2,i))
        print("R{0} true 100 src={1},dst={2} delete(R{3}),delete(R{4}),delete(R{5}),send(IDPS)".format(i,source,dst,i,i+1,i+3))
        print("R{0} true 100 src={1},dst={2} delete(R{3}),delete(R{4}),delete(R{5}),drop()".format(i+1,dst,source,i,i+1,i+4))
        print("R{0} true 100 src={1},dst={2} send(IDPS)".format(i+2,source,dst))
        print("R{0} true 100 src={1},dst={2} drop()".format(i+3,dst,source))
        print("R{0} true 100 src={1},dst={2} send(IDPS)".format(i+4,dst,source))
        source=source+1


if __name__ == "__main__":
    main()