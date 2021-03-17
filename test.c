#include <stdio.h>
#include <stdlib.h>
int main(int argc, char** argv) {
    printf("Main\n");
	if(argc != 2) {
		printf("Command type: %s 'word_to_parse'\n", argv[0]);
		exit(1);
	}
    return 0;
}