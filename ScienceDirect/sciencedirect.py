from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from ScienceDirect.notify import show_notification, ChangeVPN
import undetected_chromedriver as browser
#from webdriver_manager.chrome import ChromeDriverManager
import time
import os,subprocess
import pandas as pd
import csv
from datetime import date
import logging
import shutil
from selenium.common.exceptions import NoSuchElementException, TimeoutException, SessionNotCreatedException
#from fake_useragent import UserAgent

# Specify the file name and path relative to the script directory
file_name = 'scraper_log_file.log'
#file_path = os.path.join(script_dir, file_name)
#print(file_path)    
with open(file_name, 'w') as file:
    print("file created for logs")
    pass    
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
    filename=file_name)

logger = logging.getLogger(__name__)
show_notification("SciDir_crawler Notification", "ScienceDirect crawler has created a folder Scraper_Logs",
                  timeout=10)




class ScienceDirect(browser.Chrome):
    
    def __init__(self,
                keep_alive=True):
        
        

        chrome_options = browser.ChromeOptions()
        chrome_options.add_argument("--disable-lazy-loading")
        chrome_options.add_argument("--disable-print-preview")
        #chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-stack-profiler")
        chrome_options.add_argument("--disable-background-networking")
        #chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("excludeSwitches=enable-automation")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-popup-blocking")
        #chrome_options.add_experimental_option("debuggerAddress","localhost:51375")
        chrome_options.add_argument("--remote-allow-origins=*")
        # Add any desired options here
        # For example, to run Chrome in headless mode:
       
        
        #chrome_options.add_argument("--headless=new")
        
        #self.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        script_dir = os.path.dirname(os.path.abspath(__file__)).replace("\ScienceDirect",'',-1)
        print(f"Current Working Dir: {script_dir}")
        chromeProfile = "\Includes\Data_files\data\Chrome_profile"
        browser_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        print(f"Browser Executable Path is : {os.path.join(script_dir,browser_path)}")
        super(ScienceDirect, self).__init__(options=chrome_options,keep_alive=True)#user_data_dir= os.getcwd()+chromeProfile), version_main=114,
        self.keep_alive = keep_alive
        #self.implicitly_wait(15)
        self.maximize_window()
        
        
        
        
               
        
        
    def __exit__(self,exc_type , exc_val, exc_to):
        if not self.keep_alive:
            print(f" Check for processes still running ? {self.service.assert_process_still_running()}")
            print(f"Service.process.pid for chrome bot is : {self.service.process.pid}")
            self.stop_client()
            self.service._terminate_process()
            #subprocess.run(['kill',f'{self.service.process.pid}'],shell=True)
            process = subprocess.Popen(["powershell","Stop-Process", f"-Id {self.browser_pid},{self.service.process.pid}"],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
            result = process.communicate()[0]
            print(result)
            time.sleep(2)
            self.quit()
        
    def land_first_page(self,url=None):
        #self.execute_script("window.open('');")
        #self.switch_to.window(self.window_handles[0])
        self.get('https://www.sciencedirect.com/') #user/login?targetURL=%2F&from=globalheader
        """self.find_element(By.ID, "qs").send_keys("Cancer Research")
        self.find_element(By.XPATH,"//button/span[@class='button-text']").click()"""
        
        
        
    """def ClickCapture(self):
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://challenges.cloudflare.com/cdn-cgi/challenge-platform']")))
        time.sleep(10)
        WebDriverWait(self, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ctp-label']"))).click()
        checkbox = self.find_element(By.CSS_SELECTOR, value = 'label[class = "ctp-checkbox-label"]')
        print("Captcha CheckBox Element is visible? " + str(checkbox.is_displayed()))
        #driver.implicitly_wait(50)
        checkbox.click()"""
        
        
    def sign_in(self, username=None, pswrd = None):
        try:
            email_input = WebDriverWait(self, 20).until(EC.visibility_of_element_located((By.ID, 'bdd-email')))
            #email_input = self.find_element(By.NAME, value = "pf.username")
            
            email_input.send_keys(f"{username}")
            button_login = self.find_element(By.ID, value = "bdd-elsPrimaryBtn")
            button_login.click()
            pwd_input = WebDriverWait(self,20).until(EC.visibility_of_element_located((By.ID, 'bdd-password')))
            
            
            #pwd_input = self.find_element(By.ID, value = "bdd-password")
            pwd_input.send_keys(f"{pswrd}")
            Sign_IN = self.find_element(By.ID, value = "bdd-elsPrimaryBtn")
            Sign_IN.click()
            
        except Exception as e:
            logger.exception("Sign In Exceptions: %s", str(e))
            show_notification("ScienceDirect Scraper Error",
                              "Login Error occured in ScienceDirect, Please check Scraper_Logs Folder!",
                              timeout=10
                              )
        
            
            
    def GetNextLinks(self, keyword_input=None, year = None,offset = None,url = None):
        
        try :
                    
            #print("Enter the keywords you want to search")
            #keyword_input = keyword_input
            keyword_edit = keyword_input
            print(keyword_edit)
            query = keyword_edit.replace(" ","%20",-1)
            print(query)
            #print("Which Affiliations you want to search, e.g. Harvard University, National Institute of Singapore")
            
            
            date_range = year
            
            year = str(date_range)
            
            #print("Enter the Offset number (multiple of 100 e.g. 0, 1000 or 1200) as starting point for the search")
            #offset = int(offset)
            if offset == None:
                offset = 0
            else: 
                offset = offset        
            show_pages = 100
            if url == None:
                #self.execute_script("window.open('');")
                #self.switch_to.window(self.window_handles[0])
                
                self.get(f"https://www.sciencedirect.com/search?qs={query}&show={show_pages}&date={year}&offset={offset}")
            ###########################################
            #Changes########
            else:
                #self.execute_script("window.open('');")
                #self.switch_to.window(self.window_handles[0])
                self.get(url)
            
            try:
                self.find_element(By.CLASS_NAME, 'error-zero-results')
                zer0_res = True
            except NoSuchElementException:
                zer0_res = False

            try:
                self.find_element(By.CLASS_NAME, 'error-400')
                error_400 = True
            except NoSuchElementException:
                error_400 = False

            try:
                Institute_Login = self.find_element(By.ID, 'bdd-els-close').is_displayed()
            except NoSuchElementException:
                Institute_Login = False

            if zer0_res or error_400:
                return None
            elif Institute_Login:
                self.find_element(By.ID, 'bdd-els-close').click()
                pages_range = self.find_element(By.XPATH, "*//ol[@id='srp-pagination']//li[contains(text(),'Page ')]").text
                ########################################################
                #Additionally The program will extract the available FacetItems and Values to store them in a variable
                #######################################################
                #facetitems = self.Extract_FacetItems()
            else:
                pages_range = self.find_element(By.XPATH, "*//ol[@id='srp-pagination']//li[contains(text(),'Page ')]").text
                #facetitems = self.Extract_FacetItems()

            return pages_range
           
        except Exception as e:
            logger.debug("An Error occured: %s",str(e))
            show_notification("ScienceDirect Scraper Error",
                              "Getting Next Page Link Error, Please check Scraper_Logs Folder!",
                              timeout=10
                              )
            
            pass
    ########################################################
    #Additionally The program will extract the available FacetItems and Values to store them in a variable
    #######################################################
    def Extract_FacetItems(self):#query,show_pages,year,offset
        article_list, subject_list, publication_list = [],[],[]
        #self.get(f"https://www.sciencedirect.com/search?qs={query}&show={show_pages}&date={year}&offset={offset}")
        time.sleep(3)
        total_res = self.find_element(By.CLASS_NAME, "search-body-results-text").text
        total_results = int(total_res.split(" ")[0].replace(",","",-1))
        print(f"Total results : {total_results}")
        if total_results < 1000:
            return None
        self.find_element(By.XPATH,"*//div[@class='FacetItem']//fieldset//ol/li/button[@data-aa-button='srp-show-more-articleTypes-facet']").click()
        article_types = self.find_elements(By.XPATH,"*//div[@class='FacetItem']//fieldset//ol/li/div/label/input[contains(@id,'articleTypes-')]") 
        for article in article_types:
            article_list.append(article.get_attribute("id").split("-")) 
        pub_btn = WebDriverWait(self,10).until(EC.element_to_be_clickable((By.XPATH,"*//div[@class='FacetItem']//fieldset//ol/li/button[@data-aa-button='srp-show-more-publicationTitles-facet']")))
        self.find_element(By.XPATH,"*//div[@class='FacetItem']//fieldset//ol/li/button[@data-aa-button='srp-show-more-publicationTitles-facet']").click()  
        pub_types = self.find_elements(By.XPATH, "*//div[@class='FacetItem']//fieldset//ol/li/div/label/input[contains(@id,'publicationTitles-')]")
        for pub in pub_types:
            publication_list.append(pub.get_attribute("id").split("-"))
        time.sleep(3)
        self.find_element(By.XPATH, "//div[@class='FacetItem']//fieldset//ol/li/button[@data-aa-button='srp-show-more-subjectAreas-facet']").click()
        subject_types = self.find_elements(By.XPATH, "*//div[@class='FacetItem']//fieldset//ol/li/div/label/input[contains(@id,'subjectAreas-')]")
        for sub in subject_types:
            
            subject_list.append(sub.get_attribute("id").split("-"))
        print("#"*10)
        print(publication_list)
        print("#"*10)
        print(subject_list)
        print(article_list)
        time.sleep(2)
        return [publication_list,subject_list,article_list]  
    
         
    def initial_page(self,page_text):
            self.pageText = page_text
            if self.pageText == None:
                return None
            
            index_of = self.pageText.index('of')
            
            initial_page = self.pageText[index_of - 3:7]
            print(f"########## {initial_page} #########")
            #initial_page = initial_page.replace(" ","")
            initial_page = int(initial_page)
            print(f"Initial page Number is {initial_page}")
            return initial_page
            
    def TotalPages(self,Pages_Range):
            #self.implicitly_wait(3)
            if Pages_Range == None:
                return None
            
            index_of = Pages_Range.index('of')
            pages = Pages_Range[index_of + 3:]
            total_pages = int(pages)
            return total_pages
        
    def OffsetValue(self,total_pages):
            pagination = 10
            offset = None
            if total_pages == None:
                return None
            elif total_pages%pagination == 0:
                
                a = int(total_pages/pagination)
                        
                offset = [1000* i for i in range(a)]
                print(f"The offset list is made for scraping with offset = {offset}")
                return offset
            else :
                a = int(total_pages/pagination) + 1
                offset = [1000 * i for i in range(a) ]
                print(f"The offset list is made for scraping with offset = {offset}")
                
            
                return offset
    #############################################################
    #Changed Code to write article links to csv file instead of storing in list       
    def GetArticleLink(self,keyword_input,year_range,offset,total_pages):
        try: 
            #article_links = []
            pagination = 10
            Next_link = self.GetNextLinks(keyword_input,year_range,offset)
            if Next_link == None:
                return None
            initial_Page = self.initial_page(Next_link)
            Total_pages = self.TotalPages(Next_link)
            pages_left = Total_pages - initial_Page + 1
            
            print(f"Your {keyword_input} results contain {pages_left} pages")
            file = str(keyword_input).replace("\"","",-1)   
            f_headers = ["url", "Title"]
            show_pages = 100
            df_readCSV = f'{file}'+"_"+f'{year_range}'+"_articles_"+f'{initial_Page}.csv'
            df_outCSV = f'{file}'+"_"+f'{year_range}'+"_articles_"+f'{initial_Page}'+'_out.csv'
            if os.path.exists(df_readCSV):
                os.remove(df_readCSV)
            with open(df_readCSV, "a+",encoding="utf-8",newline="") as f:
                csv_writer = csv.DictWriter(f,f_headers)
                csv_writer.writeheader()
                facet_items = self.Extract_FacetItems()
                if facet_items is not None:
                    for items in facet_items:
                            for item in items:
                                print(f"item in [pub_list] is ==> {item}")                            
                                offset = 0    
                                if pages_left < pagination:
                                    print(f"Extracting article links for {Total_pages} pages...")
                                    for p in range(pages_left):
                                        #self.execute_script("window.open('');")
                                        #self.switch_to.window(self.window_handles[0])
                                        #time.sleep(10)
                                        self.get(f"https://www.sciencedirect.com/search?qs={keyword_input}&show={show_pages}&date={year_range}&offset={offset}&{item[0]}={item[1]}&lastSelectedFacet={item[0]}")
                                        try:
                                            self.find_element(By.ID, 'bdd-els-close').click()
                                            
                                            
                                        except Exception as e:
                                            
                                            pass
                                            
                                        finally:
                                            
                                            results = WebDriverWait(self,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"result-list-title-link")))
                                            
                                                
                                            print(f"Page {p+1} contains {len(results)} articles")
                                            for result in results:
                                                    csv_writer.writerow({"url":result.get_attribute("href"), "Title":result.text})
                                                #article_links.append({"url": result.get_attribute("href"), "Title": result.text})
                                            if len(results) < 100:
                                                break
                                        
                                        offset += show_pages
                                        
                                else:
                                    print("Extracting article links for first 10 pages...")
                                    for p in range(pagination):
                                        #self.execute_script("window.open('');")
                                        #self.switch_to.window(self.window_handles[])
                                        #time.sleep(10)
                                        self.get(f"https://www.sciencedirect.com/search?qs={keyword_input}&show={show_pages}&date={year_range}&offset={offset}&{item[0]}={item[1]}&lastSelectedFacet={item[0]}")
                                        
                                        try:
                                            self.find_element(By.ID, 'bdd-els-close').click()
                                        
                                            
                                        except Exception as e:
                                            pass
                                            
                                        finally:
                                            results = WebDriverWait(self,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"result-list-title-link")))
                                                
                                            print(f"Page {p+1} contains {len(results)} articles")
                                                                    
                                            for result in results:
                                                    csv_writer.writerow({"url":result.get_attribute("href"), "Title":result.text})
                                                #article_links.append({"url": result.get_attribute("href"), "Title": result.text})
                                            if len(results) < 100:
                                                break
                                            
                                        offset += show_pages
                else:
                    print("Extracting article links for first 10 pages...")
                    for p in range(pagination):
                        #self.execute_script("window.open('');")
                        #self.switch_to.window(self.window_handles[])
                        #time.sleep(10)
                        self.get(f"https://www.sciencedirect.com/search?qs={keyword_input}&show={show_pages}&date={year_range}&offset={offset}")
                        
                        try:
                            self.find_element(By.ID, 'bdd-els-close').click()
                        
                            
                        except Exception as e:
                            pass
                            
                        finally:
                            results = WebDriverWait(self,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"result-list-title-link")))
                                
                            print(f"Page {p+1} contains {len(results)} articles")
                                                    
                            for result in results:
                                    csv_writer.writerow({"url":result.get_attribute("href"), "Title":result.text})
                                #article_links.append({"url": result.get_attribute("href"), "Title": result.text})
                            if len(results) < 100:
                                break
                            
                        offset += show_pages       
            filename = str(keyword_input).replace("\"","",-1)   
            f = open(f'{filename}'+"_"+f'{year_range}'+"_initial_"+f'{initial_Page}.csv', 'w')
            f.close()
            df = pd.read_csv(df_readCSV, sep=",",encoding="utf-8")
            df.drop_duplicates(inplace=True)
            df.to_csv(df_outCSV,lineterminator="\n",sep=",",index=False,columns=["url","Title"])
            ChangeVPN()
            time.sleep(17)
            os.remove(df_readCSV)
            return [keyword_input,initial_Page]

            
        except Exception as e:
            #
            logger.error("An Error occured: %s",str(e))
            show_notification("Science Scraper Error",
                              "An Error occured while scraping links for articles from ScienceDirect, Please check Scraper_Logs Folder!",
                              timeout=10
                              )
            
    
    def ClickEnvelops(self,keywords,year_range,Urls,Titles):
            list_of_dict = []
            try:
                banners = WebDriverWait(self,5).until(EC.presence_of_element_located((By.ID, 'banner')))
                
                show_more = WebDriverWait(banners,1).until(EC.element_to_be_clickable((By.ID,'show-more-btn')))
                show_more.click()
                envelope_icons = WebDriverWait(self,1).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"icon-envelope")))
                icon_res = True
            except TimeoutException:
                icon_res = False
                pass
                

            if icon_res:
                #filename = str(keywords).replace("\"","",-1)
                    for icon in envelope_icons:
                        try:
                            icon.click()
                            self.implicitly_wait(2)
                            #workspace_div = self.find_element(By.CLASS_NAME, "Workspace")
                            author_info = WebDriverWait(self,2).until(EC.visibility_of_element_located((By.ID, 'side-panel-author')))      #workspace-author

                            email = author_info.find_element(By.XPATH, "//div[@class = 'e-address']//a")
                            print(email.text)
                            authors = author_info.find_element(By.CLASS_NAME, "given-name")

                            print(authors.text)

                            surnames = author_info.find_element(By.CLASS_NAME, "surname")
                            authors_name = authors.text + " " + surnames.text
                            list_of_dict.append({"Run_Date":date.today(), "Keyword_input":keywords,
                                                 "Year_Range":year_range,"URLs":Urls,"emails":email.text, "names":authors_name})
                            
                        except Exception as e:
                            logger.error("An error occured: %s",str(e))
                            """show_notification("Science Scraper Error",
                              "No Author information found while scraping links for articles from ScienceDirect, Please check Scraper_Logs Folder!",
                              timeout=10
                              )"""
                            
                            pass
            else:
                    pass
            for row in list_of_dict:
                for key in row:
                    if row[key] =='':
                        row[key] = "None"
            
            return list_of_dict
        
        
    ###########################################
    #Changed Code to read links from csv file       
    def ExtractEmails(self,keywords,dates,offset_values,total_pages):
        
        links = self.GetArticleLink(keywords,dates,offset_values,total_pages)
        if links == None:
            return None
        filename = str(keywords).replace("\"","",-1)
        headers = ["Run_Date","Keyword_input","Year_Range","URLs","emails", "names"]
        fileread_path = f'{filename}'+"_"+f'{dates}'+"_articles_"+f'{links[1]}_out.csv'
        write_emails_file = f'{filename}'+"_"+f'{dates}'+"_initial_"+f'{links[1]}.csv'
        
        with open(write_emails_file, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            with open(fileread_path, "r", encoding="utf-8", newline="") as read_file:
                csv_reader = csv.DictReader(read_file)
                                
                for count, link in enumerate(csv_reader):
                    print("#^^#"*10)
                    print(count)
                    print("#^^#"*10)
                    print(f"Opening link --> {link['url']}")
                    print(link['Title'])
                    self.get(link['url'])
                    try:
                        WebDriverWait(self, 2).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://challenges.cloudflare.com/cdn-cgi/challenge-platform']")))
                        #time.sleep(10)
                        #WebDriverWait(self, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ctp-label']"))).click()
                        checkbox = self.find_element(By.CSS_SELECTOR, value = 'label[class = "ctp-checkbox-label"]')
                        print("Captcha CheckBox Element is visible? " + str(checkbox.is_displayed()))
                        if checkbox.is_displayed():
                                                    
                            show_notification("Science Scraper Encountered A CheckBox",
                                "A CheckBox Verification is appeared while scraping ScienceDirect, Please refresh the page while VPN changes your location to continue...",
                                timeout=30
                                )
                            """print("The Captcha Box appeared during Scraping, Please click checkbox and then enter 1 ")
                            input("Enter 1 : ")"""
                            ChangeVPN()             
                            time.sleep(10)
                            
                    except (NoSuchElementException,TimeoutException):
                        
                        pass
                    except SessionNotCreatedException:
                        self.reconnect(timeout=60)
                        self.ExtractEmails(self,keywords,dates,offset_values,total_pages)   
                    finally:
                        results = self.ClickEnvelops(keywords,dates,link['url'],link['Title'])
                        writer.writerows(results)
        
        #os.remove(fileread_path)                    
                