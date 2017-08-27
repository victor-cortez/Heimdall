import joblib
x = list(range(10))
joblib.dump(x,"x.txt")
n = joblib.load("x.txt")
print(n)