arc = open("times.txt","r")
n = arc.readlines()
content = sorted([float(i.replace("\n","")) for i in n])
arc.close()
med = sum(content)/len(content)
median = content[(len(content) - 1 )// 2]
variance = sum([(i - med) ** 2 for i in content] )/ (len(content) - 1)
dp = variance ** 0.5
print (med)
print(median)
print(variance)
print(dp)