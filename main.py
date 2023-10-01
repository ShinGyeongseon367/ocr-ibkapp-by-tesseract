import app.component.pandas_component as pd_component
from app.component.create_excel_component import CreateExcel

if __name__ == "__main__":
    month = 9
    reporter_name = "신경선"
    file_name = "./assets/demo_sample.txt"

    processed = pd_component.read_text_file(file_name)
    removed_after_day = pd_component.remove_data_after_day(processed)
    removed_enter = pd_component.remove_enter(removed_after_day)
    data_frame = pd_component.extract_data(removed_enter)
    result_df = pd_component.filter_by_month(month=month, df=data_frame)

    create_excel = CreateExcel()
    create_excel.service(insert_df=result_df, month=month, reporter_name=reporter_name)
