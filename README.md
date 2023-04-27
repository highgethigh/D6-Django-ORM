# D7-Django-ORM Cache
# Перед запуском проекта запустить виртуальное окружение через консоль:
```
    source venv/bin/activate
```
### Задание:
1. В категории должна быть возможность пользователей подписываться на рассылку новых статей в этой категории.
2. Если пользователь подписан на какую-либо категорию, то, как только в неё добавляется новая статья, её краткое содержание приходит пользователю на электронную почту, которую он указал при регистрации. В письме обязательно должна быть гиперссылка на саму статью, чтобы он мог по клику перейти и прочитать её.
3. Если пользователь подписан на какую-либо категорию, то каждую неделю ему приходит на почту список новых статей, появившийся за неделю с гиперссылкой на них, чтобы пользователь мог перейти и прочесть любую из статей.
4. Добавьте приветственное письмо пользователю при регистрации в приложении.

## P.S. для корректной работы, нужно добавить в <i>setting.py</i> почту для отправки сообщений пользователю!