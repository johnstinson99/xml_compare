import re
import sys

regex = re.compile("\sAND\s", flags=re.IGNORECASE)
result = re.sub(regex, ' & ', 'Baked Beans And Spam')
print(result)

regex = re.compile("test", flags=re.IGNORECASE)
result = re.sub(regex, ' & ', 'test_20151030_1a.xml')
print(result)

print(["a", "b"] == ["a", "b"])

list = ["A", "B"]
result = ["D"].append(list)
print(str(result))
filename = "aaa.bbb"
print([filename])

print(sys.path[0])