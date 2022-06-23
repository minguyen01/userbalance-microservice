=================================================
User Balance Microservice
=================================================
Author: Minh Nguyen


To Set Up the Database
=================================================
1. Go to the database.py file
2. Edit the DATABASE_URI variable:
	- Replace the first '#' string with the master password
	- Replace the second '#' string with the name of the database
3. Run the database in pgAdmin
4. Run the datapase.py file


To Run the Web App using the Windows Command Line
=================================================
1) 
Activate the virtual environment:
venv\Scripts\activate.bat

2)
Set the FLASK_APP:
set FLASK_APP=microservice

3)
Run the microservice:
flask run