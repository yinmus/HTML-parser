#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void parse_css(const char *css) {
    const char *selector_start = NULL;
    const char *selector_end = NULL;

    selector_start = strchr(css, '{');
    while (selector_start != NULL) {
        selector_end = strchr(selector_start, '}');
        if (selector_end != NULL) {
            size_t selector_length = selector_end - selector_start;
            char *selector = (char *)malloc(selector_length + 1);
            if (selector == NULL) {
                fprintf(stderr, "failed\n");
                return;
            }
            strncpy(selector, selector_start, selector_length);
            selector[selector_length] = '\0';

            printf("Selector: %s\n", selector);
            free(selector);

            selector_start = strchr(selector_end, '{');
        } else {
            break;
        }
    }
}
