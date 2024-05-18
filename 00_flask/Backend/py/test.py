from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'auram',
}

# Create MySQL database connection
connection = mysql.connector.connect(**db_config)

@app.route('/')
def index():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    cursor.close()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)
'''
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
   
)
CREATE TABLE user_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    city VARCHAR(255),
    route VARCHAR(255),
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');
-- Get the auto-generated user_id of the inserted user
SET @user_id = LAST_INSERT_ID();

-- Insert user details with the corresponding user_id
INSERT INTO user_details (user_id, city, route, address) VALUES (@user_id, 'New York', 'Main Street', '1234 Example St');
'''