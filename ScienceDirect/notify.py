
import subprocess, random, os

from plyer import notification

def show_notification(title, message,timeout=None):
    

    # Set up the notification
    notification.notify(
        title=title,
        message=message,
        #app_icon="noun-data-science-2475218.ico",
        timeout=timeout
        #threaded=True,
        #callback_on_click=lambda: os.startfile(folder_path)
    )


def ChangeVPN():
    countries = ["Georgia","Serbia","Moldova",'"North Macedonia"',"Jersey","Monaco","Slovakia",'Lebanon','Argentina',
                     "Slovenia","Croatia","Albania","Cyprus","Liechtenstein","Malta","Ukraine",'Ghana','Chile','Colombia',
                     "Belarus","Bulgaria","Hungary","Luxembourg","Montenegro","Andorra",'Morocco','Honduras','Guatemala',
                     '"Czech Republic"',"Estonia","Latvia","Lithuania","Poland","Armenia","Austria",'Cuba','Panama',
                     "Portugal","Greece","Finland","Belgium","Denmark","Norway","Iceland","Ireland",'Bermuda','Mexico',
                     "Spain","Romania","Italy","Sweden","Turkey","Singapore",'Kenya','Israel','"South Africa"','Canada',
                     "Australia",'"South Korea - 2"',"Malaysia","Pakistan",'"Sri Lanka"',"Kazakhstan",'Bahamas','Brazil',
                     "Thailand","Indonesia",'"New Zealand"',"Cambodia","Vietnam","Macau",'Jamaica',
                     "Mongolia","Laos","Bangladesh","Uzbekistan","Myanmar","Nepal","Brunei","Bhutan",'Venezuela',
                     '"United Kingdom"', '"United States"',"Japan", "Germay", '"Hong Kong"', "Netherlands",'Bolivia',
                     "Switzerland","Algeria","France","Egypt"] 
    choice = random.choice(countries)
    print(f"Selected Country is {choice}")
    os.environ["ExpressVPN"] = os.pathsep + r"C:\Program Files (x86)\ExpressVPN\services"
    
    process = subprocess.Popen(["powershell", "ExpressVPN.CLI.exe", "disconnect"], shell=True)
    result = process.communicate()[0]
    print(result)
    process = subprocess.Popen(["powershell", "ExpressVPN.CLI.exe", "connect", f"{str(choice)}"], shell=True)
    result = process.communicate()[0]
    print(result)
    
    #################################################
    




            
    
            