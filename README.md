# FairOlymp: Проводим честные олипиады!

>[!TIP]
>**Деплой проекта [f-olymp.uxp.ru](f-olymp.uxp.ru)**

## Описание функционала
Основные функции перечислены на странице ```/```

## Структура
```
.
├── app/                          # Main application directory
│   ├── __init__.py              # Flask application initialization
│   ├── forms.py                 # Form definitions for user input
│   ├── models.py                # Database models
│   ├── routes.py                # Application routes and view functions
│   ├── static/                  # Static assets directory
│   │   ├── css/                 # CSS stylesheets
│   │   ├── js/                  # JavaScript files including React components
│   │   └── styles.css          # Custom application styles
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html            # Base template with common layout
│       ├── organizer_*.html     # Organizer-specific templates
│       └── participant_*.html   # Participant-specific templates
├── config.py                    # Application configuration
├── requirements.txt             # Python package dependencies
└── run.py                      # Application entry point
```

## Развертка у себя

### Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/Hong-Chai/FairOlimp_X.git
cd fairOlymp
```

2. Создайте виртуальное окружение:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### Запуск
1. Запустите сервер:
```bash
python run.py
```

2. Откройте у себя:
- В бразере в адресную строку введите `http://localhost:5000`

