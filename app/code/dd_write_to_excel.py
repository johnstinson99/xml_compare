import xlsxwriter
MAX_ROW = 1048575
MAX_COLUMN = 16383

def write_with_xlsxwriter(file_and_path, results_list, title_string, subtitle_string):

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(file_and_path)
    worksheet = workbook.add_worksheet()

    format_title = workbook.add_format({'size': 30})
    format_subtitle = workbook.add_format({'size': 20})
    format_bold = workbook.add_format({'bold': True})
    format_not_bold = workbook.add_format({'bold': False})
    width_of_one_char = 1.1
    row_offset = 3

    add_red_green_conditional_formatting(workbook, worksheet)

    bold_row_boolean = False
    max_column_string_lengths = []

    for row_number in range(0, len(results_list)):
        results_line = results_list[row_number]
        for column_number in range(0, len(results_line)):
            cell_string = results_line[column_number]
            my_string_length = len(cell_string)

            if len(max_column_string_lengths) <= column_number:
                max_column_string_lengths.append(0)
            else:
                max_column_string_lengths[column_number] = \
                    max(max_column_string_lengths[column_number], my_string_length)

            if column_number == 0:
                bold_column_boolean = True
                if cell_string == "":
                    bold_row_boolean = True
                else:
                    bold_row_boolean = False
            else:
                bold_column_boolean = False

            if bold_column_boolean | bold_row_boolean:
                my_format = format_bold
            else:
                my_format = format_not_bold

            worksheet.write(row_number + row_offset, column_number, cell_string, my_format)

    # Set column widths
    for i in range(0, len(max_column_string_lengths)):
        worksheet.set_column(i, i, max_column_string_lengths[i] * width_of_one_char)

    # Add titles
    worksheet.write(0, 0, title_string, format_title)
    worksheet.write(1, 0, subtitle_string, format_subtitle)

    workbook.close()


def add_red_green_conditional_formatting(my_workbook, my_worksheet):
    # my_workbook = my_worksheet.get
    format_red_bold = my_workbook.add_format({'bold': True, 'font_color': 'red'})
    format_green = my_workbook.add_format({'font_color': 'green'})
    my_worksheet.conditional_format(0, 0, MAX_ROW, MAX_COLUMN, {'type': 'text',
                                                                'criteria': 'begins with',
                                                                'value': 'Match',
                                                                'format': format_green})

    my_worksheet.conditional_format(0, 0, MAX_ROW, MAX_COLUMN, {'type': 'text',
                                                                'criteria': 'begins with',
                                                                'value': 'Mismatch',
                                                                'format': format_red_bold})
