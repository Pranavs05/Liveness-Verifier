# Liveness-Verifier



The verifier converts network tables to LTL file in the .smv format , which can then be fed to verification model checker NUSMV and generates the model. It also provides atomic proposition for properties in boolean formulaes , these atomic propositions are combined to generate a "boolean : property which is then verified against the network model in NUSMV . NUSMV then verifies the peroperty successfully or generates a counter example if the property does not hold .


# Input :

* Network Rules table with priority values and counter  value ranges .
* Property and atomixc propositions . 


Example, for a Firewall the input will be two files firewall.txt which has the rules table and atomic proposition txt:


Follow the below format with spacing for the network table and property files


Firewall.txt --->
``` 

rule active pro match action
R0 false 100 src=I drop() 
R1 false 50 src=I,dst=D drop(),add(R0)
R2 false 50 src=I,dst=F send(),add(R1)
R3 true 40 dst=I,port=2222 send(),add(R2)
R4 true 10 * send()
```
property.txt  --->   Q

```

src=I,dst=E;send(IDPS)
```

Run command to generate NUSMV file and boolean formula for the network proposition:
```shell
 python3 pysmvc.py Firewall.txt property.txt 
 
```



We get the following  Boolean formulae results for the above proposition Q.

**(r0.active=TRUE&TRUE)&r2.active=TRUE&TRUE&FALSE|!(r2.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE**



Now for the property.txt --->   P
```
src=E,dst=I;send(IDPS)     
```

We get the following  Boolean formulae results for the above proposition P.

**!(r1.active=TRUE&TRUE)&!(r3.active=TRUE&TRUE)&r4.active=TRUE&TRUE&FALSE|!(r4.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE**


The whole property in text user input 

```
a stateful firewall at the periphery of an enterprise that allows endpoint E (e.g., as an external host) to talk to I (e.g., as an internal host) only if I send a request to E first. 
```

From property P and Q from above we get the follwing boolean formulae :

(¬p∪q)∧(q→Circle Square p)        

* Circle : User input operation  for next 
* Square : User input operation  for always

(¬p∪q)∧(q→next always p)



The whole property now  in terms of boolean formulae is the obtained as : 

```
"((!(!(r1.active=TRUE&TRUE)&!(r3.active=TRUE&TRUE)&r4.active=TRUE&TRUE&FALSE|!(r4.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)U(!(r0.active=TRUE&TRUE)&r2.active=TRUE&TRUE&FALSE|!(r2.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE))&((!(r0.active=TRUE&TRUE)&r2.active=TRUE&TRUE&FALSE|!(r2.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)->(X(G(!(r1.active=TRUE&TRUE)&!(r3.active=TRUE&TRUE)&r4.active=TRUE&TRUE&FALSE|!(r4.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)))))"

```

The .smv file is loaded , the model is built and then the above property is simulated , to check if it holds in the network or a counter example  exists where the property does not hold.

Command to verify liveness property against NUSMV network model: 

```check_ltlspec -p "((!(!(r1.active=TRUE&TRUE)&!(r3.active=TRUE&TRUE)&r4.active=TRUE&TRUE&FALSE|!(r4.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)U(!(r0.active=TRUE&TRUE)&r2.active=TRUE&TRUE&FALSE|!(r2.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE))&((!(r0.active=TRUE&TRUE)&r2.active=TRUE&TRUE&FALSE|!(r2.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)->(X(G(!(r1.active=TRUE&TRUE)&!(r3.active=TRUE&TRUE)&r4.active=TRUE&TRUE&FALSE|!(r4.active=TRUE&TRUE)&r5.active=TRUE&TRUE&FALSE|!(r5.active=TRUE&TRUE)&TRUE)))))"```


# Author 

Pranav Shirke

