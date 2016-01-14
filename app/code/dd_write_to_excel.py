import xlsxwriter
MAXROW =  1048575
MAXCOLUMN = 16383

def write_with_xlsxwriter(file_and_path, results_list):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(file_and_path)
    worksheet = workbook.add_worksheet()

    # format_normal = workbook.add_format({'size': 10})
    format_large = workbook.add_format({'size': 30})
    # format_large.set_font_size(30)

    format_bold = workbook.add_format({'bold': True})
    format_not_bold = workbook.add_format({'bold': False})
    width_of_one_char = 1.1

    add_red_green_conditional_formatting(workbook, worksheet)

    bold_row_boolean = False
    bold_column_boolean = False
    max_column_string_lengths = []
    for row_number in range(0, len(results_list)):
        results_line = results_list[row_number]
        for column_number in range(0, len(results_line)):

            cell_string = results_line[column_number]

            my_string_length = len(cell_string)

            if (len(max_column_string_lengths) <= column_number):
                max_column_string_lengths.append(0)
            else:
                max_column_string_lengths[column_number] = max(max_column_string_lengths[column_number], my_string_length)

            if column_number == 0:
                bold_column_boolean = True
                if cell_string == "":
                    bold_row_boolean = True
                else:
                    bold_row_boolean = False
            else:
                bold_column_boolean = False

            if row_number == 0 & column_number == 0:
                my_format = format_large
            else:
                if bold_column_boolean | bold_row_boolean:
                    my_format = format_bold
                else:
                    my_format = format_not_bold

            worksheet.write(row_number, column_number, cell_string, my_format)

    for i in range(0, len(max_column_string_lengths)):
        worksheet.set_column(i,i, max_column_string_lengths[i]* width_of_one_char)

    # Widen the first column to make the text clearer.
   #  worksheet.set_column('A:A', 20)

    workbook.close()

def add_red_green_conditional_formatting(my_workbook, my_worksheet):
    # my_workbook = my_worksheet.get
    format_red_bold = my_workbook.add_format({'bold': True, 'font_color': 'red'})
    format_green = my_workbook.add_format({'font_color': 'green'})
    my_worksheet.conditional_format(0,0,MAXROW,MAXCOLUMN, {'type': 'text',
                                            'criteria': 'begins with',
                                            'value': 'Match',
                                            'format': format_green})

    my_worksheet.conditional_format(0,0,MAXROW,MAXCOLUMN, {'type': 'text',
                                        'criteria': 'begins with',
                                        'value': 'Mismatch',
                                        'format': format_red_bold})

    '''worksheet.conditional_format('AA:ZZ', {'type': 'cell',
                                             'criteria': '==',
                                             'value': '123',
                                             'format': format_red})'''

'''
    # Text with formatting.
   #  worksheet.write('A2', 'World', format_bold)

    # Insert an image.
    #worksheet.insert_image('B5', 'logo.png')
    '''