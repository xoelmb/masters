#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

/*
 * DNA Alphabet
 */
//#define ALPHABET_SIZE 26
//char alphabet[] = {
//    'A','B','C','D','E',
//    'F','G','H','I','J',
//    'K','L','M','N','O',
//    'P','Q','R','S','T',
//    'U','V','W','X','Y',
//    'Z'
//};
#define ALPHABET_SIZE 4
char alphabet[] = {
    'A','C','G','T'
};

/*
 * Random number generator
 */
uint64_t rand_iid(const uint64_t min,const uint64_t max) {
  int n_rand = rand(); // [0, RAND_MAX]
  const uint64_t range = max - min;
  const uint64_t rem = RAND_MAX % range;
  const uint64_t sample = RAND_MAX / range;
  // Consider the small interval within remainder of RAND_MAX
  if (n_rand < RAND_MAX - rem) {
    return min + n_rand/sample;
  } else {
    return rand_iid(min,max);
  }
}
/*
 * Generate pattern
 */
void generate_pattern(
    char* const pattern,
    const uint64_t length) {
  // Generate random characters
  uint64_t i;
  for (i=0;i<length;++i) {
    pattern[i] = alphabet[rand_iid(0,ALPHABET_SIZE)];
  }
  pattern[length] = '\0';
}
/*
 * Generate candidate-text from pattern adding random errors
 */
void generate_candidate_text_add_mismatch(
    char* const candidate_text,
    const uint64_t candidate_length) {
  // Generate random mismatch
  int position = rand_iid(0,candidate_length);
  char character = alphabet[rand_iid(0,ALPHABET_SIZE)];
  candidate_text[position] = character;
}

void generate_candidate_text_add_deletion(
    char* const candidate_text,
    uint64_t* const candidate_length) {
  // Generate random deletion
  int position = rand_iid(0,*candidate_length);
  int i;
  const uint64_t new_candidate_length = *candidate_length - 1;
  for (i=position;i<new_candidate_length;++i) {
    candidate_text[i] = candidate_text[i+1];
  }
  *candidate_length = new_candidate_length;
}

void generate_candidate_text_add_insertion(
    char* const candidate_text,
    uint64_t* const candidate_length) {
  // Generate random insertion
  int position = rand_iid(0,*candidate_length);
  int i;
  const uint64_t new_candidate_length = *candidate_length + 1;
  for (i=new_candidate_length-1;i>position;--i) {
    candidate_text[i] = candidate_text[i-1];
  }
  *candidate_length = new_candidate_length;
  // Insert random character
  candidate_text[position] = alphabet[rand_iid(0,ALPHABET_SIZE)];
}

char* generate_candidate_text(
    char* const pattern,
    const uint64_t pattern_length,
    const float error_degree) {
  // Compute nominal number of errors
  const uint64_t num_errors = ceil(pattern_length * error_degree);
  // Allocate & init-by-copy candidate text
  char* const candidate_text = malloc(pattern_length+num_errors);
  uint64_t candidate_length = pattern_length;
  memcpy(candidate_text,pattern,pattern_length);
  // Generate random errors
  int i;
  for (i=0;i<num_errors;++i) {
    int error_type = rand_iid(0,3);
    switch (error_type) {
      case 0:
        generate_candidate_text_add_mismatch(candidate_text,candidate_length);
        break;
      case 1:
        generate_candidate_text_add_deletion(candidate_text,&candidate_length);
        break;
      default:
        generate_candidate_text_add_insertion(candidate_text,&candidate_length);
        break;
    }
  }
  // Return candidate-text
  candidate_text[candidate_length] = '\0';
  return candidate_text;
}

/*
 * Parameters
 */
typedef struct {
  int num_reads;
  char *output;
  int length;
  float error_degree;
} countour_bench_args;

countour_bench_args parameters = {
    .num_reads = 1000,
    .output = NULL,
    .length = 100,
    .error_degree = 0.04
};

/*
 * Menu & parsing cmd options
 */
void usage() {
  fprintf(stderr, "USE: ./generate-datasets [OPTIONS]...\n"
                  "      Options::\n"
                  "        --output|o        <File>\n"
                  "        --num-patterns|n  <Integer>\n"
                  "        --length|l        <Integer>\n"
                  "        --error|e         <Float>\n"
                  "        --help|h\n");
}
void parse_arguments(int argc,char** argv) {
  struct option long_options[] = {
    { "num-patterns", required_argument, 0, 'n' },
    { "output", required_argument, 0, 'o' },
    { "length", required_argument, 0, 'l' },
    { "error", required_argument, 0, 'e' },
    { "help", no_argument, 0, 'h' },
    { 0, 0, 0, 0 } };
  int c,option_index;
  if (argc <= 1) {
    usage();
    exit(0);
  }
  while (1) {
    c=getopt_long(argc,argv,"n:o:l:e:h",long_options,&option_index);
    if (c==-1) break;
    switch (c) {
      case 'n':
        parameters.num_reads = atoi(optarg);
        break;
      case 'o':
        parameters.output = optarg;
        break;
      case 'l':
        parameters.length = atoi(optarg);
        break;
      case 'e':
        parameters.error_degree = atof(optarg);
        break;
      case 'h':
        usage();
        exit(1);
      case '?': default:
        fprintf(stderr, "Option not recognized \n"); exit(1);
    }
  }
}

int main(int argc,char* argv[]) {
  // Parsing command-line options
  parse_arguments(argc,argv);
  // Parameters
  FILE *output_file;
  // Open files
  output_file = fopen(parameters.output,"w");
  // Allocate
  char* const pattern = malloc(parameters.length+1);
  const int pattern_length = parameters.length;
  // Read-align loop
  int i;
  for (i=0;i<parameters.num_reads;++i) {
    // Prepare pattern
    generate_pattern(pattern,parameters.length);
    // Print pattern
    fprintf(output_file,">%s\n",pattern);
    // Generate candidate-text
    char* const candidate_text = generate_candidate_text(
        pattern,pattern_length,parameters.error_degree);
    // Print candidate-text
    fprintf(output_file,"<%s\n",candidate_text);
    free(candidate_text);
  }
  // Close files & free
  fclose(output_file);
  free(pattern);
  return 0;
}
