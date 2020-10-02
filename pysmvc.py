import sys
from collections import defaultdict	
def rep(s,b):
	for i in range(len(b)):
		v1='R'+str(i)+'1'
		w1='r'+str(i)+'1'+'.active=TRUE'
		if b[i]==1:
			s=s.replace(v1,w1)
		else:
			s=s.replace(v1,'TRUE')

		v='R'+str(i)
		w='r'+str(i)+'.active=TRUE'
		s=s.replace(v,w)
	return s

def getprop(prop,l,l1,actions,packets):
	if  prop[0]=="":
		return ("FALSE")
	elif not l:
		return ("TRUE")
	else:
		propt=prop
		#print(actions[l[0]])
		#print(packets[l[0]])
		if (((packets[l[0]]) in prop[0]) or (packets[l[0]])=="*")   and prop[1]==actions[l[0]]:
			pval=prop.copy()
			temp=prop
			if (packets[l[0]])=="*":
				temp[0]=""
			else:
				while  (packets[l[0]]) in temp[0]:
					s=temp[0].replace(packets[l[0]],"")
					temp[0]=s
			return(l[0]+"&"+l1[0]+"&"+getprop(temp,l[(1):],l1[(1):],actions,packets)+"|"+"!"+"("+l[0]+"&"+l1[0]+")"+"&"+getprop(pval,l[(1):],l1[(1):],actions,packets))
		elif (((packets[l[0]]) in prop[0]) or (packets[l[0]])=="*") and prop[1]!=actions[l[0]]:
			return("!"+"("+l[0]+"&"+l1[0]+")"+"&"+getprop(prop,l[(1):],l1[(1):],actions,packets))
		else:
			return(getprop(prop,l[(1):],l1[(1):],actions,packets))


