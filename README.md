<h1></h1>


<h2>Запуск приложения</h2>
Инструкция предполагает что у вас установлен docker и docker-compose
Через консоль, в корневой папке проекта, запустить команду "docker-compose up -d --build"

После успешного запуска приложения перейдите по ссылке "https://127.0.0.1:8000/api"

<h2>Компоненты приложения</h2>
Важные файлы в приложении
- .app/orders_api/api_calls/<b>google_sheets.py</b>
- .app/orders_api/api_calls/<b>usd_to_rub_exchange_rate.py</b>
- .app/orders_api/management/commands/<b>updatedb.py</b>

<br>
<p><b>google_sheets.py</b></p>
<p>В этом файле находится вся логика сбора данных с Google Sheets.<br>
Сбор данных реализован через google service client и ему нужен <b>service_client_secret.json</b>
в той же папке.</p>
<br>
<p><b>usd_to_rub_exchange_rate.py</b></p>
<p>Делает запрос на сайт ЦБ чтобы получить актуальный курс обмена доллара на рубль.</p>
<br>
<p><b>updatedb.py</b></p>
<p>Создает новую комманду для django-admin.<br>
Комманда использует два прошлых файла чтобы занести данные с Google Sheets в нашу базу данных</p>

<br>
<p>Периодичное обновление данных реализовано при помощи crond.
<br>каждую минуту на сервере вызывается команда <b>"updatedb"</b> которая обновляет данные
<br>Так же при каждом посещении главной страницы данные тоже обновляются</p>