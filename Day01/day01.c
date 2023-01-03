#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <regex.h>

#define DEBUG_PRINT 0

#define FAILURE -1
#define SUCCESS 0
#define INPUTLEN_GUESS 50

typedef struct Elf {
  int len;
  int *calories;
} Elf_t;

void solve_p1(void *input, int input_size) {
  int max = -1;
  for(int i = 0; i < input_size; i++) {
    Elf_t elf = ((Elf_t *)input)[i];
    int sum = 0;
    for(int j = 0; j < elf.len; j++) {
      sum += elf.calories[j];
    }
    if(sum > max) {
      max = sum;
    }
  }
  printf("PART1: %d\n", max);
}

void solve_p2(void *input, int input_size) {
  int max[3] = {-1};
  for(int i = 0; i < input_size; i++) {
    Elf_t elf = ((Elf_t *)input)[i];
    int sum = 0;
    for(int j = 0; j < elf.len; j++) {
      sum += elf.calories[j];
    }

    int lowest = max[0];
    int lowest_index = 0;
    for(int k = 1; k < 3; k++) {
      if(max[k] < lowest) {
        lowest = max[k];
        lowest_index = k;
      }
    }
    if(sum > max[lowest_index]) {
      max[lowest_index] = sum;
    }
  }
  printf("PART2: %d\n", max[0] + max[1] + max[2]);
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

  Elf_t *array = (Elf_t *) malloc(sizeof(Elf_t) * INPUTLEN_GUESS);
  int array_size = INPUTLEN_GUESS;
  int elf_num = 0;
  int *calories = (int *) malloc(sizeof(int *));
  int calories_array_size = 1;
  int calories_len = 0;

  while(-1 != getline(&line, &len, fp)) {
    if(elf_num == array_size) {
      array_size += INPUTLEN_GUESS;
      array = (Elf_t *) realloc(array, sizeof(Elf_t) * array_size);
    }

    if(!strncmp(line, "\n", 1)) {
      array[elf_num].calories = calories;
      array[elf_num++].len = calories_len;
      calories = (int *) malloc(sizeof(int *));
      calories_array_size = 1;
      calories_len = 0;
    } else {
      if(calories_len == calories_array_size) {
        calories_array_size++;
        calories = (int *) realloc(calories, sizeof(int *) * calories_array_size);
      }
      calories[calories_len++] = atoi(line);
    }
  }

  array[elf_num].calories = calories;
  array[elf_num++].len = calories_len;

  *arr = array;
  *arr_size = elf_num;

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
    for(int i = 0; i < input_size; i++) {
      Elf_t elf = ((Elf_t *)input)[i];
      if(elf.calories) {
        free(elf.calories);
        elf.calories = NULL;
      }
    }
    free(input);
    input = NULL;
  }

  return rc;
}
