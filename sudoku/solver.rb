include Math

N = 9
C = sqrt(N).floor


current_directory = Dir::getwd()
test_validation_directory = File.join(current_directory, "data", "validation")
test_data_directory = File.join(current_directory, "data", "cases")


=begin
definition: Reads .csv. file that is delimited by comma
param {String} file_path
returns {Array<Number>}
=end
def read_csv(file_path = "")
	rows = []
	file = File.new(file_path, "r")
	# See String#encode documentation
	encoding_options = {
	  :invalid           => :replace,  # Replace invalid byte sequences
	  :undef             => :replace,  # Replace anything not defined in ASCII
	  :replace           => '',        # Use a blank for those replacements
	  :universal_newline => true       # Always break lines with \n
	}
	while (line = file.gets)
		clean_line = line.split("").select{|i| i.ord != 65279}.join.to_s
		row = clean_line.split(",").map {|s| s.strip}
		rows.push(row)
	end
	file.close

	return rows
end	


=begin
definition: Retrieve digits in a row
param {Array<Array<Number>>} grid
param {Number} row
returns {Array<Number>}
=end
def get_row_digits(grid=[[]], row=0)
	return grid[row]
end
=begin
definition: Retrieve digits in a column
param {Array<Array<Number>>} grid
param {Number} column
returns {Array<Number>}
=end
def get_column_digits(grid=[[]], column=0)
	return grid.map {|row| row[column]}
end
=begin
definition: Retrieve digits in a box
param {Array<Array<Number>>} grid
param {Number} x
param {Number} y
returns {Array<Number>}
=end
def get_box_digits(grid=[[]], x=0, y=0)
	return (0..N-1).map {|i| grid[(i / C).floor + (y * C)][(i % C) + (x * C)] }
=begin
		box_x = (i % C)
		box_y = (i / C).floor
		return grid[box_y + (y * C)][box_x + (x * C)]
	}
=end
end

=begin
definition: Ensure unique digits across row
param {Array<Array<Number>>} grid
param {Number} row
returns {Boolean}
=end
def validate_row(grid=[[]], row=0)
	digits = get_row_digits(grid, row)
	missing_digits = find_missing_digits(digits)
	return missing_digits.length == 0
end
=begin
definition: Ensure unique digits across column
param {Array<Array<Number>>} grid
param {Number} column
returns {Boolean}
=end
def validate_column(grid=[[]], column=0)
	digits = get_column_digits(grid, column)
	missing_digits = find_missing_digits(digits)
	return missing_digits.length == 0
end
=begin
definition: Ensure unique digits across box
param {Array<Array<Number>>} grid
param {Number} x
param {Number} y
returns {Boolean}
=end
def validate_box(grid=[[]], x=0, y=0)
	digits = get_box_digits(grid, x, y)
	missing_digits = find_missing_digits(digits)
	return missing_digits.length == 0
end

=begin
definition: Identify digits that are missing from a set
param {Array<Number>} digits
returns {Array<Number>}
=end
def find_missing_digits(digits=[])
	index_list = {}
	digits.each_with_index do |number, index|
		begin
			digit = number.strip.to_i
			index_list[digit] = index
		rescue
			#puts "Invalid input: " + number
		end
	end

	missing_numbers = []
	return (1..N).select {|number| (not index_list.has_key?(number)) }
end

=begin
definition: Validate sudoku grid solution
			1. Ensure unique digits across row
			2. Ensure unique digits across column
			3. Ensure unique digits across 3x3 box
param {Array<Array<Number>>} grid
returns {Boolean}
=end
def sudoku_validate(grid = [[]])
	invalid_rows = []
	invalid_columns = []
	invalid_boxes = []
	(0..N-1).each do |y|
		#puts "row/column validation", y, validate_row(grid, y), validate_column(grid, y)
		if (validate_row(grid, y) == false)
			invalid_rows.push(y + 1)
		end
		if (validate_column(grid, y) == false)
			invalid_columns.push(y + 1)
		end

		box_x = (y % C)
		box_y = (y / C).floor
		if (validate_box(grid, box_x, box_y) == false)
			invalid_boxes.push([box_x, box_y])
		end
		#puts "box validation", box_x, box_y, validate_box(grid, box_x, box_y)
	end

	is_valid = true
	if (invalid_rows.length > 0)
		#puts "Invalid rows: " + invalid_rows.to_s
		is_valid = false
	end
	if (invalid_columns.length > 0)
		#puts "Invalid columns: " + invalid_columns.to_s
		is_valid = false
	end
	if (invalid_boxes.length > 0)
		#puts "Invalid boxes: " + invalid_boxes.to_s
		is_valid = false
	end
	return is_valid
end

puts "  Testing positive cases"
positive_case_directory = File.join(test_validation_directory, "positive")
Dir.entries(positive_case_directory)
	.select {|file_name| file_name.end_with?(".csv") }
	.each {|file_name|
		file_path = File.join(positive_case_directory, file_name)
		rows = read_csv(file_path)

		case_name = file_name.split(".")[0]
		validation = sudoku_validate(rows)
		puts "Expect test-case, " + case_name + ", to be true. Validation found it to be " + validation.to_s
	}

puts "  Testing negative cases"
negative_case_directory = File.join(test_validation_directory, "negative")
Dir.entries(negative_case_directory)
	.select {|file_name| file_name.end_with?(".csv") }
	.each {|file_name|
		file_path = File.join(negative_case_directory, file_name)
		rows = read_csv(file_path)

		case_name = file_name.split(".")[0]
		validation = sudoku_validate(rows)
		puts "Expect test-case, " + case_name + ", to be false. Validation found it to be " + validation.to_s
	}
