Google Voice Client (Designed on and for Linux)
-------------------------------------------

This is a program I decided to write when I found that there was a serious lack of a desktop application outside of a browser for Google Voice. Thanks to the creaters of pyGoogleVoice, I had an API to work with. Since this API has to rely on HTML and JSON downloads, it tends to be a bit slow, but not incredibly. I have found if I keep my inbox clean (reducing the downloaded data), it will get any new messages  withen 5 seconds or less of my phone.

###Use:
####Dependencies-
//I have included a python script that will install dependencies for Linux. It is untested, but worth a try.;)

-python 2.7

-wxPython (v2.8 is best)

-python-keyring

-BeautifulSoup

-pygooglevoice (custom package! In repository. I had to modify some scripts to make it work)



All you have to do is run "python main.py" in the root directory of the repo to run the program once dependencies are installed.