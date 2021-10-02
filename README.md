# Foodgram

Учебный приект Foodgram для Яндекс.Приктикум

Foodgram - интерактивная кулинарная книга.

Посмотреть проект можно сдесь:

[Foodgram]: http://62.84.122.62 "Foodgram"



#### Как запустить проект:

1. Установить Docker:

   ```http
   https://www.docker.com/products/docker-desktop
   ```

2. Клонировать репозиторий:

   ```http
   git@github.com:fincker13/foodgram-project-react.git
   ```

3. Создайте файл *.env* в дирректории */backend/* с переменными окружения для работы с базой данных:

   ```yaml
   DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
   DB_NAME=postgres # имя базы данных
   POSTGRES_USER=postgres # логин для подключения к базе данных
   POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
   DB_HOST=db # название сервиса (контейнера)
   DB_PORT=5432 # порт для подключения к БД
   ```

4. Перейти в дирректорию */infra/*. Запустите процесс сборки и запуска контейнеров. Для запуска в фоновом режиме примените ключ -d:

   ```bash
   docker-compose up
   ```

5. После завершния сборки и запуска контейнера, выполнить миграцию, создать суперюсера и загрузить статику:

   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate --noinput
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python manage.py collectstatic --no-input
   ```

6. Остановить работу и удалить контейнер можно командой:

   ```bash
   docker-compose down
   ```

   

   ### Технологии

   Проест разработан на Pyhton с использованием Django и DRF. В качестве базы данных используется PostgreSQL. Для контейнерезации используется Docker.

   

