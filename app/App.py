from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'random string'
try:
    # Connection database
    con = pymysql.connect('localhost', 'root', 'azerty', 'python_flask_crud')
    with con:
        cursor = con.cursor()
        check_connection = True
except:
    check_connection = False
    print('Error database connection')


# route home
@app.route('/')
def index():
    if check_connection:
        cursor.execute("SELECT id, DATE_FORMAT(created_at, '%d-%m-%Y à %H:%i'), city, subject, address FROM appointment")
        data = cursor.fetchall()
    else:
        data = False
    # return a title
    return render_template('index.html', appointments=data)


# route form add data
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash('Data Inserted Successfully')
        # name form data
        created_at = request.form['datetime']
        city = request.form['city']
        subject = request.form['subject']
        address = request.form['address']

        cursor.execute("INSERT INTO appointment (created_at, city, subject, address) VALUES (%s, %s, %s, %s)",
                       (created_at, city, subject, address))
        con.commit()

        return redirect(url_for('index'))


@app.route('/update/<int:id_appointment>', methods=['POST', 'GET'])
def update(id_appointment):
    if request.method == "POST":
        flash('Data Updated Successfully')
        # name form data
        created_at = request.form['datetime']
        city = request.form['city']
        subject = request.form['subject']
        address = request.form['address']

        cursor.execute("UPDATE appointment set created_at = %s, city = %s, subject = %s, address = %s WHERE id= %s",
                       (created_at, city, subject, address, id_appointment))
        con.commit()

        return redirect(url_for('index'))


@app.route('/delete/<int:id_appointment>', methods=['GET'])
def delete(id_appointment):
    cursor.execute("DELETE FROM appointment WHERE id= %s", id_appointment)
    con.commit()
    flash('Data Deleted Successfully')
    return redirect(url_for('index'))


# Launch the web site in local
if __name__ == "__main__":
    app.run(debug=True)
