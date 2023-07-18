# foodgram-project-react
## **Деплой проекта Kittygram на удалённый сервер c помощью CI/CD**

Доменное имя
```
    firsttask.ddns.net
```
email для логина
```
   dnevvs@yandex.ru
```
пароль
```
   adfmin
```
### 1.	Клонируйте репозиторий kittygram_final с проектом Kittygram со своего аккаунта на GitHub на локальный компьютер.

```
    git clone 'git@github.com:Dnevvs/foodgram-project-react.git'
```
### 2. Переходим в директорию проекта.

```
    cd foodgram-project-react/
```
### 3. Создаём виртуальное окружение.
```
    python -m venv venv
```
### 4. Активируем виртуальное окружение.
```
    source venv/scripts/activate
```
### 5. Устанавливаем зависимости.
```
    pip install -r requirements.txt
```
### 6. Переходим в директорию backend-приложения проекта.
```
	cd backend
```
### 7. Применяем миграции.
```
	python manage.py migrate
```
### 8.Создаём суперпользователя.
```
    python manage.py createsuperuser
```
### 9. Перейдите в директорию foodgram-project-react/frontend/ и выполните команду:
```
	npm i 
```
### 10.	Настройте веб-сервер Nginx для перенаправления запросов и работы со статикой проекта Foodgram: 
Опишите нужные настройки в существующем файле конфигурации.
```
    sudo nano /etc/nginx/sites-enabled/default 
```
```
server {
    server_name 130.193.53.253 firsttask.ddns.net;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }

    location /sentry-debug/ {
        proxy_pass http://127.0.0.1:8000;
    }
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/firsttask.ddns.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/firsttask.ddns.net/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

}
server {
    if ($host = firsttask.ddns.net) {
        return 301 https://$host$request_uri;
    }
    server_name 130.193.53.253 firsttask.ddns.net;
    listen 80;
    return 404;
}
Перезапустите сервер:
```    
    sudo nginx -t
    sudo systemctl reload nginx 
```    ```
### 11. Подготовить папку foodgram на удаленном сервере.
На удаленном сервере создайте папку ```foodgram```.
В папку скопируйте файл ```.env``` из корневой папки проекта.
В папку скопируйте файл ```docker-compose.production.yml``` из корневой папки проекта.
### 12. Запуску деплоя на удаленный сервер:
На локальном компютере в папке foodgram-project-react допишите свой никнейм в данный файл README.md.
Затем последовательно выполните команды.
```
    git add .
    git commit -m 'Deploy'
    git push
```
На удаленном сервере автомтически развернется проект и будте доступен по доменному имени:
```
    firsttask.ddns.net
```
Никнейм: Dnevvs
