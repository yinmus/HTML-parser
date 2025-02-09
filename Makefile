CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -shared
PYTHON = python3
PYTHONFLAGS =
SRC_DIR = parsers  # Путь к директории с исходными файлами
OBJ_DIR = ./obj
C_SRC = parsers/js_parser.c parsers/css_parser.c parsers/html_parser.c  # Явное указание пути
C_OBJ = $(C_SRC:parsers/%.c=$(OBJ_DIR)/%.o)  # Сборка объектных файлов в obj/
TARGET_LIB = libparser.so

all: $(TARGET_LIB)

$(TARGET_LIB): $(C_OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: parsers/%.c
	@mkdir -p $(OBJ_DIR)  # Убедимся, что obj существует
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -rf $(OBJ_DIR) $(TARGET_LIB)

run: $(TARGET_LIB)
	$(PYTHON) server.py

lsof:
	@read -p "port : " PORT; \
	sudo lsof -i :$$PORT

