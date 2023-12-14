# Качаем почту с Gmail

Это простой скрипт, который выкачивает почту из ящика на Gmail. Для каждого сообщения получает следующие поля:

- snippet — "превью" текста. Чаще всего вообще не связано с телом письма
- subject — тема письма
- date — дата получения(?) письма
- from — отправитель

## Требования

Для запуска вам понадобится:

- Python 3.6 или выше
- [Получить ключ](https://developers.google.com/gmail/api/quickstart/python) для доступа к Google API.

Ключ представляет собой JSON-файл с именем что-то вроде `client_secret_0000000aaaaaa.apps.googleusercontent.com.json`. Путь к этому файлу нужно вписать в файл переменных окружения — `.env`:

```bash
GMAIL_CREDENTIALS=/path/to/client_secret_0000000aaaaaa.apps.googleusercontent.com.json
```

## Запуск

Запустите скрипт:

```bash
python main.py > messages.txt
```

При первом запуске вам будет нужно войти в свой Google-аккаунт, чтобы получить токены доступа.

По-умолчанию Gmail отдает только 500 последних писем, хотя в стоит `maxResults=1000` в запросе.

TODO: получить письма с последующих страниц. Для этого в объекте `response` есть ключ `nextPageToken`. Его надо поставить в вызов `response = service.users().messages().list(userId="me", maxResults=1000, pageToken=...).execute()`
