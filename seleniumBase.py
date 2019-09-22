
#
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 创建浏览器对象驱动

driver = webdriver.Chrome()
driver.get("http://www.python.org")
#必须保证网址加载完成 在进行操作
#time.sleep(10)
#得到元素
element = driver.find_element_by_id("passwd-id")
element = driver.find_element_by_name("passwd")
element = driver.find_element_by_xpath("//input[@id='passwd-id']")
element.click()
#交互
# element.send_keys("ABCD")
#element.click()
# element.clear()


"""
    爬取动态网页，内容有JS生成

    创建驱动
        webdriver.Firefox
        webdriver.FirefoxProfile
        webdriver.Chrome
        webdriver.ChromeOptions
        webdriver.Remote
        webdriver.ActionChains
        webdriver.TouchActions
        webdriver.PhantomJS
        ...
        driver = webdriver.Chrome(
                executable_path="chromedriver",    指定驱动位置
                port=0,
                options=None,
                service_args=None,
                desired_capabilities=None,
                service_log_path=None,
                chrome_options=None  配置Chrome浏览器
            )
        获取基本信息 title url。。。
        driver.close()
        查找元素、创建元素
        frame/窗口切换的方法
        cookies 操作的方法
        执行JS代码操作 execute_script /  execute_async_script
            driver.execute_script('return document.title;')
            滚动。。。
        前进、后退、刷新、最大最小化
        alert
        截屏 save_screenshot、....
        ....



    查找元素
        driver. 两个基本方法driver.find_element(By.XPATH, '//button[text()="Some text"]')//driver.find_elements(By.XPATH, '//button')
                find_element_by_id
                find_element_by_name
                find_element_by_xpath
                find_element_by_link_text
                find_element_by_partial_link_text
                find_element_by_tag_name
                find_element_by_class_name
                find_element_by_css_selector

        获取连接 （通过连接文字 得到超链接）
            <a href="continue.html">Continue</a>
            continue_link = driver.find_element_by_link_text('Continue')
            continue_link = driver.find_element_by_partial_link_text('Conti')模糊

        元素方法和操作：from selenium.webdriver.remote.webdriver import WebElement
            标签名、值、get_property、get_attribute
            点击click()/submit()/clear()
            状态is_selected、is_enabled
            子节点查找
            截图
            位置信息
            send_keys("text" | Key) 设置内容

    特殊的Key
        from selenium.webdriver.common.keys import Keys

    事件
        ele.click()/send_keys()  都是简单的
        from selenium.webdriver.common.action_chains import ActionChains
        Chains = ActionChains(driver)
            click(on_element=None) ——单击鼠标左键
            click_and_hold(on_element=None) ——点击鼠标左键，不松开
            context_click(on_element=None) ——点击鼠标右键
            double_click(on_element=None) ——双击鼠标左键
            drag_and_drop(source, target) ——拖拽到某个元素然后松开
            drag_and_drop_by_offset(source, xoffset, yoffset) ——拖拽到某个坐标然后松开
            key_down(value, element=None) ——按下某个键盘上的键
            key_up(value, element=None) ——松开某个键
            move_by_offset(xoffset, yoffset) ——鼠标从当前位置移动到某个坐标
            move_to_element(to_element) ——鼠标移动到某个元素
            move_to_element_with_offset(to_element, xoffset, yoffset) ——移动到距某个元素（左上角坐标）多少距离的位置
            perform() ——必须执行这不操作 事件才会触发
            release(on_element=None) ——在某个元素位置松开鼠标左键
            send_keys(*keys_to_send) ——发送某个键到当前焦点的元素
            send_keys_to_element(element, *keys_to_send) ——发送某个键到指定元素

        Chains.click(ele)==>ele.click()
        ...




补充:
    等待页面完成
        A:time.sleep(10)  简单粗暴  不建议
        B:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC // 判断条件

            try:
                wait = WebDriverWait(driver,10) //等待driver最多10s
                element = wait.until(
                    EC.presence_of_element_located((By.ID, "myDynamicElement")) //等待直到发现元素
                    //presence_of_element_located  该模块下含有很多类似方法
                    自定义函数
                    def AAA(driver):
                        return None /Ele 只要不是None 就当完成等待
                )
            catch():
                pass
            finally:
                pass

    页面对象：
        一种方式 便于重复使用
        http://selenium-python-zh.readthedocs.io/en/latest/page-objects.html

    一部分API
        Alert selenium.webdriver.common.alert.Alert 弹出框
        Keys selenium.webdriver.common.keys.Keys 键盘key
        By   selenium.webdriver.common.by.By  指定查ele 方式
        Utils selenium.webdriver.common.utils 主机,Ip操作类
        UI  selenium.webdriver.support.select.Select  特殊的UI操作类
            下拉选项操作
        COlor selenium.webdriver.support.color.Color 颜色操作

    webdriver.ChromeOptions：为例 来配置Chrome
        option = webdriver.ChromeOptions()
        配置浏览器默认请求 User-Agent
            options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
        语言
            options.add_argument('lang=zh_CN.UTF-8')
        添加crx扩展
            extension_path = '/extension/path'
            options.add_extension(extension_path)
        不加载图片
            prefs = {
                'profile.default_content_setting_values' : {'images' : 2}
            }
            options.add_experimental_option('prefs',prefs)
        设置用户数据
            option.add_argument('--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')

    常见问题：
        http://selenium-python-zh.readthedocs.io/en/latest/faq.html
        //https://github.com/SeleniumHQ/selenium/wiki/Frequently-Asked-Questions
        如何使用ChromeDriver
        如何向下滚动到页面的底部
        如果上传文件到文件上传控件
        如果获取当前窗口的截图
"""