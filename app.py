from flask import Flask, render_template, request, redirect, session
import mysql.connector
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pandas as pd
import pickle
from flask import request, send_file
import pandas as pd
from flask_mail import Message, Mail
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# DB CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lead_system",
    charset="utf8"
)
cursor = db.cursor(dictionary=True)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectbased2k26@gmail.com'
app.config['MAIL_PASSWORD'] = 'stsb nann lpnx sskg'
app.config['MAIL_DEFAULT_SENDER'] = 'projectbased2k26@gmail.com'

mail = Mail(app)

import pickle

try:
    model = pickle.load(open("model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))
    print("✅ Model Loaded")
except:
    model = None
    encoders = None
    print("❌ Model NOT loaded")



# ================= DATA PREPROCESSING =================
def preprocess_data(df):

    df = df.copy()

    # Handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna("Unknown", inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

    # Encode categorical features
    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # Encode target
    target_encoder = LabelEncoder()
    df['Lead_Potential'] = target_encoder.fit_transform(df['Lead_Potential'])

    encoders['target'] = target_encoder

    return df


# ================= FEATURE ENGINEERING =================
def feature_engineering(df):

    df = df.copy()

    # Engagement Score
    df['Engagement_Score_New'] = (
        df['Time_Spent_Min'] * 0.4 +
        df['Pages_Visited'] * 0.3 +
        df['Clicks'] * 0.3
    )

    # Lead Score
    df['Lead_Score_New'] = (
        df['Engagement_Score_New'] * 0.5 +
        df['Followup_Count'] * 0.5
    )

    return df


# ================= TRAIN MODEL =================
def train_model():

    global model

    df = read_dataset()

    # Preprocessing
    df = preprocess_data(df)

    # Feature Engineering
    df = feature_engineering(df)

    # Split
    X = df.drop("Lead_Potential", axis=1)
    y = df["Lead_Potential"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scaling
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # ================= BASE MODELS =================

    xgb = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=8
    )

    lr = LogisticRegression(max_iter=1000)

    # ================= STACKING =================
    estimators = [
        ('xgb', xgb),
        ('rf', rf),
        ('lr', lr)
    ]

    stacking_model = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression()
    )

    # Train
    stacking_model.fit(X_train, y_train)

    # Predict
    y_pred = stacking_model.predict(X_test)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Model Performance")
    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)

    # Save model
    with open("model.pkl", "wb") as f:
        pickle.dump(stacking_model, f)

    model = stacking_model

    return acc


# ================= LOAD MODEL =================
def load_model():
    global model
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
    except:
        model = None


# ================= HOME =================
@app.route('/')
def home():
    return render_template("index.html")

# ================= ADMIN LOGIN =================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (u, p))
        admin = cursor.fetchone()

        if admin:
            session['admin'] = u
            return redirect('/admin_dashboard')
    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")


import pandas as pd

# ================= READ DATASET =================
def read_dataset():
    df = pd.read_csv("dataset.csv")
    return df

# ================= PROCESS 1 =================
@app.route('/process1')
def process1():
    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    # Remove target column (Lead_Potential)
    df_view = df.iloc[:, :-1]

    df_view = df_view.head(20)

    data = df_view.values.tolist()
    columns = df_view.columns.tolist()

    return render_template(
        'process1.html',
        data=data,
        columns=columns
    )

# ================= PROCESS 2 =================
@app.route('/process2')
def process2():
    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    # Remove target column
    df = df.iloc[:, :-1]

    summary = []

    for col in df.columns:
        summary.append([
            col,
            df[col].count(),
            str(df[col].dtype)
        ])

    return render_template(
        'process2.html',
        summary=summary
    )

# ================= FEATURE DEFINITIONS =================

NUMERICAL_FEATURES = [
    "Age",
    "Budget",
    "Experience_Years",
    "Time_Spent_Min",
    "Pages_Visited",
    "Clicks",
    "Engagement_Score",
    "Lead_Score",
    "Followup_Count"
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Location",
    "Education",
    "Course_Interest",
    "Occupation",
    "Source",
    "Device_Type",
    "Previous_Enquiry",
    "Email_Opened",
    "Email_Clicked",
    "Demo_Attended",
    "Webinar_Attended",
    "Preferred_Time",
    "Payment_Mode",
    "Discount_Response",
    "Call_Response"
]

