#Anuvi Batra
#eLibrary Project

import mysql.connector

eLibraryDB = "elib"
print('Connecting to eLibrary database...')
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anuvi111",
    database="elib"
)

mycursor = mydb.cursor()

def listAvailableBooks(mycursor):
    print("{0:<5}".format('ID'), "{0:<20}".format('NAME'), "{0:<20}".format('AUTHOR'), "{0:<20}".format('QTY'))
    sql = 'SELECT * FROM BOOKS'
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for x in result:
        print("{0:<5}".format(x[0]), "{0:<20}".format(x[1]), "{0:<20}".format(x[2]), "{0:<20}".format(x[3]))

def addNewBook(mycursor):
    print('Add new book:')
    bname = input("Enter name: ")
    bauthor = input("Enter author: ")
    qty = int(input("Enter quantity: "))
    sql = 'INSERT INTO BOOKS (BNAME, BAUTHOR, QTY) VALUES ("' + bname.upper() + '","' + bauthor.upper() + '",' + str(qty) + ')'
    mycursor.execute(sql)
    mydb.commit()

def listStudents(mycursor):
    print("{0:<5}".format('RNO'), "{0:<20}".format('FNAME'), "{0:<20}".format('LNAME'), "{0:<20}".format('GRADE'),"{0:20}".format('SECTION'))
    sql = 'SELECT * FROM STUDENTS'
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for x in result:
        print("{0:<5}".format(x[0]), "{0:<20}".format(x[1]), "{0:<20}".format(x[2]), "{0:<20}".format(x[3]),"{0:20}".format(x[4]))

def addStudent(mycursor):
    print('Add new student: ')
    rno=int(input('Enter Roll Number (0-9): '))
    fname=input('Enter First Name: ')
    lname=input('Enter Last Name: ')
    grade=int(input('Enter Grade (1-12): '))
    section=input('Enter Section (A-Z): ')
    sql = 'INSERT INTO STUDENTS VALUES (' + \
          str(rno) + ',"' + \
          fname.upper() + '","' + \
          lname.upper() + '",' + \
          str(grade) + ',"' + \
          section.upper() + '")'
    #print(sql)
    mycursor.execute(sql)
    mydb.commit()

def deleteStudent(mycursor):
    no=int(input('Enter Roll No: '))
    rno=str(no)
    sql='DELETE FROM STUDENTS WHERE RNO=' + rno
    mycursor.execute(sql)
    mydb.commit()

def deleteBook(mycursor):
    book_name=input('Enter Book Name: ')
    sql='DELETE FROM BOOKS WHERE BNAME="' + book_name.upper() + '"'
    mycursor.execute(sql)
    mydb.commit()

def bookAvailability(mycursor, book_name):
    if book_name == None:
        book_name=input('Enter Book Name: ')

    sql = 'SELECT ID, QTY FROM BOOKS WHERE BNAME="' + book_name.upper() + '"'
    mycursor.execute(sql)
    result = mycursor.fetchall()
    bookID = 0
    numBooks = 0
    for x in result:
        bookID = x[0]
        numBooks = x[1]
    if numBooks == 0:
        print("Sorry, this book is not available in the library.")
        return False
    else:
        iBooksSql = 'SELECT COUNT(*) FROM IBOOKS WHERE ID=' + str(bookID)
        mycursor.execute(iBooksSql)
        iResult = mycursor.fetchall()
        issuedBookCount = 0
        for y in iResult:
            issuedBookCount = y[0]
        if issuedBookCount < numBooks:
            print("This book is available in the library.")
            return True
        else:
            query = 'SELECT MIN(RETURN_DATE) FROM IBOOKS WHERE ID=' + str(bookID)
            mycursor.execute(query)
            r = mycursor.fetchall()
            a = ''
            for z in r:
                a=str(z[0])
            print("Sorry, all copies of this book are presently issued to students. Earliest available after", a)
            return False

