from openpyxl import Workbook


class ExcelHelper:
    @staticmethod
    def saveToFile(filename, table):
        wb = Workbook()
        sheet = wb.active

        cols = table.columnCount()
        rows = table.rowCount()

        # write header
        for i in range(cols):
            header = table.horizontalHeaderItem(i)
            sheet.cell(row=1, column=i + 1, value=header.text())

        # write data
        sheetRow = 2
        for i in range(rows):
            for j in range(cols):
                item = table.item(i, j)
                sheet.cell(row=sheetRow, column=j+1, value=item.text())
            sheetRow += 1

        wb.save(filename)