def main():
	g = sys.argv[1]
	propfile = sys.argv[2]
	propf=open(propfile,"r")
	prop=propf.read()
	pop=prop.split(";")
	f = open(g,"r")
	b = open("myfile.smv","w")
	lines = f.readlines()
	r = [ ]
	sol=[]
	val = defaultdict(int)
	prio = defaultdict(int)
	packets = defaultdict(int)
	actions = defaultdict()
	for x in lines:
		r.append(x.split(' '))
	intervals = []
	ind=0
	bc=[0]*len(r)
	#actions =[]
	for i in range(1,len(r)):
		#print(r[i][3])
		if "\n" in r[i][4]:
			actions[r[i][0]]=r[i][4].replace("\n","")
		else:
			actions[r[i][0]] = r[i][4]
		if "c0" in r[i][3]:
			ind= r[i][3].index("c0")
			bc[i-1]=1
			#print(r[i][3][:(ind-2)])
			packets[r[i][0]]=(r[i][3][:(ind-2)])
			if ord(r[i][3][ind-2]) not in intervals:
				intervals.append(ord(r[i][3][ind-2]))
			if	ord(r[i][3][ind+3]) not in intervals:
				intervals.append(ord(r[i][3][ind+3]))
		else:
			packets[r[i][0]]=(r[i][3])
			#actions.append(r[i][3])
	for i in range(0,len(intervals)):
		intervals[i]=intervals[i]-48
	bc=bc[:-1]
	#print(actions)
	#print(packets)
	if intervals:
		b.write("MODULE C()"+"\n")
		b.write("VAR"+"\n")
		b.write("\t"+"cur:{"+str(intervals[0]))
		for i in range(1,len(intervals)):
		#	print(int(intervals[i]))
			b.write(","+str(intervals[i]))
		b.write("};"+"\n")
		b.write("ASSIGN"+"\n")
		b.write("\t"+"init(cur) :="+str(intervals[0])+";"+"\n")


	m=[]
	for i in range(1,len(r)):
		t=0
		prio[r[i][0]]=(int(r[i][2]))
		if "c0" in r[i][3]:
			t=1		
		b.write("MODULE " + r[i][0])
		b.write("(")
		if t==1:
			b.write("c"+",r"+r[i][0][1]+"1")
		s =[]
		val ={}
		s = r[i][4].split(",")
		flag=0
		for k in range(len(s)):
			if s[k][:6]=="delete": 
				v = s[k][7].lower()
				val[s[k][8]]=0
				if s[k][7:9]!=r[i][0]:
					if flag==0:
						b.write(v+s[k][8])
					else:	
						b.write(","+v+s[k][8])
					flag=1
			if s[k][:3]=="add":
				v = s[k][4].lower()
				val[s[k][5]]=1	
				if s[k][4:6]!=r[i][0]:
					if flag==0:
						b.write(v+s[k][5] )
					else:
						b.write(","+v+s[k][5])
					flag=1	
		m.append(val)	
		b.write(")"+"\n")
		b.write("VAR"+"\n")
		b.write("\t"+"active:boolean;"+"\n")
		b.write("ASSIGN"+"\n")
		if r[i][1]=="true":
			b.write("\t"+"init(active) := TRUE;")
		else:
			b.write("\t"+"init(active):= FALSE;")
		b.write("\n")		
		if val:
			for key,value in val.items():
				if key == list(r[i][0])[1]:
					b.write("\t"+"next(self.active) := case")
					b.write("\n")
					if value==0:
						b.write("\t\t"+"self.active : FALSE;")
					else:
						b.write("\t\t"+"self.active : TRUE;")
					b.write("\n")
					b.write("\t\t"+"TRUE : self.active;")
					b.write("\n")
					b.write("\t\t"+"esac;")
					b.write("\n")
				else:
					b.write("\t"+"next(r"+key+".active) := case")
					b.write("\n")
					if value==0:
						b.write("\t\t"+"self.active : FALSE;")
					else:
						b.write("\t\t"+"self.active : TRUE;")
					b.write("\n")
					b.write("\t\t"+"TRUE : "+"r"+key+".active;")
					b.write("\n")
					b.write("\t\t"+"esac;")
					b.write("\n")
		b.write("\n")
		if t==1:
			b.write("\t"+"next(r"+r[i][0][1]+"1.active) := case")
			b.write("\n")
			b.write("\t\t"+"c.cur = " + str(-(48-ord(r[i][3][ind-2])))+ " : TRUE;")
			b.write("\n")
			b.write("\t\t"+"TRUE : FALSE;")
			b.write("\n")
			b.write("\t\t"+"esac;")
			b.write("\n")
			b.write("\t"+"next(c.cur) := case"+"\n")
			b.write("\t\t"+"self.active & "+"r"+r[i][0][1]+"1.active : " + str(-(48-ord(r[i][3][ind+3])))+";")
			b.write("\n")
			b.write("\t\t"+"TRUE : "+str(-(48-ord(r[i][3][ind-2])))+";")
			b.write("\n")
			b.write("\t\t"+"esac;"+"\n")
			b.write("MODULE " + r[i][0]+"1"+"(c)"+"\n")
			b.write("VAR"+"\n")
			b.write("\t"+"active:boolean;"+"\n")
			b.write("ASSIGN"+"\n")
			b.write("\t"+"init(active) := ")
			if (48-ord(r[i][3][ind-2]))==intervals[0]:
				b.write("TRUE;"+"\n")
			else:
				b.write("FALSE;"+"\n")	
	l=sorted(prio, key=prio.get,reverse=True)
	l1=[]
	for o in range(len(l)):
		l1.append(l[o]+"1")
	#print(l1)
	s=getprop(pop,l,l1,actions,packets)
	ltl=rep(s,bc)
	print(ltl)
	b.write("MODULE main"+"\n")
	b.write("VAR"+"\n")
	h=0
	if intervals:
		h=1
		b.write("\t"+"c : process C();"+"\n")
	for i in range(1,len(r)):
		b.write("\t"+"r"+str(i-1)+" : process "+r[i][0])
		flag=0
		b.write("(")
		if "c0" in r[i][3]:
			flag=1
			b.write("c,r"+r[i][0][1]+"1")
		if m[k]:
			for key,value in m[k].items():
				if key != list(r[i][0])[1]:
					if flag==0:
						b.write("r"+str(key))
					else:
						b.write(","+"r"+str(key))
					flag = flag+1	
		b.write(");"+"\n")
		if "c0" in r[i][3]:
			b.write("\t"+"r"+str(i-1)+"1"+" : process "+r[i][0]+"1(c);"+"\n")
		k=k+1
	b.close()

if __name__ == "__main__":
    main()



			


