from flask import Flask, render_template, request, redirect, url_for,jsonify
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import pickle

app = Flask(__name__)
#model = pickle.load(open('./model/model.pkl','rb'))

@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route('/worldcup/', defaults = {'nation' : 'England'})
# def worldcup(nation):

#     conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',
#     db='football', charset='utf8')

#     cur = conn.cursor()

#     cur.execute(f"""
#     SELECT * 
#     FROM all_data
#     WHERE (home_team = {nation} ) OR (away_team = {nation} );
#     """)

#     val = cur.fetchall()

#     return val

@app.route('/worldcup')
def worldcup():

    conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',
    db='football', charset='utf8')

    cur = conn.cursor()

    cur.execute("""
    SELECT * 
    FROM all_data
    ORDER BY date DESC
    LIMIT 50;
    """)

    val = cur.fetchall()

    conn.close()

    # return render_template('worldcup.html', val = val)
    #return str(val)
    return render_template('worldcup.html', val=val)

@app.route('/worldcup/<nation>')
def all_data(nation):
    
    conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',
    db='football', charset='utf8')

    cur = conn.cursor()

    cur.execute("""
    SELECT * 
    FROM all_data
    WHERE (home_team = %s) OR (away_team = %s)
    ORDER BY date DESC
    LIMIT 50;
    """,[nation, nation])

    val = cur.fetchall()

    conn.close()

    return render_template('nation_records.html',nation = nation, val=val)



    
@app.route('/login')
def login():
    return render_template('login.html')



# @app.route('/index')
# def index():
#     return render_template('index.html')




@app.route('/login_confirm', methods=['POST'])
def login_confirm():

    id_ = request.form['id_']
    pw_ = request.form['pw_']
    if id_ == 'admin' and pw_ == 'admin':
        return render_template('index.html')
        #redirect(url_for('index'))
    else:
        return redirect(url_for('login'))




@app.route('/api',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)




if __name__ == "__main__":              
    app.run(debug=True)