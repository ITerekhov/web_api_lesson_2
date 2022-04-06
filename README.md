# web_api_lesson_2
## Работа с API сервиса [Bitly](https://app.bitly.com) по сокращению ссылок

### Установка
Для корректной работы скрипта необходимо установить библиотеки из файла *requirements.txt*:
```
$ pip3 install -r requirements.txt
```

### Запуск
Чтобы API сервис смог вас авторизовать и выполнять запросы, нужен токен. Вы можете получить его [на сайте](https://app.bitly.com/settings/api/) сервиса.
Для того чтобы использовать токен в скрипте создаёте файл *.env* и положите его туда, в формате `BITLY_TOKEN={bitly_token}`
Для запуска скрипта необходимо прописать в консоли команду:
```
$ python3 main.py your_url
```
Обратите внимание что url который вы хотите обработать указывается аргументом при запуске, в формате *https://example.com/example_path*.
Далее вам предложат ввести адрес какого-либо ресурса. Если ввести полный URL, срипт создаст и вернёт его сокращенную версию (bitlink).
Если ввести сразу bitlink, программа вернёт количество переходов по этой ссылке за всё время существования.
