import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import pandas as pd
import numpy as np



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fi.db")

df = pd.read_excel (r'dummy data.xlsx')
print (df)


for index, row in df.iterrows():

    for i in range(1995,2019):
        if(np.isnan(row[i]) == False):
            print("insert")
            db.execute("INSERT INTO balance (user_id, EOYbalance, year) VALUES (:user_id, :EOYbalance, :year)", user_id=int(row["Id"]), EOYbalance=int(row[i]), year=i)