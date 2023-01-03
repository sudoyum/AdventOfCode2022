#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include <regex.h>


#define DEBUG_PRINT 0

#define FAILURE -1
#define SUCCESS 0
#define INPUTLEN_GUESS 50

typedef enum shape {
  Rock = 1,
  Paper,
  Scissors
} Shape;

typedef enum result {
  Lose = 1,
  Draw,
  Win
} Result;

typedef struct Round {
  Shape play;
  Shape response;
} Round_t;

void solve_p1(void *input, int input_size) {
  Round_t *rounds = (Round_t *) input;

  int score = 0;
  for(int i = 0; i < input_size; i++) {
    score += rounds[i].response;
    if(rounds[i].play == rounds[i].response) {
      score += 3;
    } else if((rounds[i].play == Paper    && rounds[i].response == Scissors) ||
              (rounds[i].play == Scissors && rounds[i].response == Rock) ||
              (rounds[i].play == Rock     && rounds[i].response == Paper)) {
      score += 6;
    }
  }
  printf("PART1: %d\n", score);
}

void solve_p2(void *input, int input_size) {
  Round_t *rounds = (Round_t *) input;

  int score = 0;
  for(int i = 0; i < input_size; i++) {
    if(rounds[i].response == Lose) {
      score += (rounds[i].play == Rock ? Scissors: rounds[i].play - 1);
    } else if(rounds[i].response == Draw) {
      score += rounds[i].play + 3;
    } else if(rounds[i].response == Win) {
      score += (rounds[i].play == Scissors ? Rock: rounds[i].play + 1) + 6;
    }
  }
  printf("PART2: %d\n", score);
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

  Round_t *array = (Round_t *) malloc(sizeof(Round_t) * INPUTLEN_GUESS);
  int array_size = INPUTLEN_GUESS;
  int line_num = 0;

  while(-1 != getline(&line, &len, fp)) {
    if(line_num == array_size) {
      array_size += INPUTLEN_GUESS;
      array = (Round_t *) realloc(array, sizeof(Round_t) * array_size);
    }
    array[line_num].play = (Shape) (line[0] - 'A' + 1);
    array[line_num++].response = (Shape) (line[2] - 'X' + 1);
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
