import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import statistics

import pandas as pd
import numpy as np


def canal():
    # Configure CS50 Library to use SQLite database
    db = SQL("sqlite:///fi.db")

    ref = []
    ref_savings = 30000
    ref_rate = 0.06
    savings = 0

    for i in range(0,24):
        savings = savings*(1+ref_rate) + ref_savings
        ref.append(savings)


    full_data = db.execute(f"SELECT user_id, year, EOYbalance FROM balance ORDER BY user_id, year")

    all_users = []
    list = []
    i=1
    for row in full_data:
        if row['user_id'] == i:
            list.append(row['EOYbalance'])
        else:
            all_users.append(list)
            i+=1
            list=[row['EOYbalance']]


    new_list = []

    for user in all_users:
        i=0
        offset = []
        while user[0]>ref[i]:
            i+=1
            offset.append(0)

        new_list.append(offset+user)



    nb_users = len(new_list)
    max_list = 0
    for i in range(nb_users):
        if len(new_list[i])>max_list:
            max_list=len(new_list[i])


    average = []
    std = []
    for j in range(0,max_list):
        col=[]
        for i in range(0,nb_users):
            if len(new_list[i]) > j:
                if new_list[i][j] != 0:
                    col.append(new_list[i][j])

        if len(col)>=5:
            average.append(int(sum(col)/len(col)))
            std.append(int(statistics.stdev(col)))


    min_1dev = [a - b for a, b in zip(average, std)]
    max_1dev = [a + b for a, b in zip(average, std)]

    return min_1dev, max_1dev