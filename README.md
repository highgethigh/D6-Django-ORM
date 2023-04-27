# D12-Django-ORM Логирование
# Перед запуском проекта запустить виртуальное окружение через консоль:
```
    source venv/bin/activate
```

### Настройки логирования должны выполнять следующее:
1. В консоль должны выводиться все сообщения уровня <b>DEBUG</b> и выше, включающие время, уровень сообщения, сообщения. Для сообщений <b>WARNING</b> и выше дополнительно должен выводиться путь к источнику события (используется аргумент <b>pathname</b> в форматировании). А для сообщений <b>ERROR</b> и <b>CRITICAL</b> еще должен выводить стэк ошибки (аргумент <b>exc_info</b>). Сюда должны попадать все сообщения с основного логгера <b>django</b>.
2. В файл <i>general.log</i> должны выводиться сообщения уровня <b>INFO</b> и выше только с указанием времени, уровня логирования, модуля, в котором возникло сообщение (аргумент <b>module</b>) и само сообщение. Сюда также попадают сообщения с регистратора <b>django</b>.  
3. В файл <i>errors.log</i> должны выводиться сообщения только уровня <b>ERROR</b> и <b>CRITICAL</b>. В сообщении указывается время, уровень логирования, само сообщение, путь к источнику сообщения и стэк ошибки. В этот файл должны попадать сообщения только из логгеров <b>django.request</b>, <b>django.server</b>, <b>django.template</b>, <b>django.db_backends</b>.
4. В файл <i>security.log</i> должны попадать только сообщения, связанные с безопасностью, а значит только из логгера <b>django.security</b>. Формат вывода предполагает время, уровень логирования, модуль и сообщение.
5. На почту должны отправляться сообщения уровней <b>ERROR</b> и выше из <b>django.request</b> и <b>django.server</b>, по формату как в <i>errors.log</i>, но без стэка ошибок.
Более того, при помощи фильтров указать, что в консоль сообщения отправляются только при <b>DEBUG = True</b>, а на почту и в файл <i>general.log</i> только при <b>DEBUG = False</b>.