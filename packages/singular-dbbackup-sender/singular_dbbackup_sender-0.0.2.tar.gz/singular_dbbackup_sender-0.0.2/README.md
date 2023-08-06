#README

Esta lib é um gerador de backups automatizado, criado para rodar com um cronjob
Para configura-lo é necessário incluir as variáveis: `BACKUP_FOLDER,DBBACKUP_FILENAME_TEMPLATE, EMAILS_BACKUP`
no arquivo de configurações (settings.py), assim como **singular_database_generator** no INSTALLED_APPS

**Configuração do cronjob**

Para configurar o cronjob, basta apenas incluir
`CRONJOBS = [
    singular_database_generator.database_backup.BACKUP_CRONJOB
]`
