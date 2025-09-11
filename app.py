
from flask import Flask, render_template, request, jsonify, send_file
from flask_mysqldb import MySQL
import json

import matplotlib.pyplot as plt

from datetime import datetime

from config import MYSQL_CONFIG
from plot_exercise import exercise_plot
from plot_calory import calory_plot,korea_time

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = MYSQL_CONFIG['MYSQL_HOST']
app.config['MYSQL_PORT'] = MYSQL_CONFIG['MYSQL_PORT']
app.config['MYSQL_USER'] = MYSQL_CONFIG['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = MYSQL_CONFIG['MYSQL_DB']

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    # Exercise Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS exercises2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            weight INT,
            reps INT,
            sets INT,
            depth VARCHAR(20),
            width VARCHAR(20),
            angle VARCHAR(20),
            rest FLOAT,
            time VARCHAR(20)
        )
    ''')

    # Food Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS foods2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            weight INT,
            time VARCHAR(20)
        )
    ''')
    # User Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            weight FLOAT,
            status VARCHAR(20),
            how_many_week INT,
            time VARCHAR(20)
        )
    ''')

    # Nutrient Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nutrient (
            name VARCHAR(255) PRIMARY KEY,
            calory FLOAT,
            protein FLOAT
        )
    ''')

    # Body Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bodybuild (
            target VARCHAR(255) ,
            name VARCHAR(255) PRIMARY KEY
        )
    ''')

    mysql.connection.commit()
    cur.close()

def confirmBodyweight(weight,status,how_many_week,time):

    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO user2 (weight,status,how_many_week,time)
        VALUES (%s,%s, %s, %s)
    ''', (weight, status,how_many_week,time))
    mysql.connection.commit()
    cur.close()    
    
def confirmExercise(name, weight, reps, sets, depth, width, angle, rest, time,memo):
    try:
        # Attempt to convert non-empty values to integers
        weight = int(weight) if weight and weight.strip() else None
        reps = int(reps) if reps and reps.strip() else None
        sets = int(sets) if sets and sets.strip() else None
        rest = rest if rest else None
    except ValueError:
        # Handle the case where conversion to integer fails
        print("Error: Unable to convert some values to integers.")
        return
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    print('confirm',time)
    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO exercises2 (name, weight, reps, sets, depth, width, angle, rest, time,memo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (name, weight, reps, sets, depth, width, angle, rest,time,memo))
    mysql.connection.commit()
    cur.close()

def confirmFood(name, weight,time):

    weight = int(weight) if weight and weight.strip() else None
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO foods2 (name, weight,time)
        VALUES (%s, %s, %s)
    ''', (name, weight, time))
    mysql.connection.commit()
    cur.close()

def confirmAddFood(name, calory,protein):

    print('name, calory,protein',name, calory,protein)
    calory = float(calory)/100 if calory and calory.strip() else None
    protein = float(protein)/100 if protein and protein.strip() else None

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO nutrient (name, calory,protein)
        VALUES (%s, %s, %s)
    ''', (name, calory, protein))
    mysql.connection.commit()
    cur.close()

