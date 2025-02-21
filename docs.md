# HTML/CSS/JS Parser & HTTP Server

Этот проект представляет собой HTTP-сервер, который обслуживает HTML, CSS и JavaScript файлы, а также анализирует их содержимое с помощью библиотеки на C.

## Компоненты проекта

### [`html_parser.c`](parsers/html_parser.c)
- Извлекает HTML-теги из переданного файла.
- Использует `strchr()` для поиска `<` и `>`.

### [`css_parser.c`](parsers/css_parser.c)
- Извлекает селекторы из CSS-файла.
- Использует `strchr()` для поиска `{` и `}`.

### [`js_parser.c`](parsers/js_parser.c)
- Находит объявления функций в JavaScript.
- Использует `strstr()` для поиска `function`.


### [`server.py`](server.py)

- Запускает HTTP-сервер на заданном порту.
- Проверяет занятость порта и предлагает убить процесс, если порт уже используется.
- Позволяет выбрать файлы (HTML, CSS, JS) через аргументы командной строки или интерактивное меню.
- Подключает `libparser.so` через `ctypes` для анализа содержимого файлов.
- При запросах:
  - Парсит HTML при открытии главной страницы.
  - Парсит CSS при запросе `/styles.css`, если указан CSS-файл.
  - Парсит JS при запросе `/script.js`, если указан JS-файл.

### [`makefile`](Makefile)
- Компилирует библиотеку `libparser.so` (или `.dll/.dylib` для Windows/Mac).
- Очищает скомпилированные файлы.
- Запускает сервер.

## Зависимости

### 1. Для работы сервера (`server.py`):
- **[Python 3](https://python.org)** (рекомендуется 3.6+)
- **Модули Python** (все встроенные, ничего устанавливать не нужно):
  - [`os`](https://docs.python.org/3/library/os.html)
  - [`sys`](https://docs.python.org/3/library/sys.html)
  - [`ctypes`](https://docs.python.org/3/library/ctypes.html)
  - [`signal`](https://docs.python.org/3/library/signal.html)
  - [`socket`](https://docs.python.org/3/library/socket.html)
  - [`http.server`](https://docs.python.org/3/library/http.server.html)
  - [`socketserver`](https://docs.python.org/3/library/socketserver.html)

### 2. Для сборки библиотеки (`libparser.so`):
- **Компилятор C**:
  - [`GCC`](https://gcc.gnu.org/) (Linux)
  - [`Clang`](https://clang.llvm.org/) (MacOS)
  - [`MinGW`](https://www.mingw-w64.org/) (Windows)
- [`Make`](https://www.gnu.org/software/make/) (для удобной сборки)

### 3. Для работы на Windows:
- [`MSYS2`](https://www.msys2.org/) (рекомендуется для сборки через MinGW)
- Или [`Cygwin`](https://www.cygwin.com/) (если используете `make`)

___
## Сборка и запуск


### 1. Сборка библиотеки
```sh
make
```
### 2. Очистка 
```sh
make clean
```
___
## Функции 

```bash
python3 server.py
```

```bash
python3 server.py <порт> <HTML-файл> <JS-файл> <CSS-файл>
```

```bash
python3 server.py 8080 index.html None None
```

```bash
python3 server.py 8080 index.html None style.css
```

```bash
python3 server.py 8080 index.html scr.js style.css
```









