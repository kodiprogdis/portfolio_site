import os
import sys

import requests
from flask import Flask, render_template, request

app = Flask(__name__)
STATIC_DIR = os.path.abspath(os.path.dirname(__file__)) + "/static"

menu = ["Портфолио", "Заказать", "Контакты"]


def getImage():
	map_request = "http://static-maps.yandex.ru/1.x/?ll=52.287995,54.898339&spn=0.002,0.002&l=map"
	response = requests.get(map_request)
	if not response:
		print("Ошибка выполнения запроса:")
		print(map_request)
		print("Http статус:", response.status_code, "(", response.reason, ")")
		sys.exit(1)
	# Записываем полученное изображение в файл.
	map_file = "map.png"
	with open(os.path.join(STATIC_DIR, map_file), "wb") as file:
		file.write(response.content)
	return map_file


images = [  # картинки для Наших товаров
	{"src": "VK-LOGO.png", "alt": "VK", "text": "VK", "id": 1},
	{"src": "ya.png", "alt": "Telegram", "text": "Telegram", "id": 2},
	{"src": "ok.png", "alt": "Однокласники", "text": "Однокласники", "id": 3},
	{"src": "iphone.jpg", "alt": "Iphone", "text": "Iphone", "id": 4},
]


@app.route('/')
def index():
	return render_template('index.html', menu=menu)


@app.route('/portfolio')
def items():
	# Отображение страницы "Наши товары" с изображениями
	return render_template('portfolio.html', images=images, menu=menu)


@app.route('/contacts', methods=['GET', 'POST'])
def about():
	if request.method == 'POST':
		name = request.form['name']
		phone = request.form['phone']
		with open('file.txt', 'a') as f:
			f.write(f"Имя: {name}, Телефон: {phone}\n")
		return '<h1>Спасибо за регистрацию!</h1>'
	return render_template('contacts.html')


@app.route('/map')
def map():
	map_file = getImage()
	return render_template('map.html', images=images, menu=menu, map_file=map_file)


if __name__ == '__main__':
	app.run(debug=True)
