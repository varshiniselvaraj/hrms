from sys import api_version
from flask import Flask, blueprints, render_template, request,url_for,redirect,flash, make_response,session
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from pip._vendor.urllib3.contrib import appengine
from datetime import datetime, timedelta
from functools import wraps
import jwt

from flask import jsonify
app=Flask(__name__,template_folder='templates')
app.config["MYSQL_HOST"] = "65.1.85.188"
app.config["MYSQL_USER"] = "devteam"
app.config["MYSQL_PASSWORD"] = "d$vteam#2022"
app.config["MYSQL_DB"] = "hrms"
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
mysql = MySQL(app)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
       
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'


@app.route('/public')
def public():
    return 'For Public'



@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == 'maestrowiz':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token':token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})



@app.route('/logout', methods=['POST'])
def logout():
    pass


@app.route('/employee',methods=['GET'])
def get_employee():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM employee")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res



# @app.route('/employees',methods=['GET'])
# def get_employee():
#     con = mysql.connection.cursor()
#     con.execute("""SELECT employee.Employee_Id,
#   employee.Employee_Name,project_hrms.ProjectId,project_hrms.Acc_Id
#   FROM employee 
#   INNER JOIN project_hrms""")
#     res= con.fetchall()
#     res = jsonify(res)
#     con.close()     
#     return res

@app.route("/employee/add",methods=['GET','POST'])
def addEmployee():
    if request.method=='POST':
        Employee_Id=request.form['Employee_Id']
        Employee_Name=request.form['Employee_Name']
        DateOfBirth=request.form['DateOfBirth']
        Address=request.form['Address']
        EmailId=request.form['EmailId']
        BloodGroup=request.form['BloodGroup']
        Qualification=request.form['Qualification']
        ContactNo=request.form['ContactNo']
        con=mysql.connection.cursor()
        sql="insert into employee(Employee_Id,Employee_Name,DateOfBirth,Address,EmailId,BloodGroup,Qualification,ContactNo) value (%s,%s,%s,%s,%s,%s,%s,%s)"
        con.execute(sql,[Employee_Id,Employee_Name,DateOfBirth,Address,EmailId,BloodGroup,Qualification,ContactNo])
        mysql.connection.commit()
        con.close()   
        return {}
    return render_template("addEmployee.html")

@app.route("/employee/edit/<string:id>",methods=['GET','POST'])
def editEmployee(id):
    sql = 'SELECT * FROM employee WHERE Employee_Id=%s'
    con = mysql.connection.cursor()
    con.execute(sql % (str(id)))
    res= con.fetchall()
    if request.method == 'POST':
        Employee_Name = request.form['Employee_Name']
        DateOfBirth = request.form['DateOfBirth']
        Address = request.form['Address']
        EmailId = request.form['EmailId']
        BloodGroup = request.form['BloodGroup']
        Qualification = request.form['Qualification']
        ContactNo = request.form['ContactNo']
        print(Employee_Name,DateOfBirth,Address,EmailId,BloodGroup,Qualification,ContactNo)
        con = mysql.connection.cursor()
        sql=("""
               UPDATE employee
               SET Employee_Name=%s,DateOfBirth=%s, Address=%s,EmailId=%s,BloodGroup=%s,Qualification=%s,ContactNo=%s
               WHERE Employee_Id=%s
            """)
        con.execute(sql,[Employee_Name, DateOfBirth, Address, EmailId, BloodGroup, Qualification,ContactNo,id])
        mysql.connection.commit()
        con.close()
        return {}
    return render_template("editEmployee.html",data=res[0])




@app.route("/employee/delete/<string:id>",methods=['GET','POST'])
def deleteEmployee(id):
    con=mysql.connection.cursor()
    print(id)
    sql = 'DELETE FROM employee WHERE Employee_Id=%s'
    con.execute(sql % (str(id)))
    mysql.connection.commit()
    con.close()
    return {}

@app.route('/account',methods=['GET'])
def get_account():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM accounts_hrms")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res


@app.route('/accounts',methods=['GET'])
def get_accounts():
    con = mysql.connection.cursor()
    con.execute("""SELECT accounts_hrms.Acc_Id,
  accounts_hrms.Acc_Name,accounts_hrms.Manager_Id,project_hrms.ProjectId
  FROM accounts_hrms 
  INNER JOIN project_hrms""")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res


