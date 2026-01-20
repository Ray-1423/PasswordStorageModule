# make a password script with a simple ui that will just take a password hash it and store it securely
# essentially a login page and store these hash passwords using bcrypt in a sqlite db
# optionally also add a steg utility in a separate module within this folder
import bcrypt
import sqlite3

#taking input - use a gui for this later
def inputForFirstTime(username, password):
    # hashing password
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, salt)

    # storing password
    storeInDB(username, hashed_password)

def storeInDB(username, password):
    stringpass = password.decode("utf-8") if isinstance(password, bytes) else str(password)
    # We want to send it w/ username to a sqlite db to be stored 
    conn = sqlite3.connect("C:\\Examplefilepath\\users.db")
    cursor = conn.cursor()

    # checking if the user is already in the db
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result is None:
    # inserting the user into the db if not there
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, stringpass))
    else: # updating if already there
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (stringpass, username))

    # Commit and close
    conn.commit()
    conn.close()

def main():
    conn = sqlite3.connect("C:\\Users\\rayaa\\OneDrive\\Documents\\burgershop\\users.db")
    cursor = conn.cursor()
    # create db if it doesn't exist
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    username = input("Enter a username: ")
    # query database and see if username exists: if so move to entering password if not ask if they want to make an account
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        print("This username does not exist\n")
        makeAnAccount = input("Would you like to make an account? y/n: ")
        if makeAnAccount == "y":
            confirmation = input("You have selected that you would like to make an account are you sure? (if so you will be asked to input a valid password) y/n: ")
            if confirmation == "n":
                "Okay goodbye!"
                return
            password = input("Enter a password: ")
            inputForFirstTime(username, password)
            conn.commit()
            conn.close()
            print("\nYour account has been created!")
            return
        else:
            "Okay goodbye!"
            conn.commit()
            conn.close()
            return
    else:
        print("\n This is a valid username enter the password below")
        password = input("Enter your password here: ")
        # query if the password is correct
        storedhash = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), storedhash.encode('utf-8')):
            print("Password verified!")
            conn.commit()
            conn.close()
            return
        else:
            print("Incorrect password.")
    conn.commit()
    conn.close()
main()
