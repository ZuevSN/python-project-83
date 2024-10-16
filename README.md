### Hexlet tests and linter status:
[![Actions Status](https://github.com/ZuevSN/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ZuevSN/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/6aef59af0ad3d45e158e/maintainability)](https://codeclimate.com/github/ZuevSN/python-project-83/maintainability)

Для просмотра работы приложения - [Проект на Render](https://python-project-83-w2fz.onrender.com)

## Описание

[Page Analyzer](https://python-page-analyzer-ru.hexlet.app/) – это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с [PageSpeed Insights](https://pagespeed.web.dev/):
#
## Работа с программой:

В диалоговое окно вводится адрес страницы.

При проверке строка адреса нормализуется и проверяется на валидность.

Если успешно, то открывается страница проверки адреса на SEO-пригодность.

При нажатии Запустить проверку определяется статус страницы и подтягиваются данные со страницы.

На вкладке сайты можно просмотреть добавленные сайты и результаты последней успешной проверки, если такая проводилась

#
Минимальные требования: Python version 3.10; Poetry version 1.8.2
#

## Установка проекта:

  1.  Склонировать репозиторий

    git clone <https://github.com/ZuevSN/python-project-83.git>

  2.  Создать базу, пользователя для нее

  3.  Задать переменные окружения (в проекте есть пример .example_env)

  4.  Запустить установку зависимостей и создание необходимых таблиц

    make build

#

## Запуск проекта:

    make start