def confirmAdd(target,name):

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO bodybuild (target,name)
        VALUES (%s, %s)
    ''', (target,name))
    mysql.connection.commit()
    cur.close()

## HTML을 주는 부분
@app.route('/')
def home():
    
    image_path = 'barbel.png'  # 이미지의 상대 경로
    image_path2 = 'gigached.png'  # 이미지의 상대 경로
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM nutrient")
    food_rows = cur.fetchall()

    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bodybuild")
    body_rows = cur.fetchall()

    print('body_rows',body_rows)

    cur.close()
    return render_template('index.html', image_path=image_path, image_path2=image_path2, food_list=food_rows, body_list=body_rows)

@app.route('/confirm-bodyweight', methods=['POST'])
def confirm_bodyweight():
    data = request.form
    confirmBodyweight(data['bodyweight'],data['status'],data['how_many_week'],data['time'])
    return jsonify({'status': 'success'})

@app.route('/confirm-exercise', methods=['POST'])
def confirm_exercise():
    data = request.form
    confirmExercise(data['name'], data['weight'], data['reps'], data['sets'], data['depth'], data['width'], data['angle'], data['rest'],data['time'],data['memo'])
    return jsonify({'status': 'success'})

@app.route('/confirm-food', methods=['POST'])
def confirm_food():
    data = request.form
    confirmFood(data['name'], data['weight'],data['time'])
    return jsonify({'status': 'success'})

@app.route('/confirm-add-food', methods=['POST'])
def confirm_add_food():
    data = request.form
    confirmAddFood(data['food_name'], data['food_calory'],data['food_protein'])
    return jsonify({'status': 'success'})
@app.route('/confirm-add', methods=['POST'])
def confirm_add():
    data = request.form
    confirmAdd(data['target'], data['name'])
    return jsonify({'status': 'success'})

@app.route('/get_exercise_data', methods=['GET'])
def get_exercise_data():
    try:
        title = request.args.get('title')
        # print('title',title)
        # MySQL 쿼리 실행
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM project.exercises2 WHERE name = %s", (title,))
        data = cur.fetchall()         
        # Convert datetime objects to strings
        formatted_data = []
        for row in data:
            formatted_row = [str(item) if isinstance(item, datetime) else item for item in row]
            formatted_data.append(formatted_row)
        #     print('formatted_row',formatted_row)
         
        # print('formatted_data',formatted_data)    
        
        
        # 데이터 처리
        # time_data = [int(datetime.strptime(item[-1], '%Y-%m-%d %H:%M:%S').timestamp()) for item in formatted_data]

        cur.close() 

        img_data,date_memo_dict = exercise_plot(formatted_data, title)

        # 맷플롯립 그래프를 클라이언트에게 전달
        return jsonify({'img_data': img_data, 'date_memo_dict': date_memo_dict})
        
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/get_food_data', methods=['GET'])    
def get_food_data():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''
                SELECT 
                    time,
                    CASE 
                        WHEN how_many_week = 1 THEN weight * 24 * 1.5
                        WHEN how_many_week = 2 THEN weight * 24 * 1.35
                        WHEN how_many_week = 3 THEN weight * 24 * 1.2
                    END AS req_calory,
                    CASE 
                        WHEN status = 'increase' THEN weight * 1.6
                        WHEN status = 'decrease' THEN weight * 1
                        WHEN status = 'maintain' THEN weight * 1
                    END AS req_protein,
                    CASE 
                        WHEN status = 'increase' THEN 
                            CASE 
                                WHEN how_many_week = 1 THEN weight * 24 * 1.5 + 200
                                WHEN how_many_week = 2 THEN weight * 24 * 1.35 + 200
                                WHEN how_many_week = 3 THEN weight * 24 * 1.2 + 200
                            END
                        WHEN status = 'decrease' THEN 
                            CASE 
                                WHEN how_many_week = 1 THEN weight * 24 * 1.5 - 200
                                WHEN how_many_week = 2 THEN weight * 24 * 1.35 - 200
                                WHEN how_many_week = 3 THEN weight * 24 * 1.2 - 200
                            END
                        WHEN status = 'maintain' THEN 
                            CASE 
                                WHEN how_many_week = 1 THEN weight * 24 * 1.5 
                                WHEN how_many_week = 2 THEN weight * 24 * 1.35 
                                WHEN how_many_week = 3 THEN weight * 24 * 1.2
                            END
                    END AS adjusted_req_calory
                FROM 
                    user2;

                ''')

        # 결과 가져오기
        results = cur.fetchall()

        # 결과 처리
        req_date_totals = {}
        for date, _, req_protein, adjusted_req_calory in results:

            req_date_totals[date] = {'req_calories': 0, 'req_protein': 0}

            req_date_totals[date]['req_calories'] = adjusted_req_calory
            req_date_totals[date]['req_protein'] = req_protein

        # 두 번째 쿼리 실행
        # cur.execute('''
        #     SELECT foods2.time, SUM(foods2.weight * nutrient.calory) AS total_calories, SUM(foods2.weight * nutrient.protein) AS total_protein
        #     FROM foods2
        #     INNER JOIN nutrient ON foods2.name = nutrient.name
        #     GROUP BY foods2.time
        # ''')

        cur.execute('''
            SELECT 
                DATE_FORMAT(foods2.time, '%Y-%m-%d') AS formatted_time, 
                SUM(foods2.weight * nutrient.calory) AS total_calories, 
                SUM(foods2.weight * nutrient.protein) AS total_protein
            FROM 
                foods2
            INNER JOIN 
                nutrient ON foods2.name = nutrient.name
            GROUP BY 
                formatted_time; -- GROUP BY should use the alias or the expression itself

        ''')

        # 결과 가져오기
        results = cur.fetchall()

        # 결과 처리
        date_totals = {}
        for time, calories, protein in results:
            if time not in date_totals:
                date_totals[time] = {'calories': 0, 'protein': 0}
            date_totals[time]['calories'] = calories
            date_totals[time]['protein'] = protein

        # 세 번째 쿼리 실행            
        today=korea_time()
        print('today',today)
        # SQL 쿼리 실행
        cur.execute('''
           SELECT name, weight, DATE_FORMAT(time, '%Y-%m-%d') AS formatted_time
            FROM foods2
            WHERE DATE(time) = CURDATE();
        ''')

        # 결과 가져오기
        results = cur.fetchall()

        # print('results',results)
        
        # 오늘 먹은것 리스트
        today_food = {}
        for name, weight,_ in results:
            if name in today_food:
                today_food[name] += weight
            else:
                today_food[name] = weight
            
        print('today_food',today_food)

        img_data,alert_calories,alert_protein,today = calory_plot(req_date_totals,date_totals)

        # 맷플롯립 그래프를 클라이언트에게 전달
        return jsonify({'img_data': img_data,"alert_calories":alert_calories,"alert_protein":alert_protein,"today":today,"today_food":today_food})

    except mysql.connector.Error as error:
        print(f"Failed to insert data into intake_per_minute table: {error}")

        
    # except Exception as e:
    #     return json.dumps({'error': str(e)})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)