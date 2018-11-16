from datetime import datetime, timedelta
import itertools

from openpyxl import Workbook

from constants import WEEK_HOURS


class ExcelHelper:
    @staticmethod
    def saveYearlySchedule(filename, table):
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

    @staticmethod
    def saveMonthlySchedule(filename, table, year):
        # for each weeknum, loop over days in that week, assuming we start
        # at monday and end on friday

        def expand_dates(weekText, clinician):
            result = []
            weekNum = int(
                weekText[:-1]) if weekText[-1] == '*' else int(weekText)

            d = weekStart = datetime.strptime(
                # year / weekNum / Monday / 8AM
                '{0}/{1:02d}/1/08:00'.format(year, weekNum),
                '%G/%V/%u/%H:%M'
            )
            weekEnd = weekStart + timedelta(hours=WEEK_HOURS)

            while d <= weekEnd:
                result.append((d, clinician))
                # print(d.strftime('%b-%d\t%a\t{}'.format(clinician)))
                d += timedelta(days=1)

            return result

        def group_months(tup):
            date = tup[0]
            return date.strftime('%b-%Y')

        weekNums = ExcelHelper.getColumn(table, 0)
        clinicians = ExcelHelper.getColumn(table, 1)

        date_maps = list(map(expand_dates, weekNums, clinicians))
        dates = list(itertools.chain.from_iterable(date_maps))

        # group according to month
        groupby_months = itertools.groupby(dates, group_months)
        month_dict = {k : list(v) for k, v in groupby_months}

    @staticmethod
    def getColumn(table, col_idx):
        rows = table.rowCount()
        column = []
        for i in range(rows):
            column.append(table.item(i, col_idx).text())

        return column

    @staticmethod
    def getRow(table, row_idx):
        cols = table.rowCount()
        row = []
        for i in range(cols):
            row.append(table.item(row_idx, i).text())

        return row
