from flask import Flask, render_template, request
import datetime


app = Flask(__name__)


# routing homepage
@app.route('/')
def login():
    return render_template('login.html')


# routing survey html
@app.route('/survey')
def survey():
    return render_template('survey.html')


# Route to handle form submission from survey.html
@app.route('/surveyAnswers', methods=['POST'])
def surveyAnswers():
    Main.questionOne.userAnswer = int(request.form['showerTime'])
    calculate_survey_answers(Main.questionOne)
    Main.questionTwo.userAnswer = int(request.form['driveTime'])
    calculate_survey_answers(Main.questionTwo)
    Main.questionThree.userAnswer = int(request.form['temp'])
    calculate_survey_answers(Main.questionThree)
    Main.questionFour.userAnswer = int(request.form['recycle'])
    calculate_survey_answers(Main.questionFour)

    Main.examplePerson.ecoScore= Main.questionOne.points + Main.questionTwo.points+Main.questionThree.points+Main.questionFour.points
    
    return render_template('home.html', msg = Main.examplePerson.ecoScore)
    
@app.route('/taskList', methods=['POST'])
def taskList():
    Main.taskOne.completed = request.form['task1']
    Main.taskTwo.completed = request.form['task2']
    Main.taskThree.completed = request.form['task3']
    Main.taskFour.completed = request.form['task4']
    Main.taskFive.completed = request.form['task5']
    
    numTaskComplete = 0
    for task in Main.tasksGenerated:
        if task.completed:
            numTaskComplete = numTaskComplete + 1
            Main.examplePerson.ecoScore = Main.examplePerson.ecoScore + 2
            if Main.examplePerson.ecoScore > 100:
                Main.examplePerson.ecoScore = 100 
    if numTaskComplete >= 3:
        Main.examplePerson.ecoScore = Main.examplePerson.ecoScore + numTaskComplete*2
        if Main.examplePerson.ecoScore > 100:
                Main.examplePerson.ecoScore = 100 
    else:
        Main.examplePerson.ecoScore = Main.examplePerson.ecoScore - 10
        if Main.examplePerson.ecoScore < 0:
                Main.examplePerson.ecoScore = 0 

    return render_template('home.html', msg = Main.examplePerson.ecoScore)


"""
#How we are storing our data for a single user for demo convenience
USER_DATA = {
    "tasks": [], 
    # "weeklyScore": 0, <--- REMOVED
    "ecoScore": 100, 
    "lastResetDate": None 
}
"""

#Person Class: User Info


class Person:
    def __init__(self, name, age, username, password, email, phone):
        self.name = name
        self.age = age
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.ecoScore = 0
        self.numEvents = 0
       
# Survey Class:
class Survey:
    def __init__(self, sentence, category):
        self.sentence = sentence
        self.points = 0
        self.userAnswer = 0
        #100 for water / 200 carbon emissons / 300 energy consumption / 400 waste reduction
        self.category = category


#Task Class
class Task:
    def __init__(self, description):
        #gets and stores specific task ID
        #Jess note jess needs to CHANGE this below
        self.id = Task.next_id
        Task.next_id += 1
        self.description = description
        #self.dueDate = dueDate
        self.completed = False
    def to_dict(self):
        #Helper for jsonify: converts Task object to a JSON-friendly dict.
        return {
            'id': str(self.id),
            'description': self.description,
            'completed': self.completed
        }

   
class Main:
    # list of questions
    #water source category
    questionOne = Survey("How many minutes is your shower?", 100)
    #carbon emissons
    questionTwo = Survey("How many days a week do you drive your car?", 200)
    #energy consumption
    questionThree = Survey("What do you keep your thermostat at during the summer?", 300)
    #waste reduction
    questionFour = Survey("How frequently do you recycle, enter 1 through 5: (1 being never, 5 being everyday):", 400)
    #questionFive = Survey("Do you have a car? 1 for yes 2 for no", 0, False)  
    
    #Person example being made to add login info to and ecoScore
    examplePerson = Person("",0,"","","","")
    #would be a database of other Person objects to represent the other website's users

    #Tasks Initialization
    taskOne = Task("Reduce your daily shower time")
    taskTwo = Task("Use public transportation at least once this week")
    taskThree = Task("Use a reusable water bottle")
    taskFour = Task("Unplug unused electronics to save energy")
    taskFive = Task("Recycle or compost your waste properly")
    tasksGenerated = [taskOne,taskTwo,taskThree,taskFour,taskFive]

# assigns the points a user recieves for each question based on its respective category
def calculate_survey_answers(question):
    # shower time
   # totalScore = 0
    #tasksGenerated = []
    if question.category == 100:
        #less than or equal 10 mins of shower time = really good
        if question.userAnswer <= 10:
            question.points = 25
        #11-25 mins of shower time = you can do better
        elif question.userAnswer <= 25:
            question.points = 15
        #more than 25 mins of shower time = really bad
        else:
            question.points = 5
        
    #if question.category == 200:
    if(question.category == 200):
        #less than or equal to 2 days of car driving = really good
        if question.userAnswer <= 2:
            question.points = 25
        #4 days of car driving = you can do better
        elif question.userAnswer <= 4:
            question.points = 15
        #more than 5 days = really bad
        else:
            question.points = 5
    #if question.category == 300:
    if(question.category == 300):
        #more than or equal to 78 degrees fahrenheit = really good
        if question.userAnswer >= 78 and question.userAnswer < 82:
            question.points = 25
        #more than or at 75 = you can do better
        elif question.userAnswer >= 75:
            question.points = 15
        #less than or at 74 days = really bad
        else:
            question.points = 5
    #if question.category == 400:
    if(question.category == 400):
        #4 or 5 for how frequent they recycle = really good
        if question.userAnswer == 5 or question.userAnswer == 5:
            question.points = 25
        #3 = you can do better
        elif question.userAnswer >= 75:
            question.points = 15
        #2 or less = really bad
        else:
            question.points = 5

"""
def add_task(description, dueDate):
    newTask = Task(description, dueDate)
    USER_DATA["tasks"].append(newTask) 
    print(f"Task '{description}' added.")

# Simplified complete_task (removed weeklyScore update)
def complete_task(task_id):
    for task in USER_DATA["tasks"]:
        if str(task.id) == str(task_id) and not task.completed: 
            task.completed = True
            return f"Task completed: {task.description}"
            
    return f"Task ID {task_id} not found or already completed."

#runs manually at the end of each week to transfer task scores to the overall ecoScore
def week_reset():
    # 1. Count how many tasks were completed
    completed_tasks_count = 0
    for task in USER_DATA["tasks"]:
        if task.completed:
            completed_tasks_count += 1
            
    # 2. Apply the scoring rule (50 points bonus)
    score_change = 0
    if completed_tasks_count >= 3:
        score_change = 50
        
    # 3. Apply optional Decay/Penalty (e.g., -10 for every task missed)
    missed_tasks_count = len(USER_DATA["tasks"]) - completed_tasks_count
    decay_penalty = missed_tasks_count * 10
    
    # 4. Final Score Update
    final_score_adjustment = score_change - decay_penalty
    USER_DATA["ecoScore"] += final_score_adjustment

    # 5. Reset for the next week
    USER_DATA["tasks"] = [] 
    
    return {
        'bonus_earned': score_change,
        'penalty_applied': decay_penalty,
        'new_eco_score': USER_DATA["ecoScore"]
    }"""

if __name__ == '__main__':
    app.run(debug=True)