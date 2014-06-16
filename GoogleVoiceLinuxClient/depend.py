#Install Linux (Debian) dependencies.

import os
try:
    import wx
except:
    os.system("sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev")

try: 
    import keyring
except:
    os.system("sudo apt-get install python-keyring")
    
try:
    import BeautifulSoup
except:
    try:
        import pip
    except:
        os.system("sudo apt-get install python-pip")
    os.system("pip install BeautifulSoup")

try:
    import googlevoice
except:
    os.system("python ./pygooglevoice-0.5/setup.py build")
    os.system("python ./pygooglevoice-0.5/setup.py install")

