
ifeq ($(OS),Windows_NT)
  CC = gcc
  CFLAGS = -Wall -fPIC
  LDFLAGS = -shared
  TARGET_LIB = libparser.dll
  PYTHON = python
  OBJ_DIR = ./obj/windows
  EXE_EXT = .exe
  RM = del /f /q
else ifeq ($(shell uname), Darwin)
  CC = clang
  CFLAGS = -Wall -fPIC
  LDFLAGS = -shared
  TARGET_LIB = libparser.dylib
  PYTHON = python3
  OBJ_DIR = ./obj/mac
  RM = rm -rf
else
  CC = gcc
  CFLAGS = -Wall -fPIC
  LDFLAGS = -shared
  TARGET_LIB = libparser.so
  PYTHON = python3
  OBJ_DIR = ./obj/linux
  RM = rm -rf
endif

SRC_DIR = parsers
C_SRC = $(SRC_DIR)/js_parser.c $(SRC_DIR)/css_parser.c $(SRC_DIR)/html_parser.c
C_OBJ = $(C_SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

all: $(TARGET_LIB)

$(TARGET_LIB): $(C_OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	$(RM) $(OBJ_DIR) $(TARGET_LIB)

run: $(TARGET_LIB)
	$(PYTHON) server.py

#Если Linux
#lsof:
#	@read -p "port : " PORT; \
#	sudo lsof -i :$$PORT

