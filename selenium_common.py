import selenium
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


from .common import DataClear,check_dir_and_create





def init_database_system_par(system_type,db_session,SystemPar):
        systemPar=None
        if system_type=='Windows':
                systemPar = SystemPar(par_code='chrome_driver', par_desc='Chrome驱动',
                                par_value=r'D:\software\chromedriver.exe', par_type=2)
                db_session.add(systemPar)
                systemPar = SystemPar(par_code='chrome_user-data-dir', par_desc='Chrome用户目录',
                                par_value=r'D:\chrome_user_data_dir', par_type=2)
                db_session.add(systemPar)

        if system_type=='Linux':
                systemPar = SystemPar(par_code='chrome_driver', par_desc='Chrome驱动',
                                par_value=r'/u01/software/chromedriver', par_type=2)
                db_session.add(systemPar)
                systemPar = SystemPar(par_code='chrome_user-data-dir', par_desc='Chrome用户目录',
                                par_value=r'/u01/chrome_user_data_dir', par_type=2)
                db_session.add(systemPar)
        if system_type=='Mac':
                systemPar = SystemPar(par_code='chrome_driver', par_desc='Chrome驱动',
                                par_value=r'‎⁨/Volumes/MacintoshHD/Software/chromedriver', par_type=2)
                db_session.add(systemPar)
                systemPar = SystemPar(par_code='chrome_user-data-dir', par_desc='Chrome用户目录',
                                par_value=r'/Volumes/MacintoshHD/Software/chrome_user_data_dir', par_type=2)
                db_session.add(systemPar)
        #测试，目录是否存在，如果不存在创建目录
        check_dir_and_create(systemPar.par_value)


def hand_scroll(driver):
        t=random.uniform(500, 10000)
        js_scroll = "var q=document.documentElement.scrollTop="+str(t)  # documentElement表示获取根节点元素
        driver.execute_script(js_scroll)


def hand_wait(start,end):
        t=random.uniform(start, end)
        time.sleep(t)
def hand_type_word_wait():
        hand_wait(0.1,1)
def hand_browse_webpage_wait():
        hand_wait(5,20)
def hand_focus_move_wait():
        hand_wait(1,3)


def hand_send_keys(input_control,input_text):
    for word in input_text:
        hand_type_word_wait()
        input_control.send_keys(word)

def hand_browser_get(browser,url):

        browser.get(url)



def hand_click(button):
        button.click()


def hand_find_date_element(webdriver,byMethod,value):
        element_text=hand_find_text_element(webdriver,byMethod,value)
        if element_text==None:
                return None
        else:
                return DataClear().text_to_date(element_text)
        
def hand_find_int_element(webdriver,byMethod,value):
        element_text=hand_find_text_element(webdriver,byMethod,value)
        if element_text==None:
                return None
        else:
                return DataClear().text_to_int(element_text)

def hand_find_text_element(webdriver,byMethod,value):
        element=hand_find_element(webdriver,byMethod,value)
        if element==None:
                return None
        else:
                element_text=element.text if (element.text!='-' and element.text!='暂无信息') else None
                
                return element_text

def hand_find_element(webdriver,byMethod,value):
        element=None
        try:
                element=webdriver.find_element(byMethod,value)
        except selenium.common.exceptions.NoSuchElementException as e:
                pass
        return element

# 智能等待10s之后获取元素，获取的是多个元素
def hand_find_list_elements_by_list_pars(webdriver,list_pars):
        all_elements=[]
        for par in list_pars:
                #print(par)
                try:
                        elements = WebDriverWait(webdriver, 10).until(EC.presence_of_all_elements_located((par['method'],par['value'])))
                        all_elements.extend(elements)
                        
                        
                except selenium.common.exceptions.TimeoutException as e:
                        pass
        return all_elements
                

class Sel():
        def __init__(self, _type,db_session,SystemPar):
                if _type=='Chrome':
                        #为Chrome浏览器初始化，从数据库获取参数
                        db_chrome_driver=db_session.query(SystemPar).filter(SystemPar.par_code=='chrome_driver').one()
                        chrome_driver=db_chrome_driver.par_value
                        driverOptions= webdriver.ChromeOptions()
                        db_chrome_user_data_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='chrome_user-data-dir').one()
                        chrome_user_data_dir=db_chrome_user_data_dir.par_value
                        driverOptions.add_argument(r"user-data-dir="+chrome_user_data_dir)
                        self.driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=driverOptions)
                        #hand_browser_get(self.driver,"https://www.tianyancha.com/")
        
        def closeWindow(self):
                self.driver.quit()

        #https://www.runoob.com/w3cnote/python-func-decorators.html
        def handle_open_page(url,func):                
                early_handles = self.driver.window_handles
                #记录当前的windows句柄
                current_window_handle=self.driver.current_window_handle

                
                self.driver.execute_script('window.open("'+url+'");')
                #新的句柄集合
                
                later_handles = self.driver.window_handles
                new_handle=None
                for handle in later_handles:
                        if handle not in early_handles:
                                new_handle=handle
                self.driver.switch_to.window(new_handle)
                hand_browse_webpage_wait()
                hand_scroll(self.driver)
                hand_browse_webpage_wait()
                func()
                self.driver.close()
                self.driver.switch_to.window(current_window_handle)
                