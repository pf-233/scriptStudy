print("asga");
str = "123456"
print(str[:-1]);
print(str[-5:]);
print("this " "is " "string");
import keyword;
print(keyword.kwlist)
# input("\n\n按下 enter 键后退出。")
import sys; x = 'runoob'; sys.stdout.write(x + '\n')


from bangumi import readConfig;
from bangumi import movePath;

savePath = readConfig("savePath.json")
movePath = savePath["savePath"]
movePath(savePath)
