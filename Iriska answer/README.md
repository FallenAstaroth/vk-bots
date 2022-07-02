# Iriska answer

Решает примеры [Ириска Кошкина | Bot](https://vk.com/club173471303).

## Настройка бота

1. Устанавливаем зависимости:

`pip install -r requirements.txt`

2. Заполняем поля файла `config.py`:

| Поле                   | Описание                                                |
|------------------------|---------------------------------------------------------|
| TOKEN                  | Токен от страницы                                       |
| MIN_SLEEP              | Минимальная задержка в секундах перед отправкой ответа  |
| MAX_SLEEP              | Максимальная задержка в секундах перед отправкой ответа |

Токен получаем [здесь](https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)