TARGET = ["Lead_Potential"]

# ================= PROCESS 3 =================
@app.route('/process3')
def process3():
    if 'admin' not in session:
        return redirect('/admin')

    return render_template(
        'process3.html',
        numerical=NUMERICAL_FEATURES,
        categorical=CATEGORICAL_FEATURES,
        target=TARGET
    )

# ================= PROCESS 4 =================
@app.route('/process4')
def process4():
    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    df = df.head(40)

    data = df.values.tolist()
    columns = df.columns.tolist()

    return render_template(
        'process4.html',
        data=data,
        columns=columns
    )

# ================= PROCESS 5 =================
@app.route('/process5')
def process5():
    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    counts = df['Lead_Potential'].value_counts().to_dict()

    potential = counts.get("Potential", 0)
    not_potential = counts.get("Not Potential", 0)

    return render_template(
        "process5.html",
        potential=potential,
        not_potential=not_potential
    )

# VIEW USERS
@app.route('/view_users')
def view_users():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM marketing_manager")
    managers = cursor.fetchall()

    cursor.execute("SELECT * FROM telecaller")
    telecallers = cursor.fetchall()

    return render_template("view_users.html", students=students, managers=managers, telecallers=telecallers)

# ================= STUDENT =================
@app.route('/student_register', methods=['GET','POST'])
def student_register():
    if request.method == 'POST':
        data = (request.form['name'], request.form['email'], request.form['mobile'],
                request.form['username'], request.form['password'])

        cursor.execute("INSERT INTO students (name,email,mobile,username,password) VALUES (%s,%s,%s,%s,%s)", data)
        db.commit()
        return redirect('/student_login')
    return render_template("student_register.html")

