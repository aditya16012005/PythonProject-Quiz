import sys
import database
import os
import time
import random
from CustomExceptions import (
    DatabaseConnectionError,
    InvalidInputError,
    AuthenticationError,
    CategoryNotFoundError,
    QuestionNotFoundError,
    UserNotFoundError,
    InvalidIntegerError,
    InvalidChoiceError
)

class Admin:
    def createCategory(self):
        try:
            category = str(input("Enter a category name: "))
            if not category.strip():
                raise InvalidInputError("Category name cannot be empty.")
            database.category.add(category)
        except DatabaseConnectionError as e:
            print(e)

    def addQuestions(self, category_id):
        try:
            if not database.category.validate(category_id):
                raise CategoryNotFoundError()
            while True:
                question_text = str(input("Enter a quiz question: "))
                option01 = str(input("Set option 1 as: "))
                option02 = str(input("Set option 2 as: "))
                option03 = str(input("Set option 3 as: "))
                option04 = str(input("Set option 4 as: "))
                while True:
                    try:
                        correct_option = int(input("Enter serial number of correct option: "))
                        if correct_option not in [1, 2, 3, 4]:
                            raise InvalidIntegerError("Correct option must be between 1 and 4.")
                        break
                    except ValueError:
                        raise InvalidIntegerError()
                print(f"\nReview the question:\nQuestion: {question_text}\n1> {option01}\n2> {option02}\n3> {option03}\n4> {option04}\ncorrect option: {correct_option}\n")
                if str(input("Press 1 to rewrite the question.\nPress any key to continue.")) != str(1):
                    database.questions.add([category_id, question_text, option01, option02, option03, option04, correct_option])
                    break
        except (DatabaseConnectionError, CategoryNotFoundError) as e:
            print(e)

    def updateQuestions(self, category_id):
        try:
            if not database.category.validate(category_id):
                raise CategoryNotFoundError()
            database.questions.getByCategory(category_id)
            question_id = int(input("Enter a question id: "))
            if not database.questions.getById(question_id):
                raise QuestionNotFoundError()
            while True:
                question_text = str(input("Enter updated question: "))
                option01 = str(input("Set option 1 as: "))
                option02 = str(input("Set option 2 as: "))
                option03 = str(input("Set option 3 as: "))
                option04 = str(input("Set option 4 as: "))
                while True:
                    try:
                        correct_option = int(input("Enter serial number of correct option: "))
                        if correct_option not in [1, 2, 3, 4]:
                            raise InvalidIntegerError("Correct option must be between 1 and 4.")
                        break
                    except ValueError:
                        raise InvalidIntegerError()
                print(f"\nReview the question:\nQuestion: {question_text}\n1> {option01}\n2> {option02}\n3> {option03}\n4> {option04}\ncorrect option: {correct_option}\n")
                if str(input("Press 1 to rewrite the question.\nPress any key to continue.")) != str(1):
                    database.questions.update([question_id, category_id, question_text, option01, option02, option03, option04, correct_option])
                    break
        except (DatabaseConnectionError, CategoryNotFoundError, QuestionNotFoundError) as e:
            print(e)

    def deleteQuestions(self, category_id):
        try:
            if not database.category.validate(category_id):
                raise CategoryNotFoundError()
            database.questions.getByCategory(category_id)
            question_id = int(input("Enter question id to delete the question: "))
            questionbody = database.questions.getById(question_id)
            if not questionbody:
                raise QuestionNotFoundError()
            print(f":\nQuestion: {questionbody[0]}\n1> {questionbody[1]}\n2> {questionbody[2]}\n3> {questionbody[3]}\n4> {questionbody[4]}\ncorrect option: {questionbody[5]}\n")
            if str(input("Press 1 to delete the question.\nPress any key to continue.")) == str(1):
                database.questions.delete(question_id)
        except (DatabaseConnectionError, CategoryNotFoundError, QuestionNotFoundError) as e:
            print(e)

    def editQuestions(self):
        try:
            database.category.showall()
            category_id = int(input("\nChoose a category:"))
            if not database.category.validate(category_id):
                raise CategoryNotFoundError()
            while True:
                case = int(input(f"\nWhat would you like to do with category {database.category.getById(category_id)}?"
                                "\n1>>> Add a question."
                                "\n2>>> Update a question."
                                "\n3>>> Delete a question."
                                "\n4>>> Back.\n>"))
                match case:
                    case 1:
                        self.addQuestions(category_id)
                    case 2:
                        self.updateQuestions(category_id)
                    case 3:
                        self.deleteQuestions(category_id)
                    case 4:
                        break
                    case _:
                        raise InvalidChoiceError()
        except (DatabaseConnectionError, CategoryNotFoundError, InvalidChoiceError) as e:
            print(e)


