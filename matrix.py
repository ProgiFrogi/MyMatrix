class Tensor:
    def __init__(self, dimension: int | tuple, data: list):
        self.dimension = dimension
        self.data = data

    def __repr__(self):
        print(self.data)

class Matrix(Tensor):
    def __init__(self, dimension: tuple, data: list):
        if not isinstance(dimension, tuple):
            raise ValueError('Invalid dimension! Dimension should be tuple with len of 2')
        if len(dimension) != 2:
            raise ValueError('Invalid dimension! Dimension should be tuple with len of 2')
        self.row, self.column = dimension
        if self.row * self.column != len(data):
            raise ValueError('Len data should be equal to size of matrix(Prod of dimensions)')
        super().__init__(dimension, data)

    def conv_rc2i(self, row, column) -> int:
        return row * self.column + column
    def conv_i2rc(self, i) -> tuple:
        return (i // self.column, i % self.column)

    def __str__(self):
        s = '[\n'
        max_num = max(self.data)
        max_num_len = len(str(max_num)) + 2

        for i in range(self.row):
            s += "".join(f"{num:>{max_num_len}}" for num in self.data[i*self.column:(i+1)*self.column])
            s += "\n\n"
        s = s[:-1] + ']'
        return s

    def get_row_by_index(self, row) -> list:
        return [self.data[self.conv_rc2i(row, x)] for x in range(self.column)]
    def get_rows_by_indexes(self, rows : list) -> list:
        return [item for row in [self.get_row_by_index(x) for x in rows] for item in row]
    def get_rows_by_slice(self, item: slice) -> list:
        rows = list(range(*item.indices(self.row)))
        return self.get_rows_by_indexes(rows)

    def get_column_in_row(self, item : int | slice | list, rows : list) -> list:
        if isinstance(item, int):
            item = [item]
        elif isinstance(item, slice):
            item = list(range(*item.indices(self.row)))
        elif not isinstance(item, list):
            raise ValueError("Invalid key")
        return [rows[x * self.column + y] for x in range(len(rows) // self.column) for y in item ]

    def __getitem__(self, item):
        if isinstance(item, int):
            if self.row == 1:
                return self.data[item]
            return Matrix((1, self.column), self.get_row_by_index(item))
        elif isinstance(item, list):
            return Matrix((len(item), self.column), self.get_rows_by_indexes(item))
        elif isinstance(item, slice):
            rows = self.get_rows_by_slice(item)
            return Matrix((len(rows) // self.column, self.column), rows)
        elif isinstance(item, tuple):
            get_rows = item[0]
            get_columns = item[1]
            if isinstance(get_rows, int) and isinstance(get_columns, int):
                if self.row <= get_rows or self.column <= get_columns:
                    raise ValueError('Invalid index: index out of range')
                return self.data[self.conv_rc2i(get_rows, get_columns)]
            elif isinstance(get_rows, (slice, int, list)) and isinstance(get_columns, (slice, int, list)):
                rows = self.get_rows_by_slice(get_rows) if isinstance(get_rows, slice) else self.get_rows_by_indexes(get_rows) if isinstance(get_rows, list) else self.get_row_by_index(get_rows)
                columns = self.get_column_in_row(get_columns, rows)
                len_rows = len(rows) // self.column
                return Matrix((len_rows, len(columns)//len_rows), columns)
        else:
            raise ValueError('Invalid type')

if __name__ == '__main__':

    matrix = Matrix((4,3),
                    [0, 1, 2,
                            3, 4, 5,
                     6, 7, 8,
                     9, 10, 11])
    print(matrix[slice(0, 4, 2)])
    # print(*[x for x in range(1, a)])
