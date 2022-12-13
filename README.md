# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. 
      The aim is to keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a 
   virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of 
   the folder. This means that you can install packages in here without affecting files outside. 
   To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. 
    - Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective 
    - file. If you install a package, make sure others know by updating the requirements.txt file. 
    - An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. 
    - However, you do that, you'll want to set the file to be <code>server.py</code>. 
    - Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details.

    - If you want to run the development server, type in the directory, either <code>flask run</code> or 
   <code>python -m flask run</code>. The app should respond with an address you should be able to go to 
   using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). 
    This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. 
    * You can look here to see what email addresses the app will accept for login.

5. Testing

    Note that the application has been successfully tested. The directory tests contains a test folder for
   each issue that has been reported at https://github.com/OpenClassrooms-Student-Center/Python_Testing. Each
   issue has been successfully fixed. In other words, every test successfully passed. 
   The folder also contains a performance test. The performance test has been performed with 6 clubs logging at the 
   same time. In the 'tests' folder, you will also find an integration test folder, in this integration test, I tested
  how all the features, I added to the application interacts together. To conclude, I also checked my test coverage
   and the code has a coverage rate of 98%.

6. Conclusion and discussion for further development

   Finally, I fixed issues that the team development would normally be able to fix. I can understand that
   the team may be busy. In the future, the application will require a real authentication system and maybe
   a real database management system.
