from flask import Flask, render_template, redirect, request, session
import csv


app = Flask(__name__)

def storireader():
    lst = []
    with open("stories.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            lst.append(row)
    return lst


def max_id():
    stories = storireader()
    max_id = 0
    for i in stories:
        if int(i[0]) > int(max_id):
            max_id = int(i[0])
    max_id += 1
    return max_id

def write_rows(filename):
    with open('stories.csv', 'w') as file:
        datawriter = csv.writer(file)
        datawriter.writerows(filename)




def get_data():
    story_title = request.form['story_title']
    user_story = request.form['user_story']
    acc_criteria = request.form['acceptcrit']
    business_value = request.form['bussines_value']
    estimation = request.form['estimation']
    status = request.form['status']
    actual_list = [story_title, user_story, acc_criteria, business_value, estimation, status]
    return actual_list


@app.route('/')
def list():
    stories_list = storireader()
    length_of_csv = len(stories_list)
    return render_template('list.html', stories_list=stories_list, long=length_of_csv)


@app.route('/story')
def new_story():
    return render_template('form.html')



@app.route('/story', methods=['POST'])
def story_receive():
    temp_data = get_data()
    id = []
    id.append(max_id())
    new_data = id + temp_data
    with open('stories.csv', 'a', newline='') as file:
        datawriter = csv.writer(file)
        datawriter.writerow(new_data)
    return redirect('/')


@app.route('/story/<int:id>')
def storybyid(id):
    stories_list = storireader()
    return render_template('form.html', id=id, stories_list=stories_list)


@app.route('/story/<int:id>', methods = ['POST'])
def update_story(id):
    temp_data = get_data()
    new_data =[]
    new_data.append(str(id))
    new_data = new_data + temp_data
    db = storireader()
    count = 0
    for i in db:
        if i[0] == new_data[0]:
            break
        else:
            count += 1
    print(db[count])
    print(new_data)
    db[count] = new_data
    with open('stories.csv', 'w', newline='') as file:
        datawriter = csv.writer(file)
        datawriter.writerows(db)
    return redirect('/')


app.secret_key = 'sadfdfgdsfg1234234234'
app.run(
    debug=True,  # Allow verbose error reports
    port=5000  # Set custom port
)
