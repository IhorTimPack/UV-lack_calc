import re
st = "ababababababa"
t = r"a[ab]+a"
r = re.match(t, st)
print(re.match(t, st))
print(r)
print(r[0])
