import yagmail
import pyautogui

def runMail(name, address, mail):
    yag = yagmail.SMTP(user='computershopFirst@gmail.com', password=pyautogui.password()) #เมลผู้ส่งและสร้าง popup ปิดรหัส
    recipients =  {mail:'Computer Shop'} #ผู้รับ #aline add 
    subject = 'สินค้าที่ท่านทำการสั่งซื้อ' 
   
    body = f"เรียน {name} สินค้าของท่านมีดังนี้ {address} คำเตือน!!: ห้ามตอบกลับ Email นี้ เพราะเป็นการส่งข้อความอัตโนมัติ"
    
    yag.useralias = 'Orders List'  #ชื่อผู้ส่ง

    yag.send(to=recipients, subject=subject,contents=[body])  

def updateMail(mail,mails):
    yag = yagmail.SMTP(user='computershopFirst@gmail.com', password=pyautogui.password()) #เมลผู้ส่งและสร้าง popup ปิดรหัส
    recipients =  {mails:'Computer Shop'} #ผู้รับ #aline add 
    subject = 'สินค้าที่ท่านทำการสั่งซื้อ' 
   
    strMail = ' '.join([str(elem) for elem in mail])
    contents = f"สินค้าของท่านมีดังนี้ {strMail} \nคำเตือน!!: ห้ามตอบกลับ Email นี้ เพราะเป็นการส่งข้อความอัตโนมัติ"
  
    yag.useralias = 'Orders List'  #ชื่อผู้ส่ง

    yag.send(to=recipients, subject=subject,contents=contents) 
