from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import os

from validation.natural_expression_parser import NatExpressionParser
from validation.integer_expression_parser import IntExpressionParser
from validation.rational_expression_parser import RatExpressionParser
from my_math.natural_module import NaturalModule
from my_math.integer_module import IntegerModule
from my_math.rational_module import RationalModule


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = "a-fixed-secret-key-for-development"


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
            parser = NatExpressionParser()
            result = parser.evaluate(expression, NaturalModule)
            session['natural_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True
            flash('Вычисление выполнено успешно!', 'success')

        except Exception as e:
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
    if 'integer_history' not in session:
        session['integer_history'] = []

    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = IntExpressionParser()
            result = parser.evaluate(expression, IntegerModule)
            session['integer_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True
            flash('Вычисление выполнено успешно!', 'success')

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'danger')

        return redirect(url_for('integer'))

    return render_template('integer.html', history=session.get('integer_history', []))


@app.route('/integer/clear', methods=['POST'])
def clear_integer_history():
    session['integer_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('integer'))


@app.route('/rational', methods=['GET', 'POST'])
def rational():
    if 'rational_history' not in session:
        session['rational_history'] = []

    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = RatExpressionParser()
            result = parser.evaluate(expression)
            session['rational_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True
            flash('Вычисление выполнено успешно!', 'success')

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'danger')

        return redirect(url_for('rational'))

    return render_template('rational.html', history=session.get('rational_history', []))

@app.route('/rational/clear', methods=['POST'])
def clear_rational_history():
    session['rational_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('rational'))


@app.route('/polynomial', methods=['GET', 'POST'])
def polynomial():
    if request.method == "POST":
        math_exp = request.form['math_exp']
    return render_template("natural.html")


if __name__ == '__main__':
    app.run(debug=True)
