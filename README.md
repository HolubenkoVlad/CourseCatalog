# Каталог курсів
Для виконання цього завдання була використана мова програмування Python, веб-фреймворк Flask, база даних SQLite та ORM Peewee.
### Розгортання проекту
##### Запуск на вбудованому сервері
Зайти в папку `venv\Scripts`.
Відкрити в цій папці `командний рядок Windows`.
Виконати команду `python.exe ..\..\manage.py runserver`.
##### Azure Web Apps
Щоб розгорнути застосунок на Azure потрібно вказати у налаштуваннях App Service файл запуску.
Для цього потрібно перейти в `Settings-> Configuration->General settings` та вказати у `Startup Command` файл `startup.txt`.
Для розгортання використовується команда `az webapp up`.
### Таблиця курсів
```
CREATE TABLE Course(
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  lectures_number integer);
```

### Endpoints
| Методи      | Опис | URL     | Приклад запиту | JSON|
| :---        |    :----   |          :--- | :---| :---|
| GET      | Отримання повного списку курсів       | /courses/   |http://127.0.0.1:5000/courses/|
| GET      | Отримання курсу по id       | /course/<int:course_id>   |http://127.0.0.1:5000/course/4|
| GET   | Фільтрування списку курсів за вказаними параметрами. Фільтрування доступне за полями name, start_date та end_date. Дані передаються як параметри        | /courses/|http://127.0.0.1:5000/courses/|```{"name":"Java","start_date":"2021-03-30","end_date":"2021-09-30"}```
| POST   | Додавання нового курсу. Дані передаються в форматі json      | /new/course/ |http://127.0.0.1:5000/new/course/ |```{"name": "C++ Course Advanced","start_date": "2021-06-30","end_date": "2021-09-30","lectures_number": 30} ```|
| DELETE   | Видалення курсу за id        | /delete/course/<int:course_id>     |http://127.0.0.1:5000/delete/course/3|
| PUT   | Оновлення курсу за id. Дані для оновлення передаються в форматі json       | /update/course/<int:course_id>   |http://127.0.0.1:5000/update/course/5|```{"name": "C++ Course Advanced","end_date": "2021-09-30","lectures_number": 10} ```|
