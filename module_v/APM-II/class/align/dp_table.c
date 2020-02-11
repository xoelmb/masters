#include "dp_table.h"

/*
 * Common numerical data processing/formating
 */
#define MIN(a,b) (((a)<=(b))?(a):(b))
#define MAX(a,b) (((a)>=(b))?(a):(b))
#define ABS(a) (((a)>=0)?(a):-(a))

/*
 * DP-Table Setup
 */
void dp_table_allocate(
    dp_table_t* const dp_table,
    const int pattern_length,
    const int text_length) {
  // Allocate DP table
  int h;
  dp_table->num_rows = pattern_length+1;
  const int num_columns = text_length+1;
  dp_table->num_columns = num_columns;
  dp_table->columns = malloc((text_length+1)*sizeof(int*)); // Columns
  for (h=0;h<num_columns;++h) {
    dp_table->columns[h] = malloc((pattern_length+1)*sizeof(int)); // Rows
  }
  // Edit operations
  const int max_ops = pattern_length+text_length;
  dp_table->edit_operations = malloc(max_ops);
  dp_table->eo_begin = max_ops;
  dp_table->eo_end = max_ops;
}


void dp_table_free(
    dp_table_t* const dp_table) {
  const int num_columns = dp_table->num_columns;
  int h;
  for (h=0;h<num_columns;++h) {
    free(dp_table->columns[h]);
  }
  free(dp_table->columns);
  free(dp_table->edit_operations);
}



/*
 * Display
 */
void dp_table_print(
    FILE* const stream,
    const dp_table_t* const dp_table,
    const char* const pattern,
    const char* const text) {
  // Parameters
  int** const dp = dp_table->columns;
  int i, j;
  // Print Header
  fprintf(stream,"       ");
  for (i=0;i<dp_table->num_columns-1;++i) {
    fprintf(stream,"  %c  ",text[i]);
  }
  fprintf(stream,"\n ");
  for (i=0;i<dp_table->num_columns;++i) {
    if (dp[i][0]!=-1) {
      fprintf(stream," %3d ",dp[i][0]);
    } else {
      fprintf(stream,"   * ");
    }
  }
  fprintf(stream,"\n");
  // Print Rows
  for (i=1;i<dp_table->num_rows;++i) {
    fprintf(stream,"%c",pattern[i-1]);
    for (j=0;j<dp_table->num_columns;++j) {
      if (dp[j][i]!=-1) {
        fprintf(stream," %3d ",dp[j][i]);
      } else {
        fprintf(stream,"   * ");
      }
    }
    fprintf(stream,"\n");
  }
  fprintf(stream,"\n");
}


void dp_cigar_print(
    FILE* const stream,
    const char* const edit_operations,
    const int eo_begin,
    const int eo_end) {
  int h;
  char last_op = edit_operations[eo_begin];
  int last_op_length = 1;
  fprintf(stream,"CIGAR=");
  for (h=eo_begin+1;h<eo_end;++h) {
    if (edit_operations[h]==last_op) {
      ++last_op_length;
    } else {
      fprintf(stream,"%d%c",last_op_length,last_op);
      last_op = edit_operations[h];
      last_op_length = 1;
    }
  }
  fprintf(stream,"%d%c\n",last_op_length,last_op);
}

