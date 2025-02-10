import random
import sys
import database
import os
import time

class Admin:

 def createCategory(self):
    category = str(input("Enter a category name: "))
    database.category.add(category)


 def  addQuestions(self,category_id):
    while True:
        question_text = str(input("Enter a quiz question: "))
        option01 = str(input("Set option 1 as: "))
        option02 = str(input("Set option 2 as: "))
        option03 = str(input("Set option 3 as: "))
        option04 = str(input("Set option 4 as: "))
        while True: 
            correct_option = int(input("Enter serial number of correct option: "))
            if correct_option in [1,2,3,4]: break 
            else: print("Choose from (1,2,3,4).\n")

        print(f"\nReview the question:\nQuestion: {question_text}\n1> {option01}\n2> {option02}\n3> {option03}\n4> {option04}\ncorrect option: {correct_option}\n")    

        if str(input("Press 1 to rewrite the question.\nPress any key to continue.")) != str(1) : 
            database.questions.add([category_id,question_text,option01,option02,option03,option04,correct_option])
            break


 def updateQuestions(self,category_id):
    database.questions.getByCategory(category_id)
    question_id = int(input("Enter a question id: "))
    while True:
        question_text = str(input("Enter updated question: "))
        option01 = str(input("Set option 1 as: "))
        option02 = str(input("Set option 2 as: "))
        option03 = str(input("Set option 3 as: "))
        option04 = str(input("Set option 4 as: "))
        while True: 
            correct_option = int(input("Enter serial number of correct option: "))
            if correct_option in [1,2,3,4]: break 
            else: print("Choose from (1,2,3,4).\n")

        print(f"\nReview the question:\nQuestion: {question_text}\n1> {option01}\n2> {option02}\n3> {option03}\n4> {option04}\ncorrect option: {correct_option}\n")    

        if str(input("Press 1 to rewrite the question.\nPress any key to continue.")) != str(1) : 
            database.questions.update([question_id,category_id,question_text,option01,option02,option03,option04,correct_option])
            break


 def deleteQuestions(self,category_id):
    database.questions.getByCategory(category_id)
    question_id = int(input("Enter question id to delete the question: ")) 
    
    questionbody = database.questions.getById(question_id)  
    
    print(f":\nQuestion: {questionbody[0]}\n1> {questionbody[1]}\n2> {questionbody[2]}\n3> {questionbody[3]}\n4> {questionbody[4]}\ncorrect option: {questionbody[5]}\n")    
    
    if str(input("Press 1 to delete the question.\nPress any key to continue.")) == str(1) : 
            database.questions.delete(question_id)

 
 def editQuestions(self):
    # print categorys from sql  
    database.category.showall()
    category_id = int(input("\nChoose a category:"))
    
    while True:
        case = int(input(f"\nWhat would you like to do with category {database.category.getById(category_id)}?"
                        "\n1>>> Add a question."
                        "\n2>>> Update a question."
                        "\n3>>> Delete a question."
                        "\n4>>> Back.\n>"))
    
        match case :
            case 1 : self.addQuestions(category_id)
            case 2 : self.updateQuestions(category_id)
            case 3 : self.deleteQuestions(category_id)
            case 4 : break
            case _ : 
                     print("\nInvalid choice, please tell me...") 
                     self.editQuestions()



class User:
 
 
 def validate(self,username,password):
        return database.user.validate(username,password) 
 
 
 def takequiz(self,userid):
     database.category.showValidCategories()
     while True:
        category_id=int(input("Choose a category (enter category id):  "))
        if database.category.validate(category_id) : break

     questions = database.user.getQuestions(category_id)
     q_numbers =  random.sample(range(1, len(questions)+1),15)   
     question_set = [question for question in questions if questions.index(question)+1 in  q_numbers ]

     Sr=1
     score=0
     for question in question_set:
    #    while True:  
         print(f"\nQuestion{Sr}:\n\nQuestion: {question[1]}\n1> {question[2]}\n2> {question[3]}\n3> {question[4]}\n4> {question[5]}\n")
         
         Sr+=1   
         if int(input("Answer> "))==question[6]:            
            score+=1
              

     print(f"\nYou scored {score}/15")
     database.user.setScore([userid,category_id,score])
     input("Press any key to continue...")

 
 def scorecard(self,userid):
     
     print("\nOverall score card:\n")
     database.user.scoreCard(userid)   
     input("Press any key to continue...")
         
 
 def quizHistory(self,userid):
     print("\nYour history:\n")
     database.user.quizHistory(userid)
     input("Press any key to continue...")


 def leaderBoard(self):  
     print("\nLeaderboard-----------------------------------\n")
     database.user.leaderBoard()
     input("\nPress any key to continue...")
 
 def userpanel(self,userInfo):
    while True:    
        os.system('cls')
        userid,username,password,email = userInfo
        print(f"User       : {username}\nUser Id    : {userid}\nUser email : {email}\n") 

        case = int(input("1>>>Take a quiz.\n2>>>See score card.\n3>>>Leaderboard.\n4>>>Quizes history\n5>>>Log out.\n>"))   
        match case:
            case 1 : self.takequiz(userid)
            case 2 : self.scorecard(userid)
            case 3 : self.leaderBoard()
            case 4 : self.quizHistory(userid)
            case 5 : 
                     print("You are logged out.")
                     time.sleep(2)
                     return
            case _ : print("Choose a valid option.")
                     
def validAdmin():
    for tries in [1,2,3]:
                    if str(input("Enter your password: ")) == database.user.getAdmin() : return True 
                    else: print("Try again.")
    return False    

if __name__ == '__main__': 

    admin = Admin()
    user = User()

    while True:
        os.system('cls')
        case = int(input("\nWho are you?\n1>>> Admin."
                         "\n2>>> User."
                         "\n3>>> Exit system.\n>"))
        match case :
            case 1:
                if not validAdmin():
                    print("Exited admin due to multiple wrong attempts.")
                    continue
                
                os.system('cls')
                print("\nGreetings! Sir Admin.")
                while True:
                    case =  int(input("\nWhat would you like to do sir?"
                                 "\n1>>> Add a category."
                                 "\n2>>> Edit questions."
                                 "\n3>>> Back.\n>")) 
                    
                    match case:
                        case 1 :  admin.createCategory()
                        case 2 :  admin.editQuestions()
                        case 3 :  break
                        case _ :
                            print("\nChoose a valid option, sir.")
            
            case 2:
                if input("Already a user? y/n") in ["Y","y"]:
                 while True:
                    userCreds =[str(input("Enter your username: ")),str(input("\nEnter password: "))]
                    userInfo = user.validate(userCreds[0],userCreds[1])
                    if userInfo is not None: break

                 time.sleep(1) 
                 os.system('cls')
                 user.userpanel(userInfo)   
                else:
                    print("Create a user:")
                    while True:
                        username = str(input("\nEnter a username: "))
                        password = str(input("\nEnter a password: "))
                        email = str(input("\nEnter an email: "))
                        if str(input("Press 1 to edit the user profile.\nPress any key to continue.")) != str(1) : break

                    database.user.createUser(username,password,email)    

                                
            case 3:
                print("\nSystem exited succefully!")
                sys.exit()
            
            case _ :   
                print("\nChoose a valid option, sir.")     
                                