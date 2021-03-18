# HelBotQuiz

HelBotQuiz permite la creacion de un cuestionario con preguntas abiertas 
y de opción multiple, todas administrables desde el admin de Django.

Estas preguntas son enviadas mediante python-telegram-bot a un bot creado en
Telegram.

Las interacciones del usuario con el bot son trackeadas para posteriormente
poder hacer un analisis de los datos y sacar conclusiones.

Version de python: 3.9.2

## Instalación

IMPORTANTE: Para poder realizar el envio de mensajes con Telegram es importante
contar ya con tu TOKEN de autenticacion y bot configurado, guia de configuración:
https://core.telegram.org/bots#6-botfather

1.- Crear un entorno virtual con:
```bash
python -m venv hel_bot_quiz_venv
```

2.- Activar el entorno virtual:
```bash
source hel_bot_quiz_venv/bin/active
```

3.- Clonar el repositorio:
```bash
git clone https://github.com/ArmandoVn/hal_telegram_bot.git
```

4.- Entrar en la carpeta del proyecto:
```bash
cd hal_telegram_bot
```

5.- Instalamos las dependencias:
```bash
pip install requirements.txt
```

6.- Crear el local_settings.py:
```bash
cp local_settings.template local_settings.py
```

7.- Modificar las credenciales para el BotFather
    en el local_settings.py

8.- Ejecutar las migraciones:
```bash
python manage.py migrate
```

9.- Crear un susper usuario para acceder al admin de Django:
```bash
python manage.py createsuperuser
```

10.- Ejecutar el proyecto:
```bash
python manage.py runserver
```

# Referencias y guias de consulta:
Python Telegram Bot (python-telegram-bot):
https://python-telegram-bot.readthedocs.io/en/stable/telegram.chat.html

Configuracion inicial de Bot con python-telegram-bot:
https://github.com/python-telegram-bot/python-telegram-bot

Ejemplos de configuracion:
https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

Libreria pre configuradas para diferentes lenguajes:
https://core.telegram.org/bots/samples

Tipos de bots:
https://core.telegram.org/bots