import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="Jahnavi@2004",
    database="quiz_system"
)
cursor = conn.cursor(buffered=True)

def admin_login():
    username = input("Enter Admin Username: ")
    password = input("Enter Password: ")
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    if cursor.fetchone():
        print("\n✅ Admin Login Successful!\n")
        admin_menu()
    else:
        print("❌ Invalid credentials!\n")

def add_question():
    tech = input("Enter Technology (Python/MySQL/etc): ")
    q = input("Enter Question: ")
    o1 = input("Option 1: ")
    o2 = input("Option 2: ")
    o3 = input("Option 3: ")
    o4 = input("Option 4: ")
    ans = int(input("Correct Option (1-4): "))

    cursor.execute(
        "INSERT INTO questions (technology, question, option1, option2, option3, option4, answer) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (tech, q, o1, o2, o3, o4, ans)
    )
    conn.commit()
    print("✅ Question added successfully!\n")

def modify_question():
    qid = input("Enter Question ID to modify: ")
    new_q = input("Enter new Question: ")
    cursor.execute("UPDATE questions SET question=%s WHERE qid=%s", (new_q, qid))
    conn.commit()
    print("✅ Question updated successfully!\n")

def delete_question():
    qid = input("Enter Question ID to delete: ")
    cursor.execute("DELETE FROM questions WHERE qid=%s", (qid,))
    conn.commit()
    print("✅ Question deleted successfully!\n")

def view_all_questions():
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    for q in questions:
        print(f"\nQuestion ID: {q[0]}")
        print(f"Technology: {q[1]}")
        print(f"Question: {q[2]}")
        print(f"A. {q[3]}")
        print(f"B. {q[4]}")
        print(f"C. {q[5]}")
        print(f"D. {q[6]}")
        print(f"Correct Option: {q[7]}")
    
def view_user_details():
    cursor.execute("SELECT * FROM users ORDER BY score DESC")
    users = cursor.fetchall()
    for u in users:
        print(f"\nUsername: {u[1]}")
        print(f"Mobile: {u[2]}")
        print(f"Score: {u[3]}")
        print(f"Quiz Time: {u[4]}")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Question")
        print("2. Modify Question")
        print("3. Delete Question")
        print("4. View All Questions")
        print("5. View All User Details")
        print("6. Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            add_question()
        elif choice == '2':
            modify_question()
        elif choice == '3':
            delete_question()
        elif choice == '4':
            view_all_questions()
        elif choice == '5':
            view_user_details()
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice!")

# ---------------- USER FUNCTIONS ---------------- #
def user_login():
    username = input("Enter Username: ")
    mobile = input("Enter Mobile Number: ")
    print("\n✅ Login Successful!\n")
    user_menu(username, mobile)

def take_quiz(username, mobile):
    tech = input("Select Technology (Python/Mysql/etc): ")
    cursor.execute("SELECT * FROM questions WHERE technology=%s", (tech,))
    questions = cursor.fetchall()
    
    if not questions:
        print("❌ No questions found for this technology.")
        return

    score = 0
    for q in questions:
        print(f"\nQ{q[0]}: {q[2]}")
        print(f"1. {q[3]}\n2. {q[4]}\n3. {q[5]}\n4. {q[6]}")
        ans = int(input("Enter your answer (1-4): "))
        if ans == q[7]:
            score += 1


    print(f"\n✅ Quiz Completed! Your Score: {score}/{len(questions)}")
    cursor.execute(
        "INSERT INTO users (username, mobile, score, quiz_time) VALUES (%s,%s,%s,%s)",
        (username, mobile, score, datetime.now())
    )
    conn.commit()

def highest_score():
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 3")
    print("\n🏆 Top 3 Highest Scores:")
    for i, row in enumerate(cursor.fetchall(), start=1):
        print(f"{i}. {row[0]} - {row[1]}")

def user_menu(username, mobile):
    while True:
        print("\n--- User Menu ---")
        print("1. Take Quiz")
        print("2. Highest Scores")
        print("3. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            take_quiz(username, mobile)
        elif choice == '2':
            highest_score()
        elif choice == '3':
            break
        else:
            print("❌ Invalid choice!")

# ---------------- MAIN PROGRAM ---------------- #
def main():
    while True:
        print("\n=== QUIZ SYSTEM ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        ch = input("Enter choice: ")
        if ch == '1':
            admin_login()
        elif ch == '2':
            user_login()
        elif ch == '3':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

main()
