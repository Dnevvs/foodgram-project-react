# foodgram-project-react

Доменное имя:
```
    firsttask.ddns.net
```
В случае временной недоступности доменного имени, проект доступен по адресу:
```
158.160.23.82:8000
```
Email для логина:
```
   dnevvs@yandex.ru
```
пароль:
```
   adfmin69 
```
### Функционал приложения «Продуктовый помощник»: 
## Зарегистрированные пользователи могут:
* публиковать рецепты, 
* добавлять чужие рецепты в избранное,
* подписываться на публикации других авторов.
## Незарегистрированные пользователи могут:
* просматривать рецепты и страницы других пользователей.
## Cервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
## **Деплой проекта Foodgram на удалённый сервер c помощью CI/CD**
### 1.	Клонируйте репозиторий foodgram-project-react с проектом Foodgram с аккаунта на GitHub на локальный компьютер.

```
    git clone 'git@github.com:Dnevvs/foodgram-project-react.git'
```
### 2. Переходим в директорию проекта.

```
    cd foodgram-project-react/
```
### 3.	Настройте на удаленном сервере веб-сервер Nginx для перенаправления запросов и работы со статикой проекта Foodgram: 
Опишите нужные настройки в существующем файле конфигурации.
```
    sudo nano /etc/nginx/sites-enabled/default 
```
```
server {
    server_name 158.160.23.82 firsttask.ddns.net;

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
    server_name 158.160.23.82` firsttask.ddns.net;
    listen 80;
    return 404;
}
Перезапустите сервер:
```    
    sudo nginx -t
    sudo systemctl reload nginx 
```    ```
### 4. Подготовить папку foodgram на удаленном сервере.
На удаленном сервере создайте папку ```foodgram```.
В папку скопируйте файл ```.env``` из корневой папки проекта.
В папку скопируйте файл ```docker-compose.production.yml``` из корневой папки проекта.
### 5. Запуску деплоя на удаленный сервер:
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