@app.route('/student_login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        cursor.execute("SELECT * FROM students WHERE username=%s AND password=%s",(u,p))
        user = cursor.fetchone()

        if user:
            session['student'] = u
            return redirect('/student_dashboard')
    return render_template("student_login.html")

@app.route('/student_dashboard')
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route('/book_course', methods=['GET', 'POST'])
def book_course():
    if 'student' not in session:
        return redirect('/student_login')

    if request.method == 'POST':

        data = (
            request.form['full_name'],
            request.form['age'],
            request.form['gender'],
            request.form['location'],
            request.form['email'],
            request.form['phone'],

            request.form['education'],
            request.form['occupation'],
            request.form['experience_years'],

            request.form['course_interest'],
            request.form['budget'],
            request.form['payment_mode'],
            request.form['preferred_time'],

            request.form['device_type'],
            request.form['time_spent'],
            request.form['pages_visited'],
            request.form['click_count'],

            request.form['previous_enquiry'],
            request.form['demo_attended'],
            request.form['webinar_attended'],

            request.form['source'],
            request.form['email_opened'],
            request.form['email_clicked']
        )

        cursor.execute("""
        INSERT INTO course_bookings (
            full_name, age, gender, location, email, phone,
            education, occupation, experience_years,
            course_interest, budget, payment_mode, preferred_time,
            device_type, time_spent, pages_visited, click_count,
            previous_enquiry, demo_attended, webinar_attended,
            source, email_opened, email_clicked
        ) VALUES (%s,%s,%s,%s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s,%s,
                  %s,%s,%s,%s,
                  %s,%s,%s,
                  %s,%s,%s)
        """, data)

        db.commit()
        return "<script>alert('Course Booked Successfully');window.location='/student_dashboard'</script>"

    return render_template('book_course.html')
# ================= MARKETING MANAGER =================
@app.route('/manager_register', methods=['GET','POST'])
def manager_register():
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['email'], request.form['mobile'],
            request.form['company_name'], request.form['location'],
            request.form['company_type'], request.form['username'], request.form['password']
        )

        cursor.execute("""
            INSERT INTO marketing_manager 
            (name,email,mobile,company_name,location,company_type,username,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)

        db.commit()
        return redirect('/manager_login')

    return render_template("manager_register.html")

@app.route('/manager_login', methods=['GET','POST'])
def manager_login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        cursor.execute("SELECT * FROM marketing_manager WHERE username=%s AND password=%s",(u,p))
        user = cursor.fetchone()

        if user:
            session['manager'] = u
            return redirect('/manager_dashboard')
    return render_template("manager_login.html")

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template("manager_dashboard.html")

@app.route('/upload_data', methods=['GET','POST'])
def upload_data():
    if 'manager' not in session:
        return redirect('/manager_login')

    if request.method == 'POST':
        file = request.files['file']

        filename = file.filename.lower()

        # ✅ HANDLE BOTH CSV & EXCEL
        if filename.endswith('.csv'):
            df = pd.read_csv(file, encoding='latin1')   # fix unicode issue
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return "❌ Upload only CSV or Excel file"

        if len(df) < 20:
            return "⚠ Upload at least 20 rows!"

        df_original = df.copy()

        # DROP UNUSED
        df = df.drop(columns=["Lead_ID","Name","Phone_Number"], errors='ignore')

        # ENCODE
        for col in df.columns:
            if col in encoders:
                try:
                    df[col] = encoders[col].transform(df[col])
                except:
                    df[col] = 0   # handle unknown values

        # PREDICT
        preds = model.predict(df)
        probs = model.predict_proba(df)[:,1]

        df_original["Prediction"] = ["Potential" if p==1 else "Not Potential" for p in preds]
        df_original["Probability"] = (probs * 100).round(2)

        # PREPARE RESULT FOR TEMPLATE
        results = []

        for i,row in df_original.iterrows():

            prob = row["Probability"]

            risk = "High Potential" if row["Prediction"]=="Potential" else "Low Potential"

            summary = f"{row['Name']} shows {'strong' if prob>70 else 'moderate' if prob>50 else 'low'} interest based on engagement."

            results.append({
                "id": i+1,
                "name": row.get("Name"),
                "phone": row.get("Phone_Number"), 
                "prob": prob,
                "risk": risk,
                "summary": summary,
                "positive": ["High Engagement","Clicked Emails","Attended Demo"],
                "negative": ["Low Budget","Less Interaction"],
                "action": "Follow immediately" if prob>70 else "Send reminder"
            })
        session['results'] = results
        cursor.execute("SELECT username, email FROM telecaller")
        telecallers = cursor.fetchall()
        return render_template(
            "prediction_result.html",
            mode="bulk",
            results=results,
            telecallers=telecallers
        )

    return render_template("upload.html")


@app.route('/view_predictions')
def view_predictions():
    if 'manager' not in session:
        return redirect('/manager_login')

    search = request.args.get('search')
    risk = request.args.get('risk')

    query = "SELECT * FROM predictions WHERE 1=1"
    values = []

    # 🔍 SEARCH FILTER
    if search:
        query += " AND Name LIKE %s"
        values.append(f"%{search}%")

    # 🎯 RISK FILTER (based on Prediction column)
    if risk:
        if risk == "High Potential":
            query += " AND Prediction='Potential'"
        elif risk == "Low Potential":
            query += " AND Prediction='Not Potential'"

    cursor.execute(query, values)
    data = cursor.fetchall()

    # 👉 Convert DB → results format (IMPORTANT)
    results = []
    for i, row in enumerate(data):
        prob = row.get("Probability", 50)  # if not stored

        results.append({
            "id": i+1,
            "name": row.get("Name"),
            "phone": row.get("Phone_Number"), 
            "prob": prob,
            "risk": "High Potential" if row.get("Prediction") == "Potential" else "Low Potential",
            "summary": "Lead analysis based on engagement",
            "positive": [],
            "negative": [],
            "action": "Follow immediately" if prob > 70 else "Send reminder"
        })

    return render_template("view_predictions.html", results=results)

# ADD TELECALLER
@app.route('/add_telecaller', methods=['GET','POST'])
def add_telecaller():
    if request.method == 'POST':
        data = (
            request.form['name'], request.form['email'], request.form['mobile'],
            request.form['working_type'], request.form['working_time'],
            request.form['username'], request.form['password']
        )

        cursor.execute("""
            INSERT INTO telecaller 
            (name,email,mobile,working_type,working_time,username,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, data)

        db.commit()
        return redirect('/manager_dashboard')

    return render_template("add_telecaller.html")



import os

import os

@app.route('/export_and_send', methods=['POST'])
def export_and_send():

    filter_value = request.form.get('filter_value')
    telecaller_data = request.form.get('telecaller')

    if not telecaller_data:
        return "Please select telecaller"

    # split username + email
    telecaller_user, telecaller_email = telecaller_data.split("|")

    results = session.get('results', [])

    # 🔹 FILTER
    if filter_value != "all":
        filtered = [r for r in results if r['risk'] == filter_value]
    else:
        filtered = results

    if not filtered:
        return "No data to export"

    # 🔹 CREATE EXCEL
    df = pd.DataFrame(filtered)

    # clean columns
    df = df[['name','phone','prob','risk','summary','action']]

    filename = f"filtered_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    filepath = os.path.join("static", filename)

    df.to_excel(filepath, index=False)

    # 🔹 SAVE TO DB (IMPORTANT FIX)
    for r in filtered:
        cursor.execute("""
        INSERT INTO assigned_leads 
        (name, phone, prob, risk, summary, action, assigned_by, assigned_to)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            r['name'],
            r['phone'],
            r['prob'],
            r['risk'],
            r['summary'],
            r['action'],
            session.get('manager'),
            telecaller_user   # ✅ store username (FIXED)
        ))

    db.commit()

    # 🔹 SEND EMAIL (uses email correctly)
    try:
        msg = Message(
            subject="📊 Filtered Leads Assigned",
            recipients=[telecaller_email]
        )

        msg.body = f"""
Hello {telecaller_user},

You have been assigned new leads.

Filter: {filter_value}
Total Leads: {len(filtered)}

Please find the attached Excel file.

Regards,
Manager
"""

        with app.open_resource(filepath) as fp:
            msg.attach(
                filename,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                fp.read()
            )

        mail.send(msg)

    except Exception as e:
        print("Mail Error:", e)

    return send_file(filepath, as_attachment=True)

# ================= TELECALLER =================
@app.route('/telecaller_login', methods=['GET','POST'])
def telecaller_login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        cursor.execute("SELECT * FROM telecaller WHERE username=%s AND password=%s",(u,p))
        user = cursor.fetchone()

        if user:
            session['telecaller'] = u
            return redirect('/telecaller_dashboard')
    return render_template("telecaller_login.html")

@app.route('/telecaller_dashboard')
def telecaller_dashboard():
    if 'telecaller' not in session:
        return redirect('/telecaller_login')

    user = session['telecaller']

    cursor.execute("""
        SELECT * FROM assigned_leads
        WHERE assigned_to=%s OR assigned_to='telecaller'
        ORDER BY created_at DESC
    """, (user,))

    leads = cursor.fetchall()

    return render_template("telecaller_dashboard.html", leads=leads)

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'telecaller' not in session:
        return redirect('/telecaller_login')

    lead_id = request.form.get('lead_id')
    status = request.form.get('status')
    call_count = request.form.get('call_count')

    # safety (if empty)
    if not call_count:
        call_count = 0

    cursor.execute("""
        UPDATE assigned_leads 
        SET status=%s, call_count=%s, updated_by=%s
        WHERE id=%s
    """, (
        status,
        call_count,
        session.get('telecaller'),
        lead_id
    ))

    db.commit()

    return redirect('/telecaller_dashboard')

@app.route('/manager_lead_status')
def manager_lead_status():
    if 'manager' not in session:
        return redirect('/manager_login')

    cursor.execute("""
        SELECT * FROM assigned_leads
        ORDER BY id DESC
    """)

    leads = cursor.fetchall()

    return render_template("manager_lead_status.html", leads=leads)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
