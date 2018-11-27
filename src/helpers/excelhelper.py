from datetime import datetime, timedelta
import itertools
import operator
import calendar

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
                # TODO: enumerate all divisions
                result.append(('{:%Y-%m-%d}'.format(d), '{:%b-%d}'.format(d), '{:%a}'.format(d), clinician))
                d += timedelta(days=1)

            return result

        cal = calendar.Calendar()

        def group_months(tup):
            date = tup[0]
            
            for i in range(1, 13):
                # search for date in month iterator
                it = cal.itermonthdates(year, i)
                month_dates = list(map(lambda x: '{:%Y-%m-%d}'.format(x), it))

                if date in month_dates:
                    return (year, i)

        weekNums = ExcelHelper.getColumn(table, 0)
        clinicians = ExcelHelper.getColumn(table, 1)

        date_maps = list(map(expand_dates, weekNums, clinicians))
        all_dates = list(itertools.chain.from_iterable(date_maps))

        # group according to month
        groupby_months = itertools.groupby(all_dates, group_months)
        month_dict = {k : list(v) for k, v in groupby_months}
        keys = sorted(month_dict.keys(), key=operator.itemgetter(0, 1))

        # write month_dict to excel, separate sheet for each month
        wb = Workbook()
        for key in keys:
            title = calendar.month_name[key[1]]
            ws = wb.create_sheet(title)
            # write header
            ws.cell(row=1, column=1, value='Date')
            ws.cell(row=1, column=2, value='Day')
            ws.cell(row=1, column=3, value='%%DIV 1%%') #TODO: enumerate all divisions

            month = month_dict[key]
            for i in range(len(month)):
                day = month[i][1:]
                print(day)
                for j in range(len(day)):
                    ws.cell(row=(i + 2), column=j + 1, value=str(day[j]))

        wb.save(filename)

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
