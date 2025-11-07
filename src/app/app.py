from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import os

from validation.natural_val import MathExpressionParser
from my_math.natural_module import NaturalModule

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return redirect(url_for('natural'))

@app.route('/natural', methods=['GET', 'POST'])
def natural():
    if 'natural_history' not in session:
        session['natural_history'] = []
    
    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = MathExpressionParser()
            result = parser.evaluate(expression, NaturalModule)
            session['natural_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True
            flash('Вычисление выполнено успешно!', 'success')
            
        except Exception as e:
            # print(f"Ошибка: {str(e)}', 'danger")
            flash(f'Ошибка: {str(e)}', 'danger')
        
        return redirect(url_for('natural'))
    
    return render_template('natural.html', history=session.get('natural_history', []))


@app.route('/natural/clear', methods=['POST'])
def clear_natural_history():
    session['natural_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('natural'))


@app.route('/integer', methods=['GET', 'POST'])
def integer():
    if request.method == "POST":
        math_exp = request.form['math_exp']
    return render_template("natural.html")


@app.route('/rational', methods=['GET', 'POST'])
def rational():
    if request.method == "POST":
        math_exp = request.form['math_exp']
    return render_template("natural.html")


@app.route('/polynomial', methods=['GET', 'POST'])
def polynomial():
    if request.method == "POST":
        math_exp = request.form['math_exp']
    return render_template("natural.html")


if __name__ == '__main__':
    app.run(debug=True)