def issueBook(mycursor):
    student_roll_no = int(input('Enter Student Roll No: '))
    sql = 'SELECT COUNT(*) FROM STUDENTS WHERE RNO=' + str(student_roll_no)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    rollNoValid = False
    for x in result:
        if x[0] == 1:
            rollNoValid = True
            break
    if rollNoValid == False:
        print('Invalid Roll No.')
    else:
        book_name=input('Enter Book Name: ')
        bookAvailable = bookAvailability(mycursor, book_name)
        if bookAvailable == True:
            booksSql = 'SELECT ID FROM BOOKS WHERE BNAME="' + book_name + '"'
            mycursor.execute(booksSql)
            bResult = mycursor.fetchall()
            bookID = 0
            for y in bResult:
                bookID = y[0]

            issueBookSql = 'INSERT INTO IBOOKS VALUES (' + str(bookID) + ',' + str(student_roll_no) + ', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY))'
            mycursor.execute(issueBookSql)
            mydb.commit()

def listIssuedBooks(mycursor):
    print("{0:<5}".format('ID'), "{0:<20}".format('RNO'), "{0:<20}".format('ISSUED_DATE'), "{0:<20}".format('RETURN_DATE'))
    issuedbookssql='SELECT * FROM IBOOKS'
    mycursor.execute(issuedbookssql)
    result=mycursor.fetchall()
    for z in result:
        print("{0:<5}".format(z[0]), "{0:<20}".format(z[1]), "{0:<20}".format(str(z[2])), "{0:<20}".format(str(z[3])))

def returnBook(mycursor):
    returnBookName=input('enter book name: ')
    returnbookRNO=int(input('enter student roll no.: '))
    returnbooksSql = 'SELECT ID FROM BOOKS WHERE BNAME="' + returnBookName.upper() + '"'
    mycursor.execute(returnbooksSql)
    returnbookResult = mycursor.fetchall()
    for d in returnbookResult:
        returnbookID = d[0]
        returnsql='DELETE FROM IBOOKS WHERE ID=' + str(returnbookID) + ' AND RNO=' + str(returnbookRNO) + ''
        mycursor.execute(returnsql)
        mydb.commit()

def bookPastDueDate(mycursor):
    bookspastdue= 'SELECT * FROM IBOOKS WHERE RETURN_DATE <= DATE_ADD(now(), INTERVAL -1 DAY);'
    mycursor.execute(bookspastdue)
    dueresult=mycursor.fetchall()
    print("{0:<5}".format('ID'), "{0:<20}".format('RNO'), "{0:<20}".format('ISSUED_DATE'), "{0:<20}".format('RETURN_DATE'))
    for p in dueresult:
        print("{0:<5}".format(p[0]), "{0:<20}".format(p[1]), "{0:<20}".format(str(p[2])), "{0:<20}".format(str(p[3])))


def print_menu():
    print('0. Print menu options')
    print('1. List available books in library')
    print('2. Add new book')
    print('3. Delete a book')
    print('4. List all issued books')
    print('5. Check book availability')
    print('6. Issue a book')
    print('7. Return a book')
    print('8. List books that are past due date')
    print('9. List students')
    print('10.Add student')
    print('11. Delete student')

print_menu()

while True:
    print()
    print()

    request = input('Select option: ')
    try:
        request = int(request)

        if request == 0:
            print_menu()

        elif request == 1:
            listAvailableBooks(mycursor)

        elif request == 2:
            addNewBook(mycursor)

        elif request == 3:
            deleteBook(mycursor)

        elif request == 4:
            listIssuedBooks(mycursor)

        elif request == 5:
            bookAvailability(mycursor, None)

        elif request == 6:
            issueBook(mycursor)

        elif request == 7:
            returnBook(mycursor)

        elif request == 8:
            bookPastDueDate(mycursor)

        elif request == 9:
            listStudents(mycursor)

        elif request == 10:
            addStudent(mycursor)

        elif request == 11:
            deleteStudent(mycursor)

        else:
            print('Invalid option, try again.')

    except:
        print('Invalid option, try again.')









