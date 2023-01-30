from flask import render_template, request, redirect, Blueprint, flash, url_for, current_app, make_response
from flask_login import login_user, current_user, logout_user, login_required
from portfoliowebsite.models import Ratings, User
from portfoliowebsite.actions.forms import UploadFile, QueryDB
from portfoliowebsite import db
import os
from portfoliowebsite import server
from werkzeug.utils import secure_filename
import pandas as pd
import xlrd
from datetime import datetime
import numpy as np

actions = Blueprint('actions',__name__)

# columns used to filter the base excel file
base_cols = ['Security ID', 'Symbol', 'Description','Risk','Objectives','Risk Explanation']

# new columns to be used once date is added
rtg_cols = ['Date','Security ID', 'Symbol', 'Description','Risk','Objectives','Risk Explanation']

@actions.route('/view-db')
@login_required
def view_db():
    # Example query
    # query = Ratings.query.filter_by(symbol='AMZN')
    # print(query.all())
    # When we print things out, it uses the __repr__ in our class

    form = QueryDB()

    if form.validate_on_submit():


        return redirect(url_for('actions.view_db'))



    return render_template('view_db.html.j2', values=Ratings.query.all(), form=form)


@actions.route('/upload-db', methods=['GET','POST'])
@login_required
def upload_db():
    form = UploadFile()

    if form.validate_on_submit():



        # Checks if file was uploaded, otherwise form.file.data = None
        if form.file.data:
            # first, grab the filename
            filename = form.file.data.filename

            # Grab the extension type and save
            ext_type = filename.split('.')[-1]
            filepath = os.path.join(current_app.root_path, 'static/ratings_files', filename)
            form.file.data.save(filepath)


        df = pd.read_excel(filepath)
        df1 = df.head(100)
        print(df.head())
        print(len(df))
        dt = datetime.strptime(form.date.data, '%Y-%m-%d')
        date_col = [dt for i in range(len(df1))]

        df1['Date'] = date_col
        df1 = df1[rtg_cols]
        print(df1.head())
        print(type(df1['Date'][0]))

        # Create array of date column
        db_dates = np.array(db.session.query(Ratings.date).all())
        print(np.unique(db_dates))
        print('\n')
        if dt.date() in np.unique(db_dates):
            print('yes')
        else:
            print('no')

        print('\n')

        print(dt)
        print(dt.date())
        print(np.unique(db_dates))
        print('\n')
        #print(np.unique(db_dates)[0])
        #print(np.unique(db_dates)[1])



        # Checks to see if this file has already been uploaded to db based on date
        if dt.date() not in np.unique(db_dates):
            for i in range(len(df1)):
                row = Ratings(
                    date = dt,
                    security_id = df1[rtg_cols[1]][i],
                    symbol = df1[rtg_cols[2]][i],
                    description = df1[rtg_cols[3]][i],
                    risk = df1[rtg_cols[4]][i],
                    objectives = df1[rtg_cols[5]][i],
                    risk_explanation = df1[rtg_cols[6]][i],
                )
                db.session.add(row)

            flash('File Upload Successful')
            db.session.commit()
        else:
            flash('Could not upload, date already exists.')

        #Ratings.query.filter_by(date)


        return redirect(url_for('actions.upload_db'))


    # Next, we need to upload the excel file to the db
    # First, we save the excel file as pandas df
    # Next, df.to_sql("df", connection, if_exists="replace", index=False)
    #   if_exists has replace, fail (raises error), append
    # connection in youtube video is con=db.connect('sqlite.db')
    # we create pandas df from sql with df=pd.read_sql_query('select * from table', con)

    # can also do db.session.add_all([x,y]) how do I know what db I'm adding to?
    # What is the current session if I'm not directly referencing the Ratings class?
    # Need to call the Ratings class directly, looping through df to upload




    return render_template('upload_db.html.j2', form=form)


@actions.route('/edit-db')
@login_required
def edit_db():
    # Below is how we make updates to the table

    # query = Ratings.query.filter_by(symbol="AMZN")
    # query.rating = "High risk"
    # db.session.add(query)
    # db.session.commit()

    # Migrating db changes

    # set FLASK_APP = app.py
    # This sets the FLASK_APP environment variable
    # flask db init -> sets up the migrations directory
    # flask db migrate -m "some message" -> sets up the migration file
    # flask db upgrade -> updates the database with the migration
    return render_template('edit_db.html.j2')