@app.route("/account/add",methods=['GET','POST'])
def addAccount():
    if request.method=='POST':
        Acc_Id=request.form['Acc_Id']
        Acc_Name=request.form['Acc_Name']
        Acc_Location=request.form['Acc_Location']
        Manager_Id=request.form['Manager_Id']
        con=mysql.connection.cursor()
        sql="insert into accounts_hrms(Acc_Id,Acc_Name,Acc_Location,Manager_Id) value (%s,%s,%s,%s)"
        con.execute(sql,[Acc_Id,Acc_Name,Acc_Location,Manager_Id])
        mysql.connection.commit()
        con.close()   
        return {}
    return render_template("addAccount.html")
    
    
    
@app.route("/account/edit/<string:id>",methods=['GET','POST'])
def editAccount(id):
    sql = 'SELECT * FROM accounts_hrms WHERE Acc_Id=%s'
    con = mysql.connection.cursor()
    con.execute(sql % (str(id)))
    res= con.fetchall()
    if request.method == 'POST':
        Acc_Name=request.form['Acc_Name']
        Acc_Location=request.form['Acc_Location']
        Manager_Id=request.form['Manager_Id']
        print(Acc_Name,Acc_Location,Manager_Id)
        con = mysql.connection.cursor()
        sql=("""
               UPDATE accounts_hrms
               SET Acc_Name=%s,Acc_Location=%s, Manager_Id=%s
               WHERE Acc_Id=%s
            """)
        con.execute(sql,[Acc_Name, Acc_Location, Manager_Id,id])
        mysql.connection.commit()
        con.close()
        return {}
    return render_template("editAccount.html",data=res[0])


@app.route("/account/delete/<string:id>",methods=['GET','POST'])
def deleteAccount(id):
    con=mysql.connection.cursor()
    print(id)
    sql = 'DELETE FROM accounts_hrms WHERE Acc_Id=%s'
    con.execute(sql % (str(id)))
    mysql.connection.commit()
    con.close()
    return {}

@app.route('/project',methods=['GET'])
def get_project():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM project_hrms")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res

@app.route('/projects',methods=['GET'])
def get_projects():
    con = mysql.connection.cursor()
    con.execute("""SELECT project_hrms.ProjectId,
  project_hrms.Project_Name,emply_acc.Employee_Id,emply_acc.Acc_Id
  FROM project_hrms 
  INNER JOIN emply_acc""")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res

@app.route("/project/add",methods=['GET','POST'])
def addProject():
    if request.method=='POST':
        ProjectId=request.form['ProjectId']
        Project_Name=request.form['Project_Name']
        StartDate=request.form['StartDate']
        EndDate=request.form['EndDate']
        Project_Status=request.form['Project_Status']
        Manager_Id=request.form['Manager_Id']
        Acc_Id=request.form['Acc_Id']
        cur=mysql.connection.cursor()
        sql="insert into project_hrms(ProjectId,Project_Name,StartDate,EndDate,Project_Status,Manager_Id,Acc_Id) value (%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,[ProjectId,Project_Name,StartDate,EndDate,Project_Status,Manager_Id,Acc_Id])
        mysql.connection.commit()
        cur.close()      
        return {}
    return render_template("addProject.html") 
@app.route("/project/edit/<string:id>",methods=['GET','POST'])
def editProject(id):
    sql = 'SELECT * FROM project_hrms WHERE ProjectId=%s'
    con = mysql.connection.cursor()
    con.execute(sql % (str(id)))
    res= con.fetchall()
    if request.method == 'POST':
        Project_Name=request.form['Project_Name']
        StartDate=request.form['StartDate']
        EndDate=request.form['EndDate']
        Project_Status=request.form['Project_Status']
        Manager_Id=request.form['Manager_Id']
        Acc_Id=request.form['Acc_Id']
        print(Project_Name,StartDate,EndDate,Project_Status,Manager_Id,Acc_Id)
        con = mysql.connection.cursor()
        sql=("""
               UPDATE project_hrms
               SET Project_Name=%s,StartDate=%s,EndDate=%s,Project_Status=%s,Manager_Id=%s,Acc_Id=%s
               WHERE ProjectId=%s
            """)
        con.execute(sql,[Project_Name, StartDate,EndDate,Project_Status,Manager_Id,Acc_Id,id])
        mysql.connection.commit()
        con.close()
        return {}
    return render_template("editProject.html",data=res[0])

@app.route("/project/delete/<string:id>",methods=['GET','POST'])
def deleteProject(id):
    con=mysql.connection.cursor()
    print(id)
    sql="delete from project_hrms where ProjectId=%s"
    con.execute(sql % (str(id)))
    mysql.connection.commit()
    con.close()
    return {}

