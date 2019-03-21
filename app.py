from flask import Flask , render_template, request, url_for, redirect
from dbconnnect import connection
import csv
from werkzeug import secure_filename

app=Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html',name="chandu")



@app.route('/bioform', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST":
        username= request.form['username']
        phonenumber=request.form['phonenumber']
        return redirect(url_for('showbio', username=username,phonenumber=phonenumber))
    return render_template("bio_form.html")

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method  == 'POST':
        f=request.files['file']
        f.save(secure_filename(f.filename))
        # file(f.filename)
        # return 'file uploaded succesfully'
        with open(f.filename) as csvfile:
            readCSV=csv.reader(csvfile,delimiter=',')
            c, conn=connection()
            for row in readCSV:
                if row:
                    name=str(row[0])
                    phone_number=int(row[1])
                    val=(name,phone_number)
                    sql="INSERT INTO DATA (name,phone_number) VALUES (%s,%s)"
                    c.execute(sql,val)

            conn.commit()
    return redirect(url_for('contacts'))
# @app.route('/file',methods=['GET','POST'])
# def file(files):
    

                

@app.route('/showbio', methods=['GET'])
def show_bio_data_form():
    username=request.args.get('username')
    phonenumber=request.args.get('phonenumber')
    try:
        c, conn=connection()
        sql="INSERT INTO DATA (name,phone_number) VALUES (%s,%s)"
        val=(username,phonenumber)
        c.execute(sql,val)
        conn.commit()
        print(c.rowcount,"record inserted")
    except Exception as e:
        return(str(e))
    return render_template("show_bio.html", username=username,phonenumber=phonenumber)

@app.route('/contacts/', methods=["GET"])
def contacts():
    try:
        c, conn=connection()
        sql="SELECT * FROM DATA"
        c.execute(sql)
        records=c.fetchall()
        # for row in records:
        #     print(row[0])
        #     print(row[1])
        #     print(row[2])
        c.close()
        return render_template('contacts.html', data=records)
        

        # print(val)
        # return(val)
    except Exception as error:
        print("Failed to get record from database: {}"+str(error))

    

if __name__=="__main__":
    app.run(debug=True,port=1263)


