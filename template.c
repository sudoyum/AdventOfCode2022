#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <regex.h>

#define DEBUG_PRINT 0

#define FAILURE -1
#define SUCCESS 0
#define INPUTLEN_GUESS 50


void solve_p1(void *input, int input_size) {
  printf("PART1:\n");
}

void solve_p2(void *input, int input_size) {
  printf("PART2:\n");
}

int parse_file(char *file_name, void **arr, int *arr_size) {
  FILE *fp = NULL;
  size_t len;
  char *line = NULL;
  int rc = SUCCESS;

  if(NULL == (fp = fopen(file_name, "r"))) {
    printf("failed to open input file %s, exiting\n", file_name);
    rc = FAILURE;
    goto cleanup;
  }

  int *array = (int *) malloc(sizeof(int) * INPUTLEN_GUESS);
  int array_size = INPUTLEN_GUESS;
  int line_num = 0;

  while(-1 != getline(&line, &len, fp)) {
    if(line_num == array_size) {
      array_size += INPUTLEN_GUESS;
      array = (int *) realloc(array, sizeof(int) * array_size);
    }
    array[line_num++] = atoi(line);
  }

  *arr = array;
  *arr_size = line_num;

cleanup:
  if(line) {
    free(line);
    line = NULL;
  }
  if(fp) {
    fclose(fp);
    fp = NULL;
  }

  return rc;
}

int main(int argc, char *argv[]) {
  void *input = NULL;
  int input_size;
  int rc = EXIT_SUCCESS;

  if(argc != 3) {
    rc = EXIT_FAILURE;
    printf("usage: ./dayXX input.txt p1|p2|both\n");
    goto cleanup;
  }

  if(FAILURE == parse_file(argv[1], &input, &input_size)) {
    printf("failed to parse %s\n", argv[1]);
    rc = EXIT_FAILURE;
    goto cleanup;
  }

  if(!strcmp(argv[2], "p1")) {
    solve_p1(input, input_size);
  } else if(!strcmp(argv[2], "p2")) {
    solve_p2(input, input_size);
  } else if(!strcmp(argv[2], "both")) {
    solve_p1(input, input_size);
    solve_p2(input, input_size);
  } else {
    rc = EXIT_FAILURE;
    printf("usage: ./dayXX input.txt p1|p2|both\n");
    goto cleanup;
  }

cleanup:
  if(input) {
    free(input);
    input = NULL;
  }

  return rc;
}
