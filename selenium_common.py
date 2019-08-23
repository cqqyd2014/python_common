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
                                par_value='/Volumes/MacintoshHD/Software/chromedriver', par_type=2)
                db_session.add(systemPar)
                systemPar = SystemPar(par_code='chrome_user-data-dir', par_desc='Chrome用户目录',
                                par_value='/Volumes/MacintoshHD/Software/chrome_user_data_dir', par_type=2)
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
        hand_wait(2,5)
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

def hand_find_float_element(webdriver,byMethod,value):
        element_text=hand_find_text_element(webdriver,byMethod,value)
        if element_text==None:
                return None
        else:
                return DataClear().text_to_float(element_text)

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

def find_element_by_xpath(root,value):
        element=None
        try:
                element=root.find_element_by_xpath(value)
        except selenium.common.exceptions.NoSuchElementException as e:
                print("find_element_by_xpath抓取对象超时,值"+str(value))
        return element

def find_elements_by_xpath(root,value):
        elements=None
        try:
                elements=root.find_elements_by_xpath(value)
        except selenium.common.exceptions.NoSuchElementException as e:
                print("find_elements_by_xpath抓取对象超时,值"+str(value))
        return elements

def hand_find_elements(webdriver,byMethod,value):
        elements=None
        try:
                locator = (byMethod,value)
                elements=WebDriverWait(webdriver,10).until(EC.presence_of_all_elements_located(locator))
        except selenium.common.exceptions.TimeoutException as e:
                print('hand_find_element抓取对象超时,方法'+str(byMethod)+',值'+str(value))
        return elements

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
                
'''
expected_conditions是selenium的一个模块，其中包含一系列可用于判断的条件：
 
selenium.webdriver.support.expected_conditions（模块）
 
这两个条件类验证title，验证传入的参数title是否等于或包含于driver.title
title_is
title_contains
 
这两个人条件验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw')
顾名思义，一个只要一个符合条件的元素加载出来就通过；另一个必须所有符合条件的元素都加载出来才行
presence_of_element_located
presence_of_all_elements_located
 
这三个条件验证元素是否可见，前两个传入参数是元组类型的locator，第三个传入WebElement
第一个和第三个其实质是一样的
visibility_of_element_located
invisibility_of_element_located
visibility_of
 
这两个人条件判断某段文本是否出现在某元素中，一个判断元素的text，一个判断元素的value
text_to_be_present_in_element
text_to_be_present_in_element_value
 
这个条件判断frame是否可切入，可传入locator元组或者直接传入定位方式：id、name、index或WebElement
frame_to_be_available_and_switch_to_it
 
这个条件判断是否有alert出现
alert_is_present
 
这个条件判断元素是否可点击，传入locator
element_to_be_clickable
 
这四个条件判断元素是否被选中，第一个条件传入WebElement对象，第二个传入locator元组
第三个传入WebElement对象以及状态，相等返回True，否则返回False
第四个传入locator以及状态，相等返回True，否则返回False
element_to_be_selected
element_located_to_be_selected
element_selection_state_to_be
element_located_selection_state_to_be
 
最后一个条件判断一个元素是否仍在DOM中，传入WebElement对象，可以判断页面是否刷新了
staleness_of
'''
class Sel():




        def __init__(self, _type,db_session,SystemPar,proxy_http_server):
                if _type=='Chrome':
                        #为Chrome浏览器初始化，从数据库获取参数
                        db_chrome_driver=db_session.query(SystemPar).filter(SystemPar.par_code=='chrome_driver').one()
                        chrome_driver=db_chrome_driver.par_value
                        driverOptions= webdriver.ChromeOptions()
                        db_chrome_user_data_dir=db_session.query(SystemPar).filter(SystemPar.par_code=='chrome_user-data-dir').one()
                        chrome_user_data_dir=db_chrome_user_data_dir.par_value
                        driverOptions.add_argument(r"user-data-dir="+chrome_user_data_dir)
                        
                        if proxy_http_server!=None:
                                driverOptions.add_argument("--proxy-server=http://"+proxy_http_server)
                        self.driver = webdriver.Chrome(executable_path=chrome_driver,options=driverOptions)
                        #hand_browser_get(self.driver,"https://www.tianyancha.com/")
        
        def closeWindow(self):
                self.driver.quit()

        def getHtmlSource(self,url):
                self.driver.get(url)
                return self.driver.page_source

        def handle_open_page(func):
                def _decorate(self,url,db_session,*args,**kwargs):
                        early_handles = self.driver.window_handles


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
                        func(self,url,db_session,*args,**kwargs)
                        self.driver.close()
                        self.driver.switch_to.window(current_window_handle)
                return _decorate
                