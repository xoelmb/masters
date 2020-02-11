#ifndef DP_TABLE_H_
#define DP_TABLE_H_

//#include "commons.h"

#include <stdio.h>
#include <stdlib.h>

typedef struct {
  // DP Table
  int** columns;
  int num_rows;
  int num_columns;
  // Edit operations
  char* edit_operations;
  int eo_begin;
  int eo_end;
} dp_table_t;

/*
 * Setup
 */
void dp_table_allocate(
    dp_table_t* const dp_table,
    const int pattern_length,
    const int text_length);
void dp_table_free(
    dp_table_t* const dp_table);

/*
 * Display
 */
void dp_table_print(
    FILE* const stream,
    const dp_table_t* const dp_table,
    const char* const pattern,
    const char* const text);
void dp_cigar_print(
    FILE* const stream,
    const char* const edit_operations,
    const int eo_begin,
    const int eo_end);

#endif /* DP_TABLE_H_ */
