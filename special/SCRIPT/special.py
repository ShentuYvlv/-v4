from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,pytz,sys
from datetime import datetime

# 设置浏览器驱动路径
gecko_driver_path = "geckodriver.exe"

# 创建Firefox浏览器实例
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = False  # 如果你想在可见的浏览器窗口中运行，将此选项设置为 True
firefox_options.add_argument("--incognito")  # 将这行代码注释掉或设置为 False
firefox_service = webdriver.FirefoxService(executable_path=gecko_driver_path)

# 打开网页
url = 'https://os.stiei.edu.cn/auth/login'

attempts = 0
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
def click_link_by_id(browser, link_ids):
    # 获取当前窗口句柄
    original_window_handle = browser.current_window_handle

    for link_id in link_ids:
        try:
            script = 'var element = document.querySelector(".lessonListOperator"); ' \
                     'element.setAttribute("lessonId", arguments[0]); ' \
                     'electCourseTable.tip.submit({lessonId: arguments[0], ele: element, type: jQuery(element).attr("operator")});'

            browser.execute_script(script, link_id)
        except Exception as e:
            print(f"[❌]课程 {dict_lesson.get(link_id)} 未找到，可能已经选择 跳过")
            continue
        try:
            alert = WebDriverWait(browser, 1).until(EC.alert_is_present())
            if alert.text == "是否提交?":
                alert.accept()
                submit_close = WebDriverWait(browser,1).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="cboxClose"]'))
                )
                submit_close.click()
                print(f"[√]课程{dict_lesson.get(link_id)}已经抢课成功")
            elif "上限人数已满，请稍后再试" in alert.text or "你已经选过" in alert.text or "以下课程冲突" in alert.text:
                print(f"[❌]课程{dict_lesson.get(link_id)}抢课失败 原因{alert.text}")
                alert.accept()
        except Exception as e:
            print(f"[❌]没有找到课程{dict_lesson.get(link_id)}可能你已选过此课程")
            continue
        # 切回原来的窗口
        browser.switch_to.window(original_window_handle)
        time.sleep(0.2)
    print("抢课结束 请刷新页面查看已选课程")


def login_and_navigate(url, user_name, password,browser,user_input_time):
    attempts = 0

    while attempts<100:
        try:
            browser.get(url)

            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'account'))
            )

            username_input = browser.find_element('id', 'account')
            password_input = browser.find_element('id', 'password')
            username_input.send_keys(user_name)
            password_input.send_keys(password)

            login_button = browser.find_element(By.XPATH,
                                                '/html/body/div/div/div/div/div[1]/div[1]/div[2]/form/div[4]/div/div/span/button')
            login_button.click()  # 点击登陆

            link2 = WebDriverWait(browser, 6).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]'))
            )
            link2.click()           #点击网站入口

            link1 = WebDriverWait(browser, 4).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]'))
            )
            link1.click()       #点击教务系统

            browser.switch_to.window(browser.window_handles[1])
            WebDriverWait(browser, 4).until(
                EC.title_contains("EAMS 3.0.0")
            )

            while True:
                current_time=datetime.now(beijing_tz)
                if current_time >= user_input_time or user_input_time=='':
                    try:
                        browser.get("http://jiaowu.stiei.edu.cn:8080/eams/stdElectCourse.action")
                        initial_handles = browser.window_handles
                        if (user_name[0:4] == "2023"):
                            script = 'window.open("{}", "_blank");'.format(
                                '/eams/stdElectCourse!defaultPage.action?electionProfile.id=1438')
                        else:
                            script = 'window.open("{}", "_blank");'.format(
                                '/eams/stdElectCourse!defaultPage.action?electionProfile.id=1434')
                        browser.execute_script(script)
                        WebDriverWait(browser, 4).until(
                            EC.new_window_is_opened(initial_handles)
                        )
                        browser.switch_to.window(browser.window_handles[2])  # Assuming there are only two windows (index 0 and 1)
                        WebDriverWait(browser,6).until(
                            EC.element_to_be_clickable((By.XPATH,"/html/body/div[12]/div[2]/form/div/table/tbody/tr[1]/td[10]/a"))
                        )
                        break
                    except:
                        attempts+=1
                        print(f"进入选课页面失败 第{attempts}次重试")
                        continue
                else:
                    time_until_execution = user_input_time - current_time
                    print("等待执行时间，剩余时间：", time_until_execution)

                    # 每隔一段时间检查一次
                    time.sleep(2)  # 暂停 60 秒，可以根据需要调整

            break  # 登录成功，退出循环
        except Exception as e:
            print("密码错误 请重新启动程序")
            browser.quit()
            sys.exit()

user_name="5645"
password="123"
select_lesson=[]
print(f"用户{user_name}-密码{password}")
if user_name !="":
    beijing_tz = pytz.timezone('Asia/Shanghai')
    print("时间格式24小时制 年份默认2024。以1月20号10点为例：1-20-10-0")
    user_input_time_str = input("请输入执行时间（24小时制）（格式：月份-日期-小时-分钟）: ")
    if not user_input_time_str:
        user_input_time = datetime.now(beijing_tz)
    else:
        # 将用户输入的时间字符串转换为 datetime 对象，默认年份为 2024
        user_input_time = beijing_tz.localize(datetime.strptime("2024-" + user_input_time_str, "%Y-%m-%d-%H-%M"))
    browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
    login_and_navigate(url,user_name,password,browser,user_input_time)
    click_link_by_id(browser, select_lesson)


else:
    print("请绑定账号")
    exit(0)



