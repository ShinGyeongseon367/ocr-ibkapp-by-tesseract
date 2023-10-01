import pandas as pd
import re


def read_text_file(filename: str) -> str:

    # 파일 읽기
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()

    # 읽어온 데이터 확인 (옵션)
    return data


def filter_by_month(month: int, df: pd.DataFrame) -> pd.DataFrame:
    # df = df.sort_values("date")
    month_str = f"{month:02}"
    return df[df['date'].str.startswith(month_str)]


def remove_data_after_day(text: str) -> str:
    # 일반적인 '(요일)' 패턴을 찾아 이후의 문자들을 제거
    processed_lines = []
    for line in text.split('\n'):
        result = re.split(r'(\d{2}일\(\w\))', line)
        if len(result) >= 2:
            # '(요일)' 이후의 문자들을 제거하고 다시 결합
            processed_lines.append(result[0] + result[1])
        else:
            processed_lines.append(line)
    return '\n'.join(processed_lines)


def remove_enter(text: str) -> str:
    # 개행 제거
    text_without_newline = text.replace('\n', '')

    # 날짜 패턴 기준으로 문자열 분할
    date_pattern = r'(\d{2}월 \d{2}일\(\w\))'
    split_text = re.split(date_pattern, text_without_newline)

    # 패턴에 따라 문자열 재조합
    reformatted = []
    for i in range(1, len(split_text), 2):
        reformatted.append(split_text[i - 1] + '>' + split_text[i])

    return '\n'.join(reformatted)


def extract_data(text: str) -> pd.DataFrame:
    # 각 줄을 분할하고 각 줄에서 '>>' 기준으로 데이터를 분리
    lines = text.strip().split('\n')

    store_names, prices, payment_dates = [], [], []

    for line in lines:
        left, payment_date = line.split('>>')
        # 금액 패턴을 찾음
        price_match = re.search(r'(\d{1,3}(?:,\d{3}))', left)
        if price_match:
            price = price_match.group(1)
            store_name = left[:price_match.start()].strip()
        else:
            price = None
            store_name = left.strip()

        store_names.append(store_name)
        prices.append(price)
        payment_dates.append(payment_date)

    # 데이터 프레임 생성
    df = pd.DataFrame({
        'date': payment_dates,
        'store': store_names,
        'price': prices
    })

    df['price'] = df['price'].str.replace(',', '').astype(int)

    df['apply_name'] = '점심'
    df['subject'] = '복리후생비'
    return df


if __name__ == "__main__":
    processed = read_text_file("../../assets/demo_sample.txt")
    removed_after_day = remove_data_after_day(processed)
    removed_enter = remove_enter(removed_after_day)
    data_frame = extract_data(removed_enter)
    data_frame = filter_by_month(month=9, df=data_frame)
    print(data_frame)
