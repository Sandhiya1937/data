from flask import Flask, jsonify
import fakeredis as redis
import ast
import time

app = Flask(__name__)
redis_client = redis.FakeStrictRedis(decode_responses=True)

def get_blog_post_from_db(post_id):
    time.sleep(2)  # Simulate database delay
    return {"post_id": post_id, "title": f"Post {post_id}", "content": "Sample blog content."}

@app.route('/')
def home():
    return "Welcome to the Blog API!"

@app.route('/post/<post_id>')
def get_post(post_id):
    cached_post = redis_client.get(post_id)
    if cached_post:
        return jsonify({"source": "cache", "data": ast.literal_eval(cached_post)})
    post = get_blog_post_from_db(post_id)
    redis_client.setex(post_id, 10, str(post))
    return jsonify({"source": "database", "data": post})

@app.route('/clear-cache/<post_id>')
def clear_cache(post_id):
    redis_client.delete(post_id)
    return jsonify({"message": f"Cache for post {post_id} cleared."})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)   # <--- important


#pip install flask fakeredis
#python app.py
#http://127.0.0.1:5000-welcome
#http://127.0.0.1:5000/post/1-within 10 sec cache and database will alter
#http://127.0.0.1:5000/clear-cache

Table Category {
    Category_ID INT [pk]
    Category_Name VARCHAR(100)
}

Table Book {
    Book_ID INT [pk]
    Title VARCHAR(255)
    Author VARCHAR(255)
    Publisher VARCHAR(255)
    ISBN VARCHAR(20)
    Category_ID INT
    Price DECIMAL(10, 2)
    Year_of_Publication YEAR
}

Table Member {
    Member_ID INT [pk]
    First_Name VARCHAR(100)
    Last_Name VARCHAR(100)
    Email VARCHAR(100)
    Phone_Number VARCHAR(15)
    Address TEXT
    Membership_Date DATE
}

Table Staff {
    Staff_ID INT [pk]
    First_Name VARCHAR(100)
    Last_Name VARCHAR(100)
    Email VARCHAR(100)
    Phone_Number VARCHAR(15)
    Role VARCHAR(50)
    Date_of_Hire DATE
}

Table Loan {
    Loan_ID INT [pk]
    Book_ID INT
    Member_ID INT
    Loan_Date DATE
    Return_Date DATE
    Due_Date DATE
}

Table Reservation {
    Reservation_ID INT [pk]
    Book_ID INT
    Member_ID INT
    Reservation_Date DATE
    Status VARCHAR(50)
}

Ref: Book.Category_ID > Category.Category_ID
Ref: Loan.Book_ID > Book.Book_ID
Ref: Loan.Member_ID > Member.Member_ID
Ref: Reservation.Book_ID > Book.Book_ID
Ref: Reservation.Member_ID > Member.Member_ID


-- Skip CREATE DATABASE and USE commands since many online compilers don't allow them

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price > 0)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    UserID INT NOT NULL,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE OrderLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    Message VARCHAR(255)
);

-- Manually inserting a log (since we can't use triggers)
INSERT INTO Users (UserID, UserName, Email) 
VALUES (1, 'John Doe', 'john@example.com');

INSERT INTO Products (ProductID, ProductName, Price) 
VALUES (1, 'Laptop', 800.00);

INSERT INTO Orders (OrderID, UserID) 
VALUES (1, 1);

INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity) 
VALUES (1, 1, 1, 2);

-- Manually adding log entry
INSERT INTO OrderLog (Message) 
VALUES ('Order 1 placed on 2025-01-06 10:00:00');

-- Query to view data
SELECT * FROM Users;
SELECT * FROM Products;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
SELECT * FROM OrderLog;