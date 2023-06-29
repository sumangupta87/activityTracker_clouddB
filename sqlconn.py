import os
import urllib.parse 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Configure Database URI: 
params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:appdb-432.database.windows.net,1433;Database=appdb;Uid=SumanSQL;Pwd=Welcome@12345;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30")


# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
