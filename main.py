from ScienceDirect.sciencedirect import ScienceDirect
import ScienceDirect.constants as const
from ScienceDirect.user_registration import Register_User
from ScienceDirect.notify import show_notification, ChangeVPN
import time,os
import csv
import subprocess


import multiprocessing



def read_userdetails():
    with open("user_details.csv", "r", newline="", encoding="utf-8") as f:
        csv_read = csv.DictReader(f)
        username,password = "",""
        for line in csv_read:
            username = line["username"]
            password = line["password"]
        return [username,password]

def startWebChrome(offset,keyword_search, dates_range,total_page):
        with ScienceDirect() as bot:
            bot.land_first_page(url=const.BASE_URL)
            print(f"Session ID for Bot chrom ==> {bot.browser_pid}")
            time.sleep(6)
            #user = read_userdetails()
            #bot.sign_in(username=user[0], pswrd=user[1])
            
                
            #bot.execute_script(f"window.open('about:blank','TAB_{dates_range}');")
            #bot.switch_to.new_window(f"TAB_{dates_range}")
            bot.implicitly_wait(5)
            
            bot.ExtractEmails(keyword_search,dates_range,offset,total_page)
            print(f" Check for processes still running ? {bot.service.assert_process_still_running()}")
            print(f"Service.process.pid for chrome bot is : {bot.service.process.pid}")
            #process = subprocess.Popen(['taskkill', '/f', '/T', f'/pid {bot.browser_pid}'],shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            #process = subprocess.Popen(["powershell","Stop-Process", f"-Id {bot.browser_pid},{bot.service.process.pid}"],shell=True, )
            #result = process.communicate()[0]
            #print(result)              
            ##subprocess.run(['taskkill /f /T /pid',f'{bot.service.process.pid}'],shell=True)
            os.system(r'.\\kill.bat ' + str(bot.browser_pid))            
            time.sleep(2)          
            
            bot.quit()
            #subprocess.run(['kill', f'{bot.browser_pid}'],shell=True)
            print(f"Killed Process {bot.browser_pid} chrome")
        show_notification(" Science Scraper Finished ",
                        "Sciedir_crawler has finished the search for you keyword, Please check the CSV file for results !"
                    )
             

def parallel_execution():
                    items = offset_value  # List of items to process
                    print(f"in Parallel Execution, itemss --> {items}")
                    #additional_param = ...  # Additional parameter to pass
                    num_threads = multiprocessing.cpu_count()
                    # Create a multiprocessing pool
                    if num_threads <= 2 or len(items) == 1:
                        
                        pool = multiprocessing.Pool(processes= 1)
                    elif num_threads > 4:
                        pool = multiprocessing.Pool(processes=3)
                    else:
                        pool = multiprocessing.Pool(processes=num_threads - 2)
                    
                    # Parallelize the function execution over the list
                    results = [pool.apply_async(startWebChrome, args=(item, keyword_search, dates_range,total_page)) for item in items]
                    
                    # Get the results
                    #output = [result.get() for result in results]
                    
                    # Close the pool
                    pool.close()
                    pool.join()
                    #print("Output: {}".format(output))

