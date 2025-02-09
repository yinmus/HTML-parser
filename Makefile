CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -shared
PYTHON = python3
PYTHONFLAGS =
SRC_DIR = parsers 
OBJ_DIR = ./obj
C_SRC = parsers/js_parser.c parsers/css_parser.c parsers/html_parser.c  
C_OBJ = $(C_SRC:parsers/%.c=$(OBJ_DIR)/%.o)  
TARGET_LIB = libparser.so

all: $(TARGET_LIB)

$(TARGET_LIB): $(C_OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: parsers/%.c
	@mkdir -p $(OBJ_DIR)  
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -rf $(OBJ_DIR) $(TARGET_LIB)

run: $(TARGET_LIB)
	$(PYTHON) server.py

lsof:
	@read -p "port : " PORT; \
	sudo lsof -i :$$PORT

