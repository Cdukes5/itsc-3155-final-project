Instructions for use:

1. Set up the database. This application uses MySQL and the connection to the database is located in app.py that consists of the line: app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flasksql'. Add the tables in tables.sql to your MySQL database then change the connection password and 'flaskql' to your own password and database.

2. Type flask run after everything is set up and dependencies are installed from requirements.txt. 

3. Sign up then login and you are ready to use the forums.