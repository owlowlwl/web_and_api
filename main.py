from flask import Flask, render_template, request
import requests
import json

# Создаем экземпляр Flask
app = Flask(__name__)
app.config["DEBUG"] = True  # убрать позже
# Ключ для вк api
access_token = 'b7149157b7149157b714915791b4074310bb714b7149157d35afb958701192c29e38603'


# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем название города из формы
        city_name = request.form.get('city')

        # Получаем id города
        cities_request = "https://api.vk.com/method/database.getCities?country_id=1&q=" \
                         f"{city_name}&access_token={access_token}&v=5.131"
        response = requests.get(cities_request).json()
        city_id = response['response']['items'][0]['id']

        url = "https://api.vk.com/method/database.getSchools"
        params = {
            "city_id": city_id,
            "count": 1000,
            "access_token": access_token,
            "v": "5.131"
        }
        response = requests.get(url, params=params)

        schools = json.loads(response.content)['response']['items']
        print(schools)

        # # Сортируем школы по рейтингу от лучшей к худшей
        # schools = sorted(schools, key=lambda x: x['rating'], reverse=True)
        #
        # Выделяем три лучшие школы другим цветом
        top_schools = schools[:3]

        # Рендерим шаблон с результатом
        return render_template('result.html', schools=schools, top_schools=top_schools)

    # Рендерим шаблон формы ввода
    return render_template('index.html')


# Запускаем приложение Flask
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=8080)
