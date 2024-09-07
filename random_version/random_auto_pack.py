import os
import subprocess
import shutil
import zipfile
import re
# 1. 用户输入一串数字
user_input = input("请输入学号:")


# 打开 a.py 并设置变量 x 的值
with open("SCRIPT/random_ver1.py", "r", encoding="utf-8") as file:
    a_py_content = file.read()

# 设置新的 x 值
pattern = re.compile(r'(user_name\s*=\s*")(.*?)"', re.DOTALL)
a_py_content = pattern.sub(rf'user_name="{user_input}"', a_py_content)
#a_py_content = a_py_content.replace('user_name=""', f'user_name = "{user_input}"')

# 写回 a.py
with open("SCRIPT/random_ver1.py", "w", encoding="utf-8") as file:
    file.write(a_py_content)


# 3. PyInstaller 打包 spider.py 脚本为 spider.exe
subprocess.run(["pyinstaller", "--onefile", "--icon=SCRIPT/stiei.ico","SCRIPT/random_ver1.py"])
# 4. 打包 geckodriver.exe, firefox.exe, spider.exe 为 spider.rar
with zipfile.ZipFile(f"SUCCESS_PACK\{user_input}stiei_spider.rar", "w") as zipf:
    for file_name in ["SCRIPT/geckodriver.exe", "SCRIPT/Firefox Setup 121.0.1.exe", "dist/random_ver1.exe"]:
        if os.path.exists(file_name):
            zipf.write(file_name, os.path.basename(file_name))

# 清理临时文件
shutil.rmtree("dist")
shutil.rmtree("build")
os.remove("random_ver1.spec")


print("打包完成。")
