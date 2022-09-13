def get_cells_range(row_index, col_index, row_count, column_count):
    start_row = row_index - 1 if row_index > 0 else row_index
    end_row = row_index + 1 if row_index < (row_count - 1) else row_index
    start_column = col_index - 1 if col_index > 0 else col_index
    end_column = col_index + 1 if col_index < (column_count - 1) else col_index
    
    return {
        'start_row': start_row,
        'end_row': end_row,
        'start_column': start_column,
        'end_column': end_column,
    }
