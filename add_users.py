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

for i in range(0,60):
    db.execute("INSERT INTO users (fname, lname, email, hash) VALUES ('bob', 'james', 'bob@gmail.com', 'bob')")