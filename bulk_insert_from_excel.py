import openpyxl
wb = openpyxl.load_workbook('source.xlsx')
sheets_names = wb.get_sheet_names()
print(sheets_names)
sheet = wb.worksheets[0]

all_rows = sheet.rows
for row in all_rows:
    if row[0].value is not None:
        s = ''
        s += 'insert into app_product (old_id, eng_name) values ('
        s += ''
        for cell in row:
            if cell.coordinate[0] != 'A':
                s += ', '
            if cell.value is None:
                s += 'NULL'
            else:
                s += '\'{}\''.format(cell.value)
        s += ');'
        print(s)


