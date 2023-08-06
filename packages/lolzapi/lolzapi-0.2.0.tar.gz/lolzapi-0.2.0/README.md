Библиотека создана для **максимального** простого кода при работа с lolz.guru API.

## Установка:

```
pip install lolzapi
```

## Примеры:

* Last post
  ```
  from lolzapi import pylolzapi

  client = pylolzapi.api("token")

  print(client.get.last_post(2430762))
  ```

* getMe function
  ```
  from lolzapi import pylolzapi

  client = pylolzapi.api("token")

  print(client.getMe())
  ```

## Список доступных методов:

* **GET**
  * *posts - Посты темы*
  * *last_post - Последний пост темы*
  * *threads - Темы раздела*
  * *findUser - Поиск пользователя*
  * *profilePosts - Посты пользователя*
  * *conversations - Ваши диалоги*

* **POST**
  * *post - Отправка сообщения в тему*
  * *like - Поставить симпатию на пост*
  * *profilePost - Отправить сообщение в профиль пользователя*

* **DELETE**
  * *like - Убрать лайк с поста*
  * *post - Удалить пост*

* **Прочее**
  * *getMe - информация про токен*