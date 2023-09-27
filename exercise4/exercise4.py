import sqlite3

def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY,
                    Title TEXT NOT NULL,
                    Author TEXT NOT NULL,
                    ISBN TEXT NOT NULL,
                    Status TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY,
                    BookID INTEGER NOT NULL,
                    UserID INTEGER NOT NULL,
                    ReservationDate TEXT NOT NULL,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID)
                )''')

    conn.commit()
    conn.close()
def add_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    c.execute("SELECT COUNT(*) FROM Books")
    book_id = c.fetchone()[0] + 1
    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, 'Available')", (book_id, title, author, isbn))

    conn.commit()
    conn.close()
    print("Book added successfully!")
def find_book_by_id():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter the BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is not None:
        c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
        reservation = c.fetchone()

        if reservation is not None:
            c.execute("SELECT * FROM Users WHERE UserID=?", (reservation[2],))
            user = c.fetchone()

            print("Book Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("Reserved by:", user[1])
            print("Reservation Date:", reservation[3])
        else:
            print("Book Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("Not reserved by anyone.")
    else:
        print("Book not found in the database.")

    conn.close()
def find_reservation_status():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    search_text = input("Enter the BookID, UserID, ReservationID, or Title: ")

    if search_text.startswith("LB"):
        c.execute("SELECT * FROM Books WHERE BookID=?", (search_text,))
        book = c.fetchone()

        if book is not None:
            print("Book Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            c.execute("SELECT * FROM Reservations WHERE BookID=?", (search_text,))
            reservation = c.fetchone()

            if reservation is not None:
                print("Reserved by UserID:", reservation[2])
                print("Reservation Date:", reservation[3])
            else:
                print("Not reserved by anyone.")
        else:
            print("Book not found in the database.")
    elif search_text.startswith("LU"):
        c.execute("SELECT * FROM Users WHERE UserID=?", (search_text,))
        user = c.fetchone()

        if user is not None:
            print("User Name:", user[1])
            print("Email:", user[2])
            c.execute("SELECT * FROM Reservations WHERE UserID=?", (search_text,))
            reservations = c.fetchall()

            if reservations:
                for reservation in reservations:
                    c.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
                    book = c.fetchone()
                    print("Book Title:", book[1])
                    print("Author:", book[2])
                    print("ISBN:", book[3])
                    print("Status:", book[4])
                    print("Reservation Date:", reservation[3])
            else:
                print("No reservations made by this user.")
        else:
            print("User not found in the database.")
    elif search_text.startswith("LR"):
        c.execute("SELECT * FROM Reservations WHERE ReservationID=?", (search_text,))
        reservation = c.fetchone()

        if reservation is not None:
            c.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
            book = c.fetchone()
            print("Book Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("Reserved by UserID:", reservation[2])
            print("Reservation Date:", reservation[3])
        else:
            print("Reservation not found in the database.")
    else:
        c.execute("SELECT * FROM Books WHERE Title LIKE ?", ('%' + search_text + '%',))
        books = c.fetchall()

        if books:
            for book in books:
                print("BookID:", book[0])
                print("Author:", book[2])
                print("ISBN:", book[3])
                print("Status:", book[4])
                c.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
                reservation = c.fetchone()

                if reservation is not None:
                    print("Reserved by UserID:", reservation[2])
                    print("Reservation Date:", reservation[3])
                else:
                    print("Not reserved by anyone.")
        else:
            print("Book not found in the database.")

    conn.close()
def find_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Books")
    books = c.fetchall()

    if books:
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            c.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
            reservation = c.fetchone()

            if reservation is not None:
                c.execute("SELECT * FROM Users WHERE UserID=?", (reservation[2],))
                user = c.fetchone()

                print("Reserved by UserID:", user[0])
                print("Reservation Date:", reservation[3])

            print("-----------------------")
    else:
        print("No books found in the database.")

    conn.close()
def update_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter the BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is not None:
        print("Book found! Enter the new details:")

        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        status = input("Status: ")
        c.execute("UPDATE Books SET Title=?, Author=?, ISBN=?, Status=? WHERE BookID=?", (title, author, isbn, status, book_id))
        c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
        reservation = c.fetchone()

        if reservation is not None:
            c.execute("UPDATE Reservations SET ReservationDate=?, BookID=? WHERE ReservationID=?", (reservation[3], book[0], reservation[0]))
            c.execute("UPDATE Users SET UserID=?, Name=?, Email=? WHERE UserID=?", (reservation[2], reservation[2], reservation[2]))

        conn.commit()
        conn.close()
        print("Book details updated successfully!")
    else:
        print("Book not found in the database.")
def delete_book():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    book_id = input("Enter the BookID: ")
    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is not None:
        c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
        reservation = c.fetchone()
        if reservation is not None:
            c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
        c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))

        conn.commit()
        conn.close()
        print("Book deleted successfully!")
    else:
        print("Book not found in the database.")
def main():
    create_database()

    while True:
        print("\nLIBRARY MANAGEMENT SYSTEM")
        print("1. Add a new book to the database")
        print("2. Find a book's detail based on BookID")
        print("3. Find a book's reservation status based on BookID, Title, UserID, and ReservationID")
        print("4. Find all the books in the database")
        print("5. Modify/update book details based on its BookID")
        print("6. Delete a book based on its BookID")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            find_book_by_id()
        elif choice == '3':
            find_reservation_status()
        elif choice == '4':
            find_all_books()
        elif choice == '5':
            update_book()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()