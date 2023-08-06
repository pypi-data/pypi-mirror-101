Библиотека создана для **максимального** простого кода при работа с **lolz.guru API**.

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
  * *notifications - Cписок оповещений*
  * *pages - Список разделов в системе*
  * *pagesById - Информация про раздел*

* **POST**
  * *post - Отправка сообщения в тему*
  * *like - Поставить симпатию на пост*
  * *profilePost - Отправить сообщение в профиль пользователя*
  * *sub - Подписаться на юзера*
  * *conversation - Написать сообщение в личну*
  * *likeProfilePost - Лайкнуть пост профиля*

* **DELETE**
  * *like - Убрать лайк с поста*
  * *post - Удалить пост*
  * *thread - Удалить тему*
  * *sub - Отписаться*
  * *profilePost - Удалить пост в профиле*
  * *LikeProfilePost - Удалить лайк с поста*

* **PUT**
  * *editMessage - Редактировать сообщение в лс*
  * *profilePost - Редактировать пост в профиле*

* **Прочее**
  * *getMe - информация про токен*