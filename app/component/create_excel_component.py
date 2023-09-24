import calendar
import datetime

import openpyxl
import pandas
from openpyxl import Workbook


class CreateExcel:
    def __init__(self):
        self.workbook: Workbook = None

    def get_excel_schema(self, path='./assets/', excel_name='corporation_card_schema.xlsx'):
        # 기존 엑셀 파일 열기
        excel_full_name = path + excel_name
        self.workbook = openpyxl.load_workbook(excel_full_name)

    def insert_date_to_excel(self, insert_data_frame: pandas.DataFrame):
        # 워크시트 선택
        sheet = self.workbook.active

        # 새로운 데이터 추가
        for row_index, row in enumerate(insert_data_frame.values, start=5):
            for col_index, value in enumerate(row, start=3):
                cell = sheet.cell(row=row_index, column=col_index)
                cell.value = value

    # 제목, 년 월 등 초기화
    def initialize_header(self, month: int, reporter_name: str):
        main_title = f'{month}월 법인카드 사용내역서'
        repoter = f'이름 {reporter_name}'

        now_year = datetime.datetime.now().year
        if month == 1:
            now_year -= 1

        last_day_every_month = calendar.monthrange(now_year, month)[1]
        period = f'기     간   :    {now_year} / {month} / 1  ~  {now_year} / {month} / {last_day_every_month}'

        sheet = self.workbook.active
        sheet['B2'] = main_title  # main title cell
        sheet['B3'] = repoter  # reporter_name cell
        sheet['E3'] = period  # period cell

    def export_result_excel(self, export_excel_name: str) -> None:
        self.workbook.save('./return_assets/' + export_excel_name + '.xlsx')

    def service(self, insert_df: pandas.DataFrame, month: int, reporter_name: str):
        self.get_excel_schema()
        self.initialize_header(month, reporter_name)
        self.insert_date_to_excel(insert_df)
        self.export_result_excel(export_excel_name='demo_header_excel')
