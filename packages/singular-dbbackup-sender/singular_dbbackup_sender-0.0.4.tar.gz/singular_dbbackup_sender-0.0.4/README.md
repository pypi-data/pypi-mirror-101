# README

Esta lib é um gerador de backups automatizado, criado para rodar com um cronjob

**Configuração do cronjob**
Inclua no arquivo de configurações (settings.py) as seguintes variáveis:

` APP_NAME = nome da pasta do seu projeto (Ex: produx)`

` DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'`

` DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, APP_NAME, 'backups')}`

`DEFAULT_FROM_EMAIL = email`

`EMAILS_BACKUP = [emails] ou ADMINS = [(Nome, email)]`
Caso queira incluir uma rotina de cronogramas, inclua 

`CRONJOBS = [
BACKUP_CRONJOB
]`
