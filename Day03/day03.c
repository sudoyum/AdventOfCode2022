#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include <regex.h>

#define DEBUG_PRINT 0

#define FAILURE -1
#define SUCCESS 0
#define INPUTLEN_GUESS 50

typedef struct RuckSack {
  char *full_str;
  char *compartment1;
  char *compartment2;
  int len;
} RuckSack_t;

int ascii_to_value(char c) {
  if(c > 'Z') {
    return c - 'a' + 1;
  } else {
    return c - 'A' + 1 + 26;
  }
}

char find_duplicate(RuckSack_t *rs) {
  for(int i = 0; i < rs->len; i++) {
    for(int j = 0; j < rs->len; j++) {
      if(rs->compartment1[i] == rs->compartment2[j]) {
        return rs->compartment1[i];
      }
    }
  }
}

char find_dups(char *s1, char *s2) {
  for(int i = 0; i < strlen(s1); i++) {
    for(int j = 0; j < strlen(s2); j++) {
      if(s1[i] == s2[j]) {
        return s1[i];
      }
    }
  }
  printf("ERROR\n");
}

void find_duplicates(char *s1, char *s2, char *duplicates) {
  int duplicates_index = 0;

  for(int i = 0; i < strlen(s1); i++) {
    for(int j = 0; j < strlen(s2); j++) {
      if(s1[i] == s2[j]) {
        bool already_exists = false;
        for(int k = 0; k < duplicates_index; k++) {
          if(duplicates[k] == s1[i]) {
            already_exists = true;
            break;
          }
        }
        if(!already_exists) {
          duplicates[duplicates_index++] = s1[i];
        }
      }
    }
  }
  duplicates[++duplicates_index] = '\0';
}

void solve_p1(void *input, int input_size) {
  RuckSack_t *rucksacks = (RuckSack_t *) input;
  int duplicates_sum = 0;

  for(int i = 0; i < input_size; i++) {
    duplicates_sum += ascii_to_value(find_duplicate(&rucksacks[i]));
  }
  printf("PART1: %d\n", duplicates_sum);
}

void solve_p2(void *input, int input_size) {
  RuckSack_t *rucksacks = (RuckSack_t *) input;

  int duplicates_sum = 0;


  for(int i = 0; i < input_size; i += 3) {
    char round1[256] = {'\0'};
    char round2[256] = {'\0'};
    find_duplicates(rucksacks[i].full_str, rucksacks[i + 1].full_str, round1);
    find_duplicates(rucksacks[i + 2].full_str, round1, round2);
    duplicates_sum += ascii_to_value(round2[0]);
  }
  printf("PART2: %d\n", duplicates_sum);
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

  RuckSack_t *array = (RuckSack_t *) malloc(sizeof(RuckSack_t) * INPUTLEN_GUESS);
  int array_size = INPUTLEN_GUESS;
  int line_num = 0;

  while(-1 != getline(&line, &len, fp)) {
    if(line_num == array_size) {
      array_size += INPUTLEN_GUESS;
      array = (RuckSack_t *) realloc(array, sizeof(RuckSack_t ) * array_size);
    }
    int full_len = strlen(line);
    int compartment_len = (full_len - 1)/2;

    array[line_num].compartment1 = (char *) malloc(sizeof(char) * compartment_len + 1);
    array[line_num].compartment2 = (char *) malloc(sizeof(char) * compartment_len + 1);
    array[line_num].full_str = (char *) malloc(sizeof(char) * full_len);

    array[line_num].compartment1 = strncpy(array[line_num].compartment1, (char *) &line[0], compartment_len);
    array[line_num].compartment2 = strncpy(array[line_num].compartment2, (char *)&line[compartment_len], compartment_len);
    array[line_num].full_str = strncpy(array[line_num].full_str, (char *) line, full_len);

    array[line_num].compartment1[compartment_len] = '\0';
    array[line_num].compartment2[compartment_len] = '\0';
    array[line_num].full_str[compartment_len * 2] = '\0';
    array[line_num++].len = compartment_len;
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
    RuckSack_t *rs = (RuckSack_t *)input;
    for(int i = 0; i < input_size; i++) {
      free(rs[i].compartment1);
      free(rs[i].compartment2);
      free(rs[i].full_str);
    }
    free(input);
    input = NULL;
  }

  return rc;
}
