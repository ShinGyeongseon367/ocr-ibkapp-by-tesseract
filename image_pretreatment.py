from typing import List
from datetime import datetime
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from pytesseract import pytesseract
import re


COLUMN_APPROVAL_DATE = '승인일자'
COLUMN_MERCHANT_NAME = '가맹점명'
COLUMN_AMOUNT = '금액'


def extract_text_from_horizontal_layout(path: str, *file_names: str) -> pd.DataFrame:
    result_arr = []

    for file_name in file_names:
        file_full_name = path + file_name
        # 이미지 읽기
        image = cv2.imread(file_full_name, cv2.IMREAD_COLOR)

        # 이미지의 높이와 너비 가져오기
        height, width, _ = image.shape

        # 각 영역의 높이 계산
        section_height = height // 10

        # 10개의 영역에 대해 사각형 그리기
        for i in range(10):
            start_y = section_height * i
            end_y = section_height * (i + 1)

            # 해당 영역 추출 (ROI 설정)
            roi = image[start_y:end_y, 0:width]

            # ROI에 대한 OCR 수행
            ocr_result = pytesseract.image_to_string(roi, lang='eng+kor')

            # 결과 출력
            filtered_rec:List[str] = [x for x in ocr_result.strip().split('\n') if x]
            if len(filtered_rec) >= 2:
                name, price = split_name_and_price(filtered_rec[0])
                date = filtered_rec[1][:filtered_rec[1].find('(')].replace(' ', '')
                result_arr.append([date, name, price])

    return create_data_frame(result_arr)


def make_rectangle_layout():
    image = cv2.imread('./assets/sample001.jpg', cv2.IMREAD_COLOR)

    # 이미지의 높이와 너비 가져오기
    height, width, _ = image.shape

    # 각 영역의 높이 계산
    section_height = height // 10

    # 10개의 영역에 대해 사각형 그리기
    for i in range(10):
        start_y = section_height * i
        end_y = section_height * (i + 1)

        # 사각형 그리기 (이미지, 시작 좌표, 종료 좌표, 색상, 두께)
        cv2.rectangle(image, (0, start_y), (width, end_y), (0, 255, 0), 2)

        # 섹션 내에서 레이아웃 나누기
        cv2.rectangle(image, (0, start_y), (int(width * 0.6), int(start_y + section_height * 0.6)), (255, 0, 0),
                      2)  # 첫 번째 사각형 (파란색)
        cv2.rectangle(image, (0, int(start_y + section_height * 0.55)), (int(width * 0.6), end_y), (255, 0, 0),
                      2)  # 두 번째 사각형 (파란색)
        cv2.rectangle(image, (int(width * 0.6), start_y), (width, end_y), (255, 0, 0), 2)  # 세 번째 사각형 (파란색)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


def create_data_frame(receipt_ocr_result_arr: List[str]):
    return pd.DataFrame(receipt_ocr_result_arr,
                        columns= [COLUMN_APPROVAL_DATE, COLUMN_MERCHANT_NAME, COLUMN_AMOUNT])


def convert_to_date(ocr_date:str):
    current_year = datetime.now().year
    month = ocr_date[:2]
    day = ocr_date[3:5]
    return datetime.strptime(f"{current_year}-{month}-{day}", "%Y-%m-%d")


def convert_won(ocr_won: str):
    match = re.search(r'(\d{1,3},?\d{1,3})', ocr_won)
    if match:
        won_str = match.group(0)
        if isinstance(won_str, str) and ',' in won_str:
            return int(won_str.replace(',', ''))

        return match.group(0)

    return ocr_won


def split_name_and_price(name_and_price_str: str):
    # xx,xxx 원 혹은 x,xxx 원 혹은 xxx 원 패턴을 찾습니다
    match = re.search(r'(\d{1,3},?\d{1,3})', name_and_price_str)
    if match:
        # 매치된 '금액' 패턴의 시작 인덱스를 가져옵니다
        idx = match.start()
        name = name_and_price_str[:idx].strip()  # 시작부터 해당 인덱스 전까지가 이름
        price = name_and_price_str[idx:].strip()  # 해당 인덱스부터 끝까지가 금액
        return name, price
    else:
        return name_and_price_str, ''


def main_service(input_month: int):
    # WILLDO::: parameter validation: not_null, 1~12
    # WILLDO::: 파일경로와 , 파일이름은 나중에 stream byte로 받을 수 있게 만들어야합니다.
    result_ocr_arr = extract_text_from_horizontal_layout('./assets/', 'sample008.jpeg', 'sample002.jpeg')
    df = create_data_frame(result_ocr_arr)
    df[COLUMN_APPROVAL_DATE] = df[COLUMN_APPROVAL_DATE].apply(convert_to_date)
    df[COLUMN_AMOUNT] = df[COLUMN_AMOUNT].apply(convert_won)
    return_data = df[pd.DatetimeIndex(df[COLUMN_APPROVAL_DATE]).month == input_month]
    return return_data