#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void parse_html(const char *html) {
    const char *tag_start = NULL;
    const char *tag_end = NULL;

    tag_start = strchr(html, '<');
    while (tag_start != NULL) {
        tag_end = strchr(tag_start, '>');

        if (tag_end != NULL) {
            size_t tag_length = tag_end - tag_start + 1;
            char *tag = (char *)malloc(tag_length + 1);
            if (tag == NULL) {
                fprintf(stderr, "failed\n");
                return;
            }
            strncpy(tag, tag_start, tag_length);
            tag[tag_length] = '\0';

            printf("Tag: %s\n", tag);
            free(tag);

            tag_start = strchr(tag_end, '<'); 
        } else {
            break;
        }
    }
}
