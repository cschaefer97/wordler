Welcome to my Wordle solver app!
Running this is simple. After downloading this repository, Install PIP and the latest version of Python on your machine. Then, Using PIP, install the packages seen in requirements.txt.

Now open textsender.py and replace the following strings:
1. For EMAIL, replace with your personal email or any email address you have access to
2. For password, replace with an _app password_ for your email address. This different than your usual logon password and allows an application to use your email address. Instructions can be found here (gmail): https://support.google.com/mail/answer/185833?hl=en

   NOTE: App Passwords are unique by machine, so if you set this up on multiple machines, you will need a different app password for each one.
4. Replace destination with your phone number FOLLOWED BY your carrier extension (e.g. '@mms.att.net' for AT&T users). Carrier extensions can be found here: https://avtech.com/articles/138/list-of-email-to-sms-addresses/
5. Run the main file with 'python ./main.py'

That's it! You should see a web broswer pop up and solve the wordle for you. Shortly after you will get a text message to your phone with the 'emoji score' and the correct word. Enjoy!