@app.route('/employeeproject',methods=['GET'])
def employeeproject():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM employee_projects")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res


@app.route("/emply/add",methods=['GET','POST'])
def addEmply():
    if request.method=='POST':
        EpId=request.form['EpId']
        EAccId=request.form['EAccId']
        ProjectId=request.form['ProjectId']
        Employee_StartDate=request.form['Employee_StartDate']
        cur=mysql.connection.cursor()
        sql="insert into employee_projects(EpId,EAccId,ProjectId,Employee_StartDate) value (%s,%s,%s,%s)"
        cur.execute(sql,[EpId,EAccId,ProjectId,Employee_StartDate])
        mysql.connection.commit()
        cur.close()       
        return {}
    return render_template("addEmply.html") 

@app.route("/emply/edit/<string:id>",methods=['GET','POST'])
def editEmply(id):
    sql = 'SELECT * FROM employee_projects WHERE EpId=%s'
    con = mysql.connection.cursor()
    con.execute(sql % (str(id)))
    res= con.fetchall()
    if request.method == 'POST':
        EAccId=request.form['EAccId']
        ProjectId=request.form['ProjectId']
        Employee_StartDate=request.form['Employee_StartDate']
        print(EAccId,ProjectId,Employee_StartDate)
        con = mysql.connection.cursor()
        sql=("""
               UPDATE employee_projects
               SET EAccId=%s,ProjectId=%s,Employee_StartDate=%s
               WHERE EpId=%s
            """)
        con.execute(sql,[EAccId, ProjectId,Employee_StartDate,id])
        mysql.connection.commit()
        con.close()
        return {}
    return render_template("editEmply.html",data=res[0])

@app.route("/emply/delete/<string:id>",methods=['GET','POST'])
def deleteEmply(id):
    con=mysql.connection.cursor()
    print(id)
    sql="delete from employee_projects where EpId=%s"
    con.execute(sql % (str(id)))
    mysql.connection.commit()
    con.close()
    return {}
@app.route('/employeeaccount',methods=['GET'])
def get_employee_account():
    con = mysql.connection.cursor()
    print
    con.execute("SELECT * FROM emply_acc")
    res= con.fetchall()
    res = jsonify(res)
    con.close()     
    return res



@app.route("/emplyacc/add",methods=['GET','POST'])
def addemplyacc():
    if request.method=='POST':
        EAccId=request.form['EAccId']
        Employee_Id=request.form['Employee_Id']
        Employee_Process=request.form['Employee_Process']
        Acc_Id=request.form['Acc_Id']
        cur=mysql.connection.cursor()
        sql="insert into emply_acc(EAccId,Employee_Id,Employee_Process,Acc_Id) value (%s,%s,%s,%s)"
        cur.execute(sql,[EAccId,Employee_Id,Employee_Process,Acc_Id])
        mysql.connection.commit()
        cur.close()       
        return {}
    return render_template("add.html") 
@app.route("/emplyacc/edit/<string:id>",methods=['GET','POST'])
def editEmplyacc(id):
    sql = 'SELECT * FROM emply_acc WHERE EAccId=%s'
    con = mysql.connection.cursor()
    con.execute(sql % (str(id)))
    res= con.fetchall()
    if request.method == 'POST':
        Employee_Id=request.form['Employee_Id']
        Employee_Process=request.form['Employee_Process']
        Acc_Id=request.form['Acc_Id']
        print(Employee_Id,Employee_Process,Acc_Id)
        con = mysql.connection.cursor()
        sql=("""
               UPDATE emply_acc
               SET Employee_Id=%s,Employee_Process=%s,Acc_Id=%s
               WHERE EAccId=%s
            """)
        con.execute(sql,[Employee_Id, Employee_Process,Acc_Id,id])
        mysql.connection.commit()
        con.close()
        return {}
    return render_template("edit.html",data=res[0])

@app.route("/emplyacc/delete/<string:id>",methods=['GET','POST'])
def deleteEmplyacc(id):
    con=mysql.connection.cursor()
    print(id)
    sql="delete from emply_acc where EAccId=%s"
    con.execute(sql % (str(id)))
    mysql.connection.commit()
    con.close()
    return{}
    


    

if __name__ == '__main__':
     app.secret_key='admin1234'
     app.run(debug=True,host='0.0.0.0',port=5000)
     
     