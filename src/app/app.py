import traceback
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_bootstrap import Bootstrap


from validation.natural_expression_parser import NatExpressionParser
from validation.integer_expression_parser import IntExpressionParser
from validation.rational_expression_parser import RatExpressionParser
from validation.polynomial_expression_parser import PolExpressionParser
from my_math.natural_module import NaturalModule
from my_math.integer_module import IntegerModule



app = Flask(__name__)  # создаём экземпляр Flask-приложения
Bootstrap(app)         # подключаем Bootstrap-расширение для шаблонов



app.config['SECRET_KEY'] = "secret_key_XD"  # секретный ключ для подписи cookies и работы с session



@app.route('/')
def index():
    # корневой маршрут: сразу перенаправляем на страницу с натуральными числами
    return redirect(url_for('natural'))



@app.route('/natural', methods=['GET', 'POST'])
def natural():
    # инициализация истории для натуральных чисел в сессии, если её ещё нет
    if 'natural_history' not in session:
        session['natural_history'] = []

    # обработка отправки формы
    if request.method == 'POST':
        expression = request.form.get('math_exp')  # читаем введённое выражение из формы
        try:
            parser = NatExpressionParser()         # создаём парсер для натуральных
            # вычисляем выражение; вторым аргументом передаётся класс модуля
            result = parser.evaluate(expression, NaturalModule)
            # добавляем в историю текущей сессии запись: что ввели и какой результат
            session['natural_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True               # помечаем, что session изменён
            flash('Вычисление выполнено успешно!', 'success')  # всплывающее сообщение об успехе

        except Exception as e:
            # при любой ошибке показываем флеш-сообщение пользователю
            flash(f'Ошибка: {str(e)}', 'danger')

        # после POST всегда делаем redirect по PRG-паттерну
        return redirect(url_for('natural'))

    # при GET просто рендерим шаблон и передаём историю из сессии
    return render_template('natural.html', history=session.get('natural_history', []))



@app.route('/natural/clear', methods=['POST'])
def clear_natural_history():
    # очистка истории натуральных чисел в текущей сессии
    session['natural_history'] = []
    session.modified = True
    flash('История очищена', 'info')  # сообщение об очистке
    return redirect(url_for('natural'))



@app.route('/integer', methods=['GET', 'POST'])
def integer():
    # история для целых чисел
    if 'integer_history' not in session:
        session['integer_history'] = []

    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = IntExpressionParser()              # парсер для целых
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
    # очистка истории для целых чисел
    session['integer_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('integer'))



@app.route('/rational', methods=['GET', 'POST'])
def rational():
    # история для рациональных чисел
    if 'rational_history' not in session:
        session['rational_history'] = []

    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = RatExpressionParser()          # парсер для рациональных
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
    # очистка истории рациональных чисел
    session['rational_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('rational'))



@app.route('/polynomial', methods=['GET', 'POST'])
def polynomial():
    # история для многочленов
    if 'polynomial_history' not in session:
        session['polynomial_history'] = []

    if request.method == 'POST':
        expression = request.form.get('math_exp')
        try:
            parser = PolExpressionParser()           # парсер для полиномиальных выражений
            result = parser.evaluate(expression)
            session['polynomial_history'].append({
                'expression': expression,
                'result': result
            })
            session.modified = True
            flash('Вычисление выполнено успешно!', 'success')

        except Exception as e:
            # флеш-сообщение об ошибке пользователю
            flash(f'Ошибка: {str(e)}', 'danger')
            # полный трейсбек ошибки в консоль для отладки
            traceback.print_exc()

        return redirect(url_for('polynomial'))

    # отдаём страницу с историей вычислений многочленов
    return render_template('polin.html', history=session.get('polynomial_history', []))



@app.route('/polynomial/clear', methods=['POST'])
def clear_polynomial_history():
    # очистка истории многочленов
    session['polynomial_history'] = []
    session.modified = True
    flash('История очищена', 'info')
    return redirect(url_for('polynomial'))



if __name__ == '__main__':
    # запуск приложения в режиме отладки (автоперезагрузка, подробные ошибки)
    app.run(debug=True)
