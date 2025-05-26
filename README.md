## Самостоятельный проект: Микросервисное приложение с CI/CD

## Стек технологий
- **Backend**: `Flask (Python)`
- **База данных**: `MySQL 8.0`
- **Управление БД**: `Adminer`
- **Мониторинг**: `Prometheus, Grafana`
- **Контейнеризация**: `Docker, Docker Compose`
- **Оркестрация**: `Kubernetes`
- **CI/CD**: `GitHub Actions`

**Выполненные шаги :**

## 1. Контейнеризировал приложение USER-APP с помощью Docker и Docker Compose.
- Собрал Docker-образ на основе `python:3.10.11`.
- Настроил `docker-compose.yml` для управления сервисом.
  - Контейнер приложения (`api`) использует образ собранный и загруженный на DockerHub. Имеет тома для монтирования локальных файлов и папок. Запускается только после того, как сервис db станет (healthy), что определяется проверкой состояния (healthcheck) в конфигурации db. Указываются переменные окружения для настройки и управления поведением приложения без изменения его кода.   
  - Для базы (`db`) данных использовал образ `mysql:8.0` для базы данных. Для хранения данных создал том `db_data`, а также `healthcheck` дял проверки состояния контейнера.
  - Для управления базой данных(`adminer`) использовал `Adminer` последней версии (`adminer:latest`)
  - Мониторинг был реализован с помощью связки `Grafana + Prometheus` последних версий(данные собираются с помощью Prometheus и передаются в Gragfana для отображения)- метрика количество созданных пользователей.  
  - Для подключения контейнеров в одну сеть была создана сеть `app-network` с типом `bridge`
  - Также для всех контейнеров установлен параметр `depends_on` означающих их запуск только после запуска контейнера базы данных.
  - Указаны порты на которых работают контейнеры.     
## 2. Развернул приложение в Kubernetes(Minikube).
- Написал два манифеста - один для приложения и его сервисов, другой для мониторинга (с разными `namespace`).
- Для каждого сервиса написан `Deployment` и `Service`
- Деплоймент mysql имеет:
   - Манифест `PersistentVolumeClaim` для хранения данных после перезапуска пода.
   - `readinessProbe` проверка на то что под запущен.
   - Перменные окружения настройки и доступа в `Secret` - secrets.yaml
- Деплоймент api имеет:
  - Переменные окружения для подключения к базе данных в `Secret` - secrets.yaml
  - Подключенные тома для хранения файлов.
- Для `Api` и `Mysql` настроен HorizontalPodAutoscaler (HPA), для автоматичекого масштабирования подов в завимости от нагрузки (для сбора нагрузки используется  Metrics Server(metrics-server.yaml)).
## 3. Настройка мониторинга
  - Для монитронинга был написан отдельный манифест, с `namespase monitoring`. Через `ConfigMap` было реализовано хранение конфига для `prometheus`, подключение конфига происходит в деплойменте.
  - Также были написаны `NetworkPolicy`, который разрешает исходящий трафик к подам в пространстве имён (monitoring), а также исходящий трафик с простаства имен default c пометкой пода api.
## 4. СI/CD
 - Реализовано в GitHub Actions. Сборка `Dockerfile`, push образа на DockerHub c тэгом коммита (latest=tagcommit), деплой проекта с последним образом в `Kubernetes`.
## Мини-демо приложения
   ![Мой GIF](https://d3q44e7ubi1hi2.cloudfront.net/a875u6%2Fpreview%2F67503643%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D%22main_large.gif%22%3B&response-content-type=image%2Fgif&Expires=1748242035&Signature=DsEVePGRJdidKAks9MiREH8w9TiPFRBvi29YqXHEgu-Xy14CJuLgZ8fWUDldMHAN503~9Yf7ME5QSsg5py1lVJjrK585oMf75vnfwba-gcs9JGmSHXmxbZ2C7lhmab-ZXCKsq9SjJoebBUUMwCOowIUdsrCNnlVKx1YThQK16E7J37NANXWK1WwIFPn0kaoMN3UoL3ML8iaP5jRuOlfaTHiKL50HDGNlw3v8WLXTjreGrigBdaPQ6ouNY5izrVok1YTeshmteVC11c5O~mkzn1LdUlL-aXO~PXf6ekrFMDw2-zGnDN3MU9RqR0pDT~xnZfyx7BlMY2PoJcce3~8jJw__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ)
