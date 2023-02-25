import mysql.connector as sql
from mysql.connector.errors import ProgrammingError
import os
import platform
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def clearscreen():
    if(platform.system()=="Windows"):
        os.system("CLS")
    else:
        os.system("clear")
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-WELCOME TO -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-CHILL_OUT-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-")
    print("-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-RESTAURANT-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

def getProdList(qry):
    try:
        engine=create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?use_unicode=1&charset=utf8'.format('root', '1234', 'localhost', 'chill_out'))
        df=pd.read_sql(qry,engine,index_col="Product ID")
    except ProgrammingError as ex:
        print("MySQL Error",ex)
    finally:
        engine.dispose()
    return df

def listprod(qry):
    df=getProdList(qry)
    print(df)

def addprod():
    op='Y'
    try:
        engine=create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?use_unicode=1&charset=utf8'.format('root', '1234', 'localhost', 'chill_out'))
        while(op=='Y'):
            pro_id=input("Enter Product ID:- ")
            pro_name=input("Enter Product Name:- ")
            pro_rate=float(input("Enter Product Rate:- "))
            d={'pro_id':pro_id,'pro_name':pro_name,'pro_rate':pro_rate}
            df=pd.DataFrame(d,index=[0])
            df.to_sql(con=engine,if_exists='append',name='product',index=False)
            print("Product Added Successfully")
            op=input("Do You Want To Add More(Y/N)").upper()
    except ProgrammingError as ex:
        print("MySQL Error",ex)
    finally:
        engine.dispose()

def editprod():
    df=getProdList("SELECT pro_id as 'Product ID',pro_name as 'Product Name', pro_rate as 'Rate' FROM PRODUCT")
    print(df)
    prod_id=input("Enter Product ID:- ")
    pro_name=input("Enter Product Name:- ")
    pro_rate=float(input("Enter Product Rate:- "))
    try:
        engine=create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?use_unicode=1&charset=utf8'.format('root', '1234', 'localhost', 'chill_out'))
        engine.connect()
        qry="UPDATE product SET pro_name='{0}',pro_rate={1} WHERE pro_id='{2}'".format(pro_name,pro_rate,prod_id)
        engine.execute(qry)
    except ProgrammingError as ex:
        print("MySQL Error",ex)
    finally:
        engine.dispose() 

def delprod():
    df=getProdList("SELECT pro_id as 'Product ID',pro_name as 'Product Name', pro_rate as 'Rate' FROM PRODUCT")
    print(df)
    prod_id=input("Enter Product ID:- ")
    try:
        engine=create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?use_unicode=1&charset=utf8'.format('root', '1234', 'localhost', 'chill_out'))
        engine.connect()
        qry="DELETE FROM product WHERE pro_id='{0}'".format(prod_id)
        engine.execute(qry)
    except ProgrammingError as ex:
        print("MySQL Error",ex)
    finally:
        engine.dispose()

def prodmenu():
    while(True):
        clearscreen()
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. List Product")
        print("5. Back to Main menu")
        ch=int(input("Enter your option:"))
        if(ch==1):
            addprod()
        elif(ch==2):
            editprod()
            input("Press Any Key To Continue...")
        elif(ch==3):
            delprod()
        elif(ch==4):
            listprod("SELECT pro_id as 'Product ID',pro_name as 'Product Name', pro_rate as 'Rate' FROM PRODUCT")
            input("Press Any Key To Continue...")
        elif(ch==5):
            return
        else:
            print("You Have Choosen an Invalid Option!!!")

def billmenu():
    op="Y"
    items=[]
    tb = input("Enter the Table Number:")
    while(op=="Y"):
        df=getProdList("SELECT pro_id as 'Product ID',pro_name as 'Product Name', pro_rate as 'Rate' FROM PRODUCT")
        print(df)
        p_id = input("Enter Product ID:")
        qty = float(input("Enter Quantity:"))
        l=list([p_id,df["Product Name"][p_id],df["Rate"][p_id],qty])
        items.append(l)
        op=input("Do You Want To Add More(Y/N)").upper()
    print("Bill".center(54," "))
    print("Table No.: ",tb)
    print("-"*54)
    print("{0:6s}{1:20s}{2:8s}{3:10s}{4:15s}".format("SN.","Item","Rate","Qty","Amount"))
    sn=1
    total_amount=0
    for item in items:
        amount=item[2]*item[3]
        print("{0:<6s}{1:20s}{2:<7.2f}{3:>5.2f}{4:>12.2f}".format(str(sn),item[1][:20],item[2],item[3],amount))
        sn+=1
        total_amount+=amount
    print("-"*54)
    print("Total Amount Payable=",total_amount)
    print("\nThanks for choosing us. Do visit us again...")
    input("Press any key to continue...")
    

def mainmenu():
    while(True):
        clearscreen()
        print("1. Calculate Bill")
        print("2. Product Menu")
        print("3. Exit")
        ch=int(input("Enter your option:"))
        if(ch==1):
            billmenu()
            pass
        elif(ch==2):
            prodmenu()
        elif(ch==3):
            print("Good Bye....")
            break
        else:
            print("You Have Choosen an Invalid Option!!!")
            
mainmenu()
