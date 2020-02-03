#include "dp_table.h"
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <stdbool.h>


#define MIN(a,b) (((a)<=(b))?(a):(b))
#define MAX(a,b) (((a)>=(b))?(a):(b))

/*
 * Edit distance computation using raw DP-Table
 */
void edit_dp_traceback(
    dp_table_t* const dp_table) 
{
  // Parameters
  int** const dp = dp_table->columns;
  char* const edit_ops = dp_table->edit_operations;
  int eo_sentinel = dp_table->eo_end-1;
  int h, v;
  // Compute traceback
  h = dp_table->num_columns-1;
  v = dp_table->num_rows-1;
  while (h>0 && v>0) {
    if (dp[h][v]==dp[h][v-1]+1) {
      edit_ops[eo_sentinel--] = 'D';
      --v;
    } else if (dp[h][v]==dp[h-1][v]+1) {
      edit_ops[eo_sentinel--] = 'I';
      --h;
    } else if (dp[h][v]==dp[h-1][v-1]) {
      edit_ops[eo_sentinel--] = 'M';
      --h;
      --v;
    } else {
      edit_ops[eo_sentinel--] = 'X';
      --h;
      --v;
    }
  }
  while (h>0) {edit_ops[eo_sentinel--] = 'I'; --h;}
  while (v>0) {edit_ops[eo_sentinel--] = 'D'; --v;}
  dp_table->eo_begin = eo_sentinel+1;
}

void edit_dp_compute(
    dp_table_t* const dp_table,
    const char* const pattern,
    const int pattern_length,
    const char* const text,
    const int text_length) 
{
  // Parameters
  int** dp = dp_table->columns;
  int h, v;

  // Init DP
  for (v=0;v<=pattern_length;++v) dp[0][v] = v; // No ends-free
  for (h=0;h<=text_length;++h)    dp[h][0] = h; // No ends-free

  // Compute DP
  for (h=1;h<=text_length;++h) {
    for (v=1;v<=pattern_length;++v) {
      int min = dp[h-1][v-1] + (text[h-1]!=pattern[v-1]);
      min = MIN(min,dp[h-1][v]+1); // Ins
      min = MIN(min,dp[h][v-1]+1); // Del
      dp[h][v] = min;
    }
  }
}


/*
 * Generic parameters
 */
typedef struct {
  char *input;
  char *output;
} countour_bench_args;
countour_bench_args parameters = {
  .input=NULL,
  .output=NULL,
};


/*
 * Benchmark output
 */
void align_benchmark_output(
    FILE* const output_file,
    const int reads_processed,
    char* const edit_operations,
    const int eo_begin,
    const int eo_end) {
  fprintf(output_file,"%d\t",reads_processed);
  dp_cigar_print(output_file,edit_operations,eo_begin,eo_end);
}


/*
 * Benchmark Edit
 */
void align_benchmark_edit_dp(
    char* const pattern,
    const int pattern_length,
    char* const text,
    const int text_length,
    const int reads_processed,
    FILE* const output_file) 
{
  // Parameters
  dp_table_t dp_table;

  // Allocate
  dp_table_allocate(&dp_table,pattern_length,text_length);

  // Align
  edit_dp_compute(&dp_table,pattern,pattern_length,text,text_length);

  // Compute traceback
  edit_dp_traceback(&dp_table);

  // Output & Free
  if (output_file) {
    fprintf(output_file,"%d\t",reads_processed);
    dp_cigar_print(output_file,
        dp_table.edit_operations,
        dp_table.eo_begin,dp_table.eo_end);
  }
  dp_table_free(&dp_table);
}


/*
 * Generic Menu
 */
void usage() {
  fprintf(stderr, "USE: ./align_benchmark -i input -o output \n"
                  "      Options::\n"
                  "        --input|i            <File>\n"
                  "        --output|o           <File>\n"
                  "        --help|h\n");
}

void parse_arguments(int argc,char** argv) {
  struct option long_options[] = {
    { "input", required_argument, 0, 'i' },
    { "output", required_argument, 0, 'o' },
    { "help", no_argument, 0, 'h' },
    { 0, 0, 0, 0 } };
  int c,option_index;
  while (1) {
    c=getopt_long(argc,argv,"i:o:h",long_options,&option_index);
    if (c==-1) break;
    switch (c) {
      break;
    case 'i':
      parameters.input = optarg;
      break;
    case 'o':
      parameters.output = optarg;
      break;
    case 'h':
      usage();
      exit(1);
    // Other
    case '?': default:
      fprintf(stderr, "Option not recognized \n"); exit(1);
    }
  }
}


int main(int argc,char* argv[]) 
{
  // Parsing command-line options
  parse_arguments(argc,argv);

  // Parameters
  FILE  *input_file = NULL, *output_file = NULL;
  char  *line1 = NULL, *line2 = NULL;
  int    line1_length=0,    line2_length=0;
  size_t line1_allocated=0, line2_allocated=0;

  // Open file
  input_file = fopen(parameters.input, "r");
  if (parameters.output) {
    output_file = fopen(parameters.output, "w");
  }

  // Read-align loop
  int reads_processed = 0;
  while (true) 
  {
    // Read queries
    line1_length = getline(&line1,&line1_allocated,input_file);
    line2_length = getline(&line2,&line2_allocated,input_file);
    if (line1_length==-1 || line2_length==-1) break;

    // Configure query
    char* const pattern = line1+1;
    const int pattern_length = line1_length-1;
    char* const text = line2+1;
    const int text_length = line2_length-1;

    // Align queries using DP
    align_benchmark_edit_dp(
        pattern,pattern_length,text,text_length,
        reads_processed,output_file);

    // Update progress
    ++reads_processed;
  }

  // Close & free
  fclose(input_file);
  if (output_file) fclose(output_file);
  free(line1);  free(line2);
  return 0;
}
