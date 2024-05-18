from flask import Flask , jsonify, request ,render_template, url_for, redirect
import mysql.connector
import smtplib
from email.message import EmailMessage
from flask_cors import CORS, cross_origin


app = Flask(__name__)

CORS(app)  # Initialize CORS with your Flask app
#MYSQL CONFIG
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'auram',
}



# Create MySQL database connection
try:
    connection = mysql.connector.connect(**db_config)
    
except:
    print('server down')

#home default
@cross_origin
@app.route("/", methods = ["GET"])
def helloMessage():
    return render_template('index.html')


#fetchUser
@cross_origin
@app.route('/users', methods = ['GET'])
def fetchUser():
    if request.method == 'GET':
        

        cursor = connection.cursor()
        cursor.execute('SELECT user_name, email FROM user_registration')
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    
    
#registet user
@cross_origin
@app.route('/registration', methods = ['POST'])
def user_registration():
    if request.method == 'POST':
        
            #id = 22
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_registration WHERE email = (%s)', (email,) )
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            
            return jsonify({'message':'user already exist'})
        
        else:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_registration (user_name,email,password) VALUES (%s, %s, %s)" , (user_name, email, password))
            #cursor.execute("SET @details_id = LAST_INSERT_ID()")
            connection.commit()
            cursor.close
            return jsonify({'message':'registration successful'})
        
        
        
#login user
@cross_origin
@app.route('/login', methods = ['POST'])
def user_login():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
        
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user_registration WHERE email = (%s)', (email,) )
        existing_user = cursor.fetchone()
        cursor.close()
        
        
        if (existing_user):
            db_password = existing_user[3]
            #print(existing_user[3])
            if (db_password == password):
                
                return jsonify({'message':'logged in succesfuly'})
            else:
                return jsonify({'message':'wrong password'})
            
        else:
            return jsonify({'message':'you have not registered please register'})
                

#user_details
@cross_origin
@app.route("/details", methods = ["POST"])
def user_details():
    if request.method == 'POST':
        full_name = request.json['name']
        email_address = request.json['email']
        phone_number = request.json['phone_number']
        nationality = request.json['nationality']
        time_to_travel = request.json['time_to_travel']
        time_to_spend = request.json['time_to_spend']
        
        #checkbox Interests
        #interest = request.form.getlist('interests')
        #specific_experience= ', '.join(interest) if interest else None
        interests = request.json.get('interests',[])
        specific_experience = ''
        
        for interest in interests:
            specific_experience += interest + ' '
            
        
        adults = request.json.get('adults', '')
        children = request.json.get('children', '')
        childrens_age = request.json.get('childrens_age', '')
        #checkbox Accommodation
        accommodations = request.json.get('accommodation', [])
        comfort_level = ''
        
        for accommodation in accommodations:
            comfort_level += accommodation + ','
        #accommodation = request.form.getlist('accommodation')
        

        #radio Tour type
        travel_preference = request.json.get('travel_preference','')
        
        message = request.json.get('message','')
        
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO user_details (
        
        full_name,
        email_address,
        whatsapp_number,
        nationality,
        ideal_travel_time,
        time_to_spend,
        specific_experience,
        travelling_adults,
        travelling_with_child,
        childrens_age,
        comfort_level,
        travel_preference,
        message
        )
        VALUES (
             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        
        full_name,
        email_address,
        phone_number,
        nationality,
        time_to_travel,
        time_to_spend,
        specific_experience,
        adults,
        children,
        childrens_age,
        comfort_level,
        travel_preference,
        message
    ))


            
    cursor.close()
        
    return jsonify({'message':'details posted succssess'})
    #return redirect('/')



## EMAIL FLASK API


# Email server configuration
EMAIL_ADDRESS = 'levygesy123@gmail.com'
EMAIL_PASSWORD = 'zkzj lagg afad cqza'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587



# //-------------EMAIL--------------------//
@cross_origin
@app.route('/send_email', methods=['POST'])
def send_email():
    # Get email and message from the request
    sender_email = request.form.get('email')
    message = request.form.get('message')

    if not sender_email or not message:
        return jsonify({'error': 'Email and message are required'}), 400

    # Create email message
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Message From Client!'
    msg['From'] = sender_email
    msg['To'] = EMAIL_ADDRESS

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        return jsonify({'error': 'Failed to send email'}), 500

    return jsonify({'message': 'Email sent successfully'}), 200

    
    
    
    

#ADMINISTRATION

#login admin
@cross_origin
@app.route('/login', methods = ['POST'])
def admin_login():
    if request.method == 'POST':
        
        username = request.form['email']
        password = request.form['password']
        
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM admin_login WHERE email = (%s)', (username,) )
        existing_user = cursor.fetchone()
        cursor.close()
        
        
        if (existing_user):
            db_password = existing_user[3]
            #print(existing_user[3])
            if (db_password == password):
                
                return jsonify({'message':'logged in succesfuly'})
            else:
                return jsonify({'message':'wrong password'})
            
        else:
            return jsonify({'message':'you have not registered ple'})
        
        
## GET USERS
@cross_origin
@app.route('/admin', methods = ['GET'])
def fetch_users():
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_details")
        data = cursor.fetchall()
        selected_users = data
        cursor.close()
        
        return render_template('admin.html',selected_users = selected_users)
    
##DELETE USERS
@cross_origin
@app.route('/admin/delete/<int:id>')
def delete_users(id):

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_details WHERE id = (%s)', (id,))
    selected_user = cursor.fetchone()
    
    
    if selected_user:
        # If user found, execute DELETE query to remove them from the database
        
        cursor.execute('DELETE FROM user_details WHERE id = %s', (id,))
        connection.commit()
        cursor.close()
        #return jsonify({'message': f'User with ID {id} deleted successfully'})
        return redirect('/admin')
    else:
        cursor.close()
        return jsonify({'error': 'User not found'}), 404
    
##EDIT USERS
@cross_origin
@app.route('/admin/edit/<int:id>', methods=['POST', 'GET'])
def edit_users(id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_details WHERE id = %s', (id,))
    selected_user = cursor.fetchone()

    if request.method == 'POST':
         #checkbox Interests
        interest = request.form.getlist('interests')
        specific_experience = ', '.join(interest) if interest else None
        
        #checkbox Accommodation
        accommodation = request.form.getlist('accommodation')
        comfort_level = ",".join(accommodation) if accommodation else None
        
        details_update= (
            request.form.get('id', ''),
            request.form.get('name', ''),
            request.form.get('email', ''),
            request.form.get('phone_number', ''),
            request.form.get('nationality', ''),
            request.form.get('time_to_travel', ''),
            specific_experience,
            request.form.get('adults', ''),
            request.form.get('children', ''),
            comfort_level,
            request.form.get('tour_type', ''),
            request.form.get('message', '')
        )
        
        cursor.execute("""
            UPDATE user_details SET
            id = %s, 
            full_name = %s,
            email_address = %s,
            whatsapp_number = %s,
            nationality = %s,
            ideal_travel_time = %s,
            specific_experience = %s,
            travelling_adults = %s,
            travelling_with_child = %s,
            comfort_level = %s,
            travel_preference = %s,
            message = %s
            WHERE id = %s
        """, (*details_update, id))
        
        connection.commit()
        cursor.close()
        return redirect('/admin')
    
    return render_template('updateForm.html', y=selected_user)

        
        
if __name__ == '__main__':
    app.run(debug=True)