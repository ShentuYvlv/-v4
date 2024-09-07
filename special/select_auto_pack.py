import os
import subprocess
import shutil
import sys
import zipfile
import re
dict_lesson = {
    103165: "《共产党宣言》导读（网络课程）  通识",
    103157: "《论语》与儒家思想  通识",
    103149: "上海历史文化漫谈  艺术",
    103192: "上海历史文化漫谈  艺术",
    103150: "上海历史文化漫谈  艺术",
    103173: "中国先秦哲学智慧  艺术",
    103135: "中国古建筑欣赏与设计（网络课程）   艺术",
    103131: "中国流行音乐发展简史  通识",
    103189: "中国流行音乐发展简史  通识",
    103159: "中国道路的经济解释（网络课程）  通识",
    103125: "中国音乐鉴赏   艺术",
    103124: "中国音乐鉴赏   艺术",
    103126: "中国音乐鉴赏   艺术",
    103148: "信息检索  通识",
    103181: "信息检索  通识",
    103190: "健身塑型  通识",
    103191: "健身塑型  通识",
    103137: "创新工程实践  通识",
    103167: "劳动合同法理论与实务  通识",
    103166: "劳动合同法理论与实务  通识",
    103175: "匠心中国  通识",
    103180: "博弈论与生活  通识",
    103146: "博弈论与生活  通识",
    103158: "历史大转折中的上海  通识",
    103161: "古典诗词鉴赏（网络课程）  通识",
    103183: "合唱艺术与实践  通识",
    103162: "国学智慧（网络课程）  通识",
    103185: "多元微积分  通识",
    103184: "多元微积分  通识",
    103134: "宋崇导演教你拍摄微电影（网络课程）   艺术",
    103160: "带您走进西藏（网络课程）  通识",
    103194: "思维与创新  通识",
    103193: "思维与创新  通识",
    103142: "旅游地理  通识",
    103179: "旅游地理  通识",
    103163: "星海求知：天文学的奥秘（网络课程）  通识",
    103186: "概率论与数理统计  通识",
    103187: "概率论与数理统计  通识",
    103172: "法律与社会  通识",
    103153: "社会学概论  通识",
    103144: "管理学  通识",
    103145: "管理学  通识",
    103196: "足球  通识",
    103177: "篮球  通识",
    103147: "篮球  通识",
    103122: "素描   艺术",
    103121: "素描   艺术",
    103171: "素描   艺术",
    103195: "经典心理学效应分析  通识",
    103178: "经典音乐剧鉴赏  艺术",
    103132: "经典音乐剧鉴赏  艺术",
    103136: "艺术导论（网络课程）   艺术",
    103138: "英语写作及赏析  通识",
    103141: "英语词汇识记与应用  通识",
    103140: "英语词汇识记与应用  通识",
    103123: "西方音乐名作赏析  艺术",
    103133: "设计与人文：当代公共艺术（网络课程）   艺术",
    103188: "运动营养学基础  通识",
    103164: "追寻幸福：中国伦理史视角（网络课程）  通识",
    103129: "音乐理论基础   艺术",
    103130: "音乐理论基础   艺术",
    103128: "音乐理论基础   艺术"
}
# 1. 用户输入一串数字
user_input = input("请输入学号:")
password_input=input("输入密码:")
result_list=[]
while True:
    less_select=input("输入选择课程id后两位(以空格分开):")
    numbers_str = less_select.split()
    # 添加前缀1031并转为int格式
    for num_str in numbers_str:
        prefixed_num = int("1031" + num_str)
        result_list.append(prefixed_num)
        print(f"你选择的id:{prefixed_num} 对应的课程是{dict_lesson.get(prefixed_num)}")

    ensure=input("是否确认（确认直接回车） 输入n或者N可重新输入id:" or None)
    if ensure =="n" or ensure=="N":
        continue
    else:
        break

# 打开 a.py 并设置变量 x 的值
with open("SCRIPT/special.py", "r", encoding="utf-8") as file:
    a_py_content = file.read()

# 设置新的 学号 值
pattern = re.compile(r'(user_name\s*=\s*")(.*?)"', re.DOTALL)
a_py_content = pattern.sub(rf'user_name="{user_input}"', a_py_content)

#设置新的密码

pattern_pwd = re.compile(r'(password\s*=\s*")(.*?)"', re.DOTALL)
a_py_content = pattern_pwd.sub(rf'password="{password_input}"', a_py_content)



#设置选择id列表
pattern_select_lesson = re.compile(r'(select_lesson\s*=\s*)\[.*?\]', re.DOTALL)
a_py_content = pattern_select_lesson.sub(rf'select_lesson={result_list}', a_py_content)

# 写回 a.py
with open("SCRIPT/special.py", "w", encoding="utf-8") as file:
    file.write(a_py_content)



# 3. PyInstaller 打包 spider.py 脚本为 spider.exe
subprocess.run(["pyinstaller", "--onefile", "--icon=SCRIPT/stiei.ico","SCRIPT/special.py"])
# 4. 打包 geckodriver.exe, firefox.exe, spider.exe 为 spider.rar
with zipfile.ZipFile(f"SUCCESS_PACK\{user_input}stiei_spider.rar", "w") as zipf:
    for file_name in ["SCRIPT/geckodriver.exe", "SCRIPT/Firefox Setup 121.0.1.exe", "dist/special.exe"]:
        if os.path.exists(file_name):
            zipf.write(file_name, os.path.basename(file_name))

# 清理临时文件
shutil.rmtree("dist")
shutil.rmtree("build")
os.remove("special.spec")


print("打包完成。")
