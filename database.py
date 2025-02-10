import mysql.connector
from datetime import datetime,date
import random
from tabulate import tabulate
import os


def generateId():
    
    id = f"{datetime.now().strftime('%H%M%S')}"

    return int(id)


def getConnection():
    connection = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        database="ProjectQuiz"
    )
    cursor = connection.cursor()

    return [connection,cursor]

class category:

    
    def category_name(category_id):
        connection,cursor = getConnection() 
        query = f"select category_name from Categories where category_id = {category_id}" 
        cursor.execute(query)
        category = cursor.fetchall()

        return str(category[0][0])
    
    
    def add(category):
        connection,cursor = getConnection()

        id =  generateId()
        query = f"insert into Categories(category_id,category_name) values ({id},'{category}')"

        cursor.execute(query)
        connection.commit()
        
        print(f"Category : {category}, successfully created with {id}")  

    
    def showall():
        connection,cursor = getConnection() 
        query = "select * from Categories"   

        cursor.execute(query)
        headers = [columns[0] for columns in cursor.description]  
        records = cursor.fetchall()

        print(tabulate(records,headers,tablefmt="pretty")) 

    
    def showValidCategories():        
        connection,cursor = getConnection() 
        query = "SELECT c.category_id, c.category_name FROM categories c JOIN (SELECT category_id, COUNT(*) as cnt FROM questions GROUP BY category_id HAVING COUNT(*) > 15) q ON c.category_id = q.category_id;"   

        cursor.execute(query)
        headers = ["Category code","category"]  
        records = cursor.fetchall()

        print(tabulate(records,headers,tablefmt="pretty"))    

    
    def getById(category_id):
        connection,cursor = getConnection() 
        query = f"select category_name from Categories where category_id = {category_id}"
        cursor.execute(query)
        category = cursor.fetchall()

        return str(category[0][0])
    
    
    def validate(category_id):
        connection,cursor = getConnection() 
        query = f"SELECT EXISTS(SELECT 1 FROM Categories WHERE category_id = category_id)"
        cursor.execute(query)
        valid = cursor.fetchall()
        if int(valid[0][0]) == 0:
            print("Category does not exists! Retry.")
            return False
        else:
            return True


class questions:
    
    
    #### add questions
    def add(question):
        category_id,question_text,option01,option02,option03,option04,correct_option= question
        connection,cursor = getConnection()

        id = generateId()
        query = f"insert into Questions(question_id,category_id,question_text,option01,option02,option03,option04,correct_option)values({id},{category_id},'{question_text}','{option01}','{option02}','{option03}','{option04}',{correct_option})"
        
        cursor.execute(query)
        connection.commit()

        print(f"Question, successfully created with {id}")  

    
    #### update questions
    def update(question):
        question_id,category_id,question_text,option01,option02,option03,option04,correct_option= question 
        connection,cursor = getConnection()

        query = f"update Questions set question_text='{question_text}',option01='{option01}',option02='{option02}',option03='{option03}',option04='{option04}',correct_option={correct_option} where question_id = {question_id}"
        
        cursor.execute(query)
        connection.commit()

        print(f"Question updated successfully with id: {question_id}")

    
    #### delete a question
    def delete(question_id):
        connection,cursor = getConnection() 


        query = f"delete from questions where question_id = {question_id}" 

        cursor.execute(query)
        connection.commit()  

    
    #### show all questions
    def showall():
        connection,cursor = getConnection() 
        query = "select * from questions"   

        cursor.execute(query)
        headers = [columns[0] for columns in cursor.description]  
        records = cursor.fetchall()

        print(tabulate(records,headers,tablefmt="pretty"))
        print()       

    
    def getById(question_id):
        connection,cursor = getConnection() 
        query = f"select question_text,option01,option02,option03,option04,correct_option from questions where question_id = {question_id}"
        cursor.execute(query)
        records = cursor.fetchall()
        question = list()
        for data in records[0]:
            question.append(data)

        return question
    
    
    def getByCategory(category_id):
        connection,cursor = getConnection() 
        query = f"select question_id,question_text,option01,option02,option03,option04,correct_option from questions where category_id = {category_id}"   

        cursor.execute(query)
        headers = [columns[0] for columns in cursor.description]  
        records = cursor.fetchall()

        print(tabulate(records,headers,tablefmt="pretty"))
        print()         





