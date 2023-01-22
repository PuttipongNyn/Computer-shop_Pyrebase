import pyrebase
from firebase_admin import credentials, firestore, auth
import firebase_admin, pyrebase, G13_email

credpath = r"E:\Workspace\Computer Shop\computer-shop-b108c-firebase-adminsdk-8ayyh-9f0a94dab6.json"
login = credentials.Certificate(credpath)

firebaseConfig = {
  'apiKey': "AIzaSyAeIpWFDocsnDtC_cPqaxv6fcM8D6qSm6I",
  'authDomain': "computer-shop-b108c.firebaseapp.com",
  'databaseURL': "https://computer-shop-b108c-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "computer-shop-b108c",
  'storageBucket': "computer-shop-b108c.appspot.com",
  'messagingSenderId': "217551541946",
  'appId': "1:217551541946:web:5cec0d7777c19376881483"
}
firebase = pyrebase.initialize_app(firebaseConfig)
dbs = firebase.database() #realtime
auth = firebase.auth()
firebase_admin.initialize_app(login)
db = firestore.client() #firestore

#Create Product in Realtime Database
def addProduct():
  choose = input('=============== Type to add ===============\n1.GRAPHIC CARD\n2.CPU\n3.MAINBOARD\n4.RAM\n5.POWER SUPPLY\nSelect: ')
  if choose == '1':
    type = 'GPU'
  elif choose == '2':
    type = 'CPU'
  elif choose == '3':
    type = 'MB'
  elif choose == '4':
    type = 'RAM'
  elif choose == '5':
    type = 'PSU'
  print('=============== ',type,' ===============')
  Product = input('Enter Product : ')
  ID = input('Enter ID : ')
  Price = input('Enter Price : ')
  data = {'ID': ID, 'Price': Price}
  datas = {'Name': Product, 'Price': Price}
  dbs.child('Storage').child(type).child(Product).set(data)
  dbs.child('Product').child(type).child(ID).set(datas)
  print('Add product Complete')
  ch = input('Do you want to add another Item[y/n] : ')
  if ch == 'y':
    addProduct()
  else:
    admin()

def findProduct():
    while True:
        name = input('=============== Find Customer Product ===============\nEnter customer name : ')
        findData = db.collection('customers').where('Name', '==', name).get()
        for data in findData:
            print(data.to_dict())
            if data == None:
                print('Customer name not found!')
        ch = input('Do you want to find another Customer product?[y/n] : ')
        if ch == 'y':
            findProduct()
        else:
            admin()

def customerProduct():
    while True:
        findData = db.collection('customers').where('Name', '==', name).get()
        for data in findData:
            print(data.to_dict(),'\n')
            if data == None:
                print('Customer name not found!')
        shopping()

def deleteCus():
  print("=============== Delete Customer ===============")
  while True:
    name = input('Enter customer name : ')
    findData = db.collection('customers').where('Name', '==', name).get()
    for data in findData:
        print(data.to_dict())
        confirm = input('Are you sure ? [y/n] : ')
        if confirm == 'y':
          db.collection('customers').document(name).update({'Product':firestore.DELETE_FIELD})
          db.collection('customers').document(name).update({'Price':firestore.DELETE_FIELD})
          db.collection('customers').document(name).update({'Total':firestore.DELETE_FIELD})
          print("Remove Complete")
        else:
          admin()

        if data == None:
            print('Customer name not found!')
    ch = input('Do you want to delete another customer?[y/n] : ')
    if ch == 'y':
         deleteCus()
    else:
        admin()        

def deleteFromCus():
  print("=============== Delete From Customer ===============")
  while True:
    findData = db.collection('customers').where('Name', '==', name).get()
    for data in findData:
        print(data.to_dict())
        confirm = input('Are you sure ? [y/n] : ')
        if confirm == 'y':
          db.collection('customers').document(name).update({'Product':firestore.DELETE_FIELD})
          db.collection('customers').document(name).update({'Price':firestore.DELETE_FIELD})
          db.collection('customers').document(name).update({'Total':firestore.DELETE_FIELD})
          print("Remove Complete")
          shopping()
        else:
          shopping()
        if data == None:
            print('Customer name not found!')
 
