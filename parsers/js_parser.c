#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void parse_js(const char *js) {
    const char *func_start = NULL;
    const char *func_end = NULL;

    func_start = strstr(js, "function");
    while (func_start != NULL) {
        func_end = strchr(func_start, '{');
        if (func_end != NULL) {
            size_t func_length = func_end - func_start;
            char *func_name = (char *)malloc(func_length + 1);
            if (func_name == NULL) {
                fprintf(stderr, "failed\n");
                return;
            }
            strncpy(func_name, func_start, func_length);
            func_name[func_length] = '\0';

            printf("Function: %s\n", func_name);
            free(func_name);

            func_start = strstr(func_end, "function");
        } else {
            break;
        }
    }
}
