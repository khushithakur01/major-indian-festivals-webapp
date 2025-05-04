from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'indian_festivals_app_key'

# Load festival data from JSON
def load_festival_data():
    with open('festivals.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    """Landing page with Start button"""
    return render_template('index.html')

@app.route('/home')
def home():
    """Home page with festival cards"""
    festivals = load_festival_data()
    return render_template('home.html', festivals=festivals)

@app.route('/learn/<festival_id>')
def learn(festival_id):
    """Learning page for specific festival"""
    festivals = load_festival_data()
    if festival_id in festivals:
        return render_template('learn.html', festival=festivals[festival_id], festival_id=festival_id)
    return redirect(url_for('home'))

@app.route('/quiz/<festival_id>')
def quiz(festival_id):
    """Quiz page for specific festival"""
    festivals = load_festival_data()
    if festival_id == 'all':
        # All festivals quiz
        quiz_data = []
        for fest_id, fest_data in festivals.items():
            if 'quiz' in fest_data:
                # Take some questions from each festival
                quiz_data.extend(fest_data['quiz'][:2])  # Take first 2 questions from each
        return render_template('quiz.html', quiz_data=quiz_data, festival_id=festival_id, title="All Festivals Quiz")
    
    elif festival_id in festivals and 'quiz' in festivals[festival_id]:
        return render_template('quiz.html', 
                              quiz_data=festivals[festival_id]['quiz'], 
                              festival_id=festival_id,
                              title=f"{festivals[festival_id]['name']} Quiz")
    return redirect(url_for('home'))

@app.route('/submit_quiz/<festival_id>', methods=['POST'])
def submit_quiz(festival_id):
    """Process quiz submission"""
    user_answers = {}
    for key, value in request.form.items():
        if key.startswith('q'):
            user_answers[key] = value
    
    # Store answers in session
    session['user_answers'] = user_answers
    return redirect(url_for('result', festival_id=festival_id))

@app.route('/result/<festival_id>')
def result(festival_id):
    """Results page showing score and feedback"""
    if 'user_answers' not in session:
        return redirect(url_for('quiz', festival_id=festival_id))
    
    user_answers = session['user_answers']
    festivals = load_festival_data()
    
    if festival_id == 'all':
        # All festivals quiz
        quiz_data = []
        for fest_id, fest_data in festivals.items():
            if 'quiz' in fest_data:
                quiz_data.extend(fest_data['quiz'][:2])  # Take first 2 questions from each
    elif festival_id in festivals and 'quiz' in festivals[festival_id]:
        quiz_data = festivals[festival_id]['quiz']
    else:
        return redirect(url_for('home'))
    
    # Calculate score
    score = 0
    feedback = []
    for i, question in enumerate(quiz_data):
        question_id = f'q{i}'
        if question_id in user_answers:
            user_answer = user_answers[question_id]
            correct_answer = question['answer']
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            feedback.append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })
    
    # Clear session after calculating results
    session.pop('user_answers', None)
    
    title = "All Festivals Quiz Results" if festival_id == 'all' else f"{festivals[festival_id]['name']} Quiz Results"
    
    return render_template('result.html', 
                          score=score, 
                          total=len(quiz_data),
                          feedback=feedback,
                          title=title)

if __name__ == '__main__':
    app.run(debug=True)