if __name__ == "__main__":
    
    multiprocessing.freeze_support()
    """if not os.path.exists("Scraper_Logs"):

        os.mkdir("Scraper_Logs")
"""    #script_dir = os.path.dirname(os.path.abspath(__file__))

    """ if not os.path.exists("Includes\chromedriver_win32\chromedriver.exe"):
        
        os.makedirs("Includes\chromedriver_win32")
        os.chdir("Includes")
        if not os.path.exists("Data_files"):
            os.mkdir("Data_files")
        os.chdir("..\\")
        print(f"current working dir is: {os.getcwd()}")
            
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the file name and path relative to the script directory
        
        file = 'chromedriver_win32\chromedriver.exe'
        file_path = os.path.join(script_dir, file)
        new_path = os.path.join(script_dir,const.DRIVER_Path)
        print(file_path)    
        print("#"*20)
        print(new_path)
        os.rename(file_path,new_path)"""


    
    """registration =  Register_User("users_scidir.db")
    registration.createTable()
    registration.login_user()
    """
        
    #######################################
    # ADD COde Here to automate the crawling for List of Keywords
    #######################################
    print("Enter the path of keywords.csv file:")
    keywords = input()
    key_list = ""
    if keywords.startswith("\""):
        
        key_list = str(keywords)
        key_list = key_list.replace("\"","",-1)
    else:
        key_list = keywords
    print(f"After replacin \" : {key_list}")
    print(f"Chosen File : {key_list}")
    print("Enter Date Range e.g., 2002 or 2017-2023")
    d_range = input()
    """dates_range = d_range.split("-")
    dates = []
    if len(dates_range) == 2:
        d = [int(date) for date in dates_range]
        dates = [i for i in range(d[0],d[1]+1,1)]
        
        
    elif len(dates_range) == 1:
        dates = [int(dates_range)]
        
        
    print(dates)
        """
    dates_range = str(d_range)
    print("\{\}"*20)
    with open(key_list, "r") as list_file:
        Csv_File = csv.reader(list_file)
        for line in Csv_File:
                #t = 60*8
                print(line)
                keyword_search = line[0]
                offset_value = 0
                total_page = 0
                #startWebChrome(offset_value, keyword_search, str(d_range))
            
               
                with ScienceDirect() as bot:
                    bot.land_first_page(url=const.BASE_URL)
                    print(f"Session ID for Bot chrom ==> {bot.browser_pid}")
                    #user = read_userdetails()
                    #bot.sign_in(username=user[0], pswrd=user[1])
                    
                        
                    #bot.execute_script(f"window.open('about:blank','TAB_{dates_range}');")
                    #bot.switch_to.new_window(f"TAB_{dates_range}")
                    bot.implicitly_wait(5)
                    next_page = bot.GetNextLinks(keyword_search,dates_range,offset=None)
                    if next_page == None:
                        print(f" Check for processes still running ? {bot.service.assert_process_still_running()}")
                        print(f"Service.process.pid for chrome bot is : {bot.service.process.pid}")
                        #bot.stop_client()
                        #bot.service._terminate_process()
                        #ps1_script = '.\\kill.bat' + f'{str(bot.browser_pid)}'
                        os.system(r'.\\kill.bat ' + str(bot.browser_pid))
                        #process = subprocess.Popen(['taskkill', '/f', '/T', f'/pid {bot.browser_pid}'],shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                        #process = subprocess.Popen(["powershell","Stop-Process", f"-Id {bot.browser_pid},{bot.service.process.pid}",'-Force'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
                        #result = process.communicate()[0]
                        #print(result)
                        time.sleep(3)
                        bot.quit()
                        #subprocess.run(['kill', f'{bot.browser_pid}'],shell=True)
                        print(f"Killed Process {bot.browser_pid} chrome")
                
                        continue
                    
                    #bot.ExtractEmails(keyword_search,str(d_range),offset_value)
                    total_page = bot.TotalPages(next_page)
                    """for items in next_page[1]:
                        for item in items:
                            print(f"Extracted Facet Lists is : ==> {item}")"""
                    print(f"Total_pages are ==>> {total_page}")
                    offset_value = bot.OffsetValue(total_page)
                    print(f" Check for processes still running ? {bot.service.assert_process_still_running()}")
                    print(f"Service.process.pid for chrome bot is : {bot.service.process.pid}")
                    #process = subprocess.Popen(['taskkill /f /T /pid',f'{bot.service.process.pid}'],shell=True)
                        
                    #subprocess.run(['kill',f'{self.service.process.pid}'],shell=True)
                    #ps1_script = '.\\kill.bat' + f'{str(bot.browser_pid)}'
                    os.system(r'.\\kill.bat ' + str(bot.browser_pid))
                    #process = subprocess.Popen(['taskkill', '/f', '/T', f'/pid {bot.browser_pid}'],shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                    #process = subprocess.Popen(["powershell","Stop-Process", f"-Id {bot.browser_pid},{bot.service.process.pid}",'-Force'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
                    #result = process.communicate()[0]
                    #print(result)
                    time.sleep(3)
                    bot.stop_client()
                    bot.service._terminate_process()
                    #time.sleep(2)
                    bot.quit() 
                    #subprocess.run(['kill', f'{bot.browser_pid}'],shell=True)
                    print(f"Killed Process {bot.browser_pid} chrome")
                

                print("#"*15)
                print(offset_value)
                startWebChrome(offset_value[0],keyword_search,dates_range,total_page)
                #parallel_execution()
                ChangeVPN()
            
                time.sleep(17)