def deletePro():
  choose = input('----- Type to add -----\n1.GRAPHIC CARD\n2.CPU\n3.MAINBOARD\n4.RAM\n5.POWER SUPPLY\nSelect: ')
  if choose == '1':
    type = 'GPU'
  elif choose == '2':
    type = 'CPU'
  elif choose == '3':
    type = 'MB'
  elif choose == '4':
    type = 'RAM'
  elif choose == '5':
    type = 'PSU'
  Product = input('Enter Product : ')
  ID = input('Enter ID : ')
  findData = dbs.child('Product').child(type).child(ID).get()
  a = findData.val()['Name']
  b = findData.val()['Price']
  print(ID,' : ',a,' : ',b)
  confirm = input('Are you sure ? [y/n] : ')
  if confirm == 'y':
    dbs.child('Storage').child(type).child(Product).remove()
    dbs.child('Product').child(type).child(ID).remove()
    print("Remove Complete")
  else:
    admin()
    
  ch = input('Do you want to delete another product?[y/n] : ')
  if ch == 'y':
    deletePro()
  else:
    admin()   

def admin():
  print('=============== Admin Mode ===============')
  ch = input('1. Add Product\n2. Delete Customer Product\n3. Delete Product\n4. Read Customer Data\n5. Exit\n Your Answer : ')
  if ch == '1':
    addProduct()
  elif ch == '2':
    deleteCus()
  elif ch == '3':
    deletePro()
  elif ch =='4':
    findProduct()
  elif ch == '5':
    main()

def mail():
  queryData = db.collection('customers').document(name).get()
  if queryData.exists:
    mail = []
    mail.append(queryData.to_dict())
    G13_email.updateMail(mail,email)

def list(tempCal):
  choose = input('=============== Computer List ===============\n1.GRAPHIC CARD\n2.CPU\n3.MAINBOARD\n4.RAM\n5.POWER SUPPLY\nSelect: ')
  if choose == '1':
    type = 'GPU'
  elif choose == '2':
    type = 'CPU'
  elif choose == '3':
    type = 'MB'
  elif choose == '4':
    type = 'RAM'
  elif choose == '5':
    type = 'PSU'
  #Create First time Firestore Database
  print('created product\n=============== ',type,' LIST ===============')
  # Realtime Database
  cal = 0
  while True:
    items = dbs.child('Storage').child(type).get()
    for item in items.each():
      n = item.key()
      d = item.val()['ID']
      p = item.val()['Price']
      print(d,' : ',n,' : ',p)

    id = input('ID : ')
    ch = dbs.child('Product').child(type).child(id).get()
    a = ch.val()['Name']
    b = ch.val()['Price']
    print(a,' : ',b)
    incal = int(input('Enter amount : '))
    bb = int(b)
    cal = bb*incal
    tempCal = tempCal+cal
    print("Total : ",cal)

    update = db.collection('customers').document(name).update({'Product': firestore.ArrayUnion([a])})
    updates = db.collection('customers').document(name).update({'Price': firestore.ArrayUnion([cal])})
    updatess = db.collection('customers').document(name).update({'Total': tempCal})
    chs = input('Do you want to continue buying?[y/n] : ')
    if chs == 'n':
      mail()
      shopping()
    elif chs == 'y':
      list(tempCal)

tempCal = 0
def shopping():
  print("=============== Select Yout Choice ===============\n 1.SHOPING LIST\n 2.CHECK YOUR ORDER\n 3.REMOVE YOUR ORDER")
  selectCh = input('Select : ')
  if selectCh == '1':
    list(tempCal)
  elif selectCh == '2':
    customerProduct()
  elif selectCh == '3':
    deleteFromCus()

def createTable():
  global name
  name = input('Name : ')
  customers = db.collection("customers")
  customers.document(name).set({
    'Name': name,
    'Total':'',
    'Product':'',
    'Price':''
      })

def signup():
    print("========================== Sign Up ==========================") 
    global email
    email = input("Enter Your Email : ")
    password = input('Enter Your Password : ')
    try:
        print()
        user = auth.create_user_with_email_and_password(email, password)
        print('User created successfully: ',email)
        createTable()
        main()   
    except:
        print('Email already exists!')
        main()

def login():
    global email
    email = input("=============== Login ===============\nEnter email : ")
    password = input('Enter password : ')
    try:
        logins = auth.sign_in_with_email_and_password(email, password)
        print('\nLogged in!')
        if email == 'admin@admin.com':
          admin()
        else:
          global name
          name = input('Name : ')
          shopping()
    except:
        print('Incorrect username or password !')
        login()

def main():
  print('==================== Welcome to computer shop ====================\n\t1.Register \n\t2.Login')
  ch = input('Select : ')
  if ch == '1':
    signup()
  elif ch == '2':
    login()

main()