class user:
    category = category()

    def getAdmin():
        connection,cursor = getConnection()
        query="Select password from Users where user_id='191431' and username='ADMIN'"
        cursor.execute(query)
        value=cursor.fetchall()
        password=str(value[0][0])
        
        return password


    def createUser(username,password,email):
        connection,cursor = getConnection()
        id = generateId()
        query =f"insert into users(user_id,username,email,password)values({id},'{username}','{email}','{password}')"
        cursor.execute(query)
        connection.commit()

        print(f"User successfully created with username: {username} and user Id: {id} ")
    
    def validate(username,password):
        connection,cursor = getConnection() 
        query = f"SELECT EXISTS(SELECT 1 FROM Users WHERE username ='{username}')"
        cursor.execute(query)
        valid = cursor.fetchall()
        if int(valid[0][0]) == 0:
            return None
        
        query = f"select user_id,password,email from Users where username= '{username}'"
        cursor.execute(query)
        
        userCreds =cursor.fetchall()

        if userCreds[0][1] == password:
            os.system('cls')
            print(f"Hello, {username}.")
            # print([int(userCreds[0][0]),username,password,str(userCreds[0][2])])
            return [int(userCreds[0][0]),username,password,str(userCreds[0][2])]
        else :
            return None
        

    def getQuestions(category_id):
        connection,cursor = getConnection() 
        query = f"select question_id,question_text,option01,option02,option03,option04,correct_option from questions where category_id = {category_id}"   

        cursor.execute(query)
        headers = [columns[0] for columns in cursor.description]  
        questions = cursor.fetchall()

        return questions  
    
    
    def setScore(testInfo):
        connection,cursor = getConnection()
        userid,category_id,score = testInfo
        id = generateId()
        # query = f"SELECT EXISTS(SELECT 1 FROM Results WHERE user_id ='{userid}' and category_id='{category_id}')"
        query = f"insert into Results(result_id,user_id,category_id,score,quiz_date)values ({id},{userid},{category_id},{score},'{date.today()}')"
        cursor.execute(query)
        connection.commit()
         
    
    def quizHistory(userid):     
        connection,cursor = getConnection() 
        # print(f"\n{category.category_name(category_id)} scores:\n")
        query = f"select categories.category_name,results.quiz_date,results.score from Categories join Results on categories.category_id = results.category_id where results.user_id ={userid}"
        cursor.execute(query)
        headers = ["Category","Date of Quiz","Score"]  
        results=cursor.fetchall()

        print(tabulate(results,headers,tablefmt='pretty'))

    
    def scoreCard(userid):
        connection,cursor = getConnection() 
        query = f"SELECT categories.category_name, Max(results.score) as max_score FROM categories JOIN results ON categories.category_id = results.category_id where results.user_id = {userid} GROUP BY categories.category_name;"
        cursor.execute(query)
        headers = ["Category","Maximum Score"]  
        results=cursor.fetchall()

        print(tabulate(results,headers,tablefmt='pretty'))


    def leaderBoard():
         connection,cursor = getConnection()    

         query = f"Select ROW_NUMBER() OVER (ORDER BY Avg(results.score) DESC) as ranks,users.username,ROUND(Avg(results.score), 2) as total_score FROM results JOIN users ON results.user_id = users.user_id GROUP BY users.username ORDER BY total_score DESC;"
         cursor.execute(query)
         headers = ["Rank","Username","Cummulative Score"]  
         results=cursor.fetchall()
         tblfmt = { 'tablefmt': 'plain', 'numalign': 'left', 'stralign': 'left',}

         print(tabulate(results,headers,**tblfmt))