class User:
    def validate(self, username, password):
        try:
            userInfo = database.user.validate(username, password)
            if userInfo is None:
                raise AuthenticationError()
            return userInfo
        except (DatabaseConnectionError, AuthenticationError) as e:
            print(f"{e},incorrect username or password.")

    def takequiz(self, userid):
        try:
            database.category.showValidCategories()
            while True:
                try:
                    category_id = int(input("Choose a category (enter category id): "))
                except ValueError:
                    raise InvalidIntegerError("Please enter a valid integer for the category ID.")
                if database.category.validate(category_id):
                    break
                else:
                    print("Invalid category ID. Please choose a valid category.")
            questions = database.user.getQuestions(category_id)
            q_numbers = random.sample(range(1, len(questions) + 1), 15)
            question_set = [question for question in questions if questions.index(question) + 1 in q_numbers]
            Sr = 1
            score = 0
            for question in question_set:
                print(f"\nQuestion{Sr}:\n\nQuestion: {question[1]}\n1> {question[2]}\n2> {question[3]}\n3> {question[4]}\n4> {question[5]}\n")
                Sr += 1
                try:
                    user_answer = int(input("Answer> "))
                    if user_answer == question[6]:
                        score += 1
                except ValueError:
                    raise InvalidIntegerError("Please enter a valid integer for your answer.")
            print(f"\nYou scored {score}/15")
            database.user.setScore([userid, category_id, score])
            input("Press any key to continue...")
        except (InvalidIntegerError, CategoryNotFoundError) as e:
            print(e)

    def scorecard(self, userid):
        try:
            print("\nOverall score card:\n")
            database.user.scoreCard(userid)
            input("Press any key to continue...")
        except DatabaseConnectionError as e:
            print(e)

    def quizHistory(self, userid):
        try:
            print("\nYour history:\n")
            database.user.quizHistory(userid)
            input("Press any key to continue...")
        except DatabaseConnectionError as e:
            print(e)

    def leaderBoard(self):
        try:
            print("\nLeaderboard-----------------------------------\n")
            database.user.leaderBoard()
            input("\nPress any key to continue...")
        except DatabaseConnectionError as e:
            print(e)

    def userpanel(self, userInfo):
        while True:
            try:
                os.system('cls')
                userid, username, password, email = userInfo
                print(f"User       : {username}\nUser Id    : {userid}\nUser email : {email}\n")
                try:
                    case = int(input("1>>>Take a quiz.\n2>>>See score card.\n3>>>Leaderboard.\n4>>>Quizes history\n5>>>Log out.\n>"))
                except ValueError:
                    raise InvalidIntegerError("Please enter a valid integer choice.")
                match case:
                    case 1:
                        self.takequiz(userid)
                    case 2:
                        self.scorecard(userid)
                    case 3:
                        self.leaderBoard()
                    case 4:
                        self.quizHistory(userid)
                    case 5:
                        print("You are logged out.")
                        time.sleep(2)
                        return
                    case _:
                        raise InvalidChoiceError()
            except (InvalidIntegerError, InvalidChoiceError) as e:
                print(e)


def validAdmin():
    try:
        for tries in [1, 2, 3]:
            admin_password = str(input("Enter your password: "))
            if admin_password == database.user.getAdmin():
                return True
            else:
                print("Try again.")
        raise AuthenticationError("Exited admin due to multiple wrong attempts.")
    except (DatabaseConnectionError, AuthenticationError) as e:
        print(e)
        return False

if __name__ == '__main__':
    admin = Admin()
    user = User()
    while True:
        try:
            os.system('cls')
            try:
                case = int(input("\nWho are you?\n1>>> Admin."
                                 "\n2>>> User."
                                 "\n3>>> Exit system.\n>"))
            except ValueError:
                raise InvalidIntegerError("Please enter a valid integer choice.")
            match case:
                case 1:
                    if not validAdmin():
                        continue
                    os.system('cls')
                    print("\nGreetings! Sir Admin.")
                    while True:
                        try:
                            case = int(input("\nWhat would you like to do sir?"
                                             "\n1>>> Add a category."
                                             "\n2>>> Edit questions."
                                             "\n3>>> Back.\n>"))
                        except ValueError:
                            raise InvalidIntegerError("Please enter a valid integer choice.")
                        match case:
                            case 1:
                                admin.createCategory()
                            case 2:
                                admin.editQuestions()
                            case 3:
                                break
                            case _:
                                raise InvalidChoiceError()
                case 2:
                    if input("Already a user? y/n") in ["Y", "y"]:
                        while True:
                            userCreds = [str(input("Enter your username: ")), str(input("\nEnter password: "))]
                            userInfo = user.validate(userCreds[0], userCreds[1])
                            if userInfo is not None:
                                break
                        time.sleep(1)
                        os.system('cls')
                        user.userpanel(userInfo)
                    else:
                        print("Create a user:")
                        while True:
                            username = str(input("\nEnter a username: "))
                            password = str(input("\nEnter a password: "))
                            email = str(input("\nEnter an email: "))
                            if str(input("Press 1 to edit the user profile.\nPress any key to continue.")) != str(1):
                                break
                        database.user.createUser(username, password, email)
                case 3:
                    print("\nSystem exited successfully!")
                    sys.exit()
                case _:
                    raise InvalidChoiceError()
        except (InvalidIntegerError, InvalidChoiceError) as e:
            print(e)