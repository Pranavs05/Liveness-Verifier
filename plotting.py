import matplotlib.pyplot as plt
x1 = [100,200,250,300,500,700]
x2 = [100,200,250,300]
x3 = [50,75,100,200,250,300]
port = [0.05,0.08,0.12,0.12,0.23,0.41]
Firewall = [0.12,1.07,10.75,24.72]
Ftp = [0.06,0.14,0.39,20.38,150.3,202.6]
plt.plot(x1,port,label = 'portknocking')
plt.plot(x2,Firewall, label ='Firewall')
plt.plot(x3,Ftp , label ='Ftp')
plt.xlabel('Table size')
plt.ylabel('Time(s)')
plt.legend()
plt.show()