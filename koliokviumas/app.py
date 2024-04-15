from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# In-memory storage for users and tasks
users = []
tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        user_name = request.form['name']
        users.append(user_name)
        return redirect(url_for('manage_users'))
    return render_template('users.html', users=users)

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        task_title = request.form['title']
        task_description = request.form['description']
        task_user = request.form['user']
        task_status = 'Neatlikta'  # Default status when task is created
        task_id = len(tasks) + 1
        tasks.append({
            'id': task_id,
            'title': task_title,
            'description': task_description,
            'status': task_status,
            'user': task_user
        })
        return redirect(url_for('manage_tasks'))
    return render_template('tasks.html', tasks=tasks, users=users)

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return 'Task not found', 404

    if request.method == 'POST':
        # Update task details
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['status'] = request.form['status']
        task['user'] = request.form['user']
        return redirect(url_for('manage_tasks'))

    return render_template('task_detail.html', task=task, users=users)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('manage_tasks'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
