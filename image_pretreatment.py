import cv2
import matplotlib.pyplot as plt
from pytesseract import pytesseract
import re


# TODO ::: 1. 하나의 이미지의 텍스트를 추출하여 결과를 return 하는 것 까지 만듭니다.
def extract_text_from_horizontal_layout():
    # 이미지 읽기
    image = cv2.imread('./assets/sample007.jpg', cv2.IMREAD_COLOR)

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
        filtered_rec = [x for x in ocr_result.strip().split('\n') if x]
        result_arr = []
        if len(filtered_rec) >= 2:
            name, price = split_name_and_price(filtered_rec[0])
            result_arr.append(name)
            result_arr.append(price)
            result_arr.append(filtered_rec[1])
        print(result_arr, len(result_arr))
    # End


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


def create_data_frame(receipt_ocr_result: str):
    pass


# TODO ::: 2. OCR의 결과 데이터가 정확하지 않습니다. 결과에 대해서 전처리하는 기능 필요
def split_name_and_price(name_and_price_str: str):
    # xx,xxx 원 혹은 x,xxx 원 혹은 xxx 원 패턴을 찾습니다.
    match = re.search(r'(\d{1,3},?\d{1,3})', name_and_price_str)
    if match:
        # 매치된 '금액' 패턴의 시작 인덱스를 가져옵니다.
        idx = match.start()
        name = name_and_price_str[:idx].strip() # 시작부터 해당 인덱스 전까지가 이름
        price = name_and_price_str[idx:].strip() # 해당 인덱스부터 끝까지가 금액
        return name, price
    else:
        return name_and_price_str, ''
# TODO ::: 3. 삽입된 모든 이미지의 텍스트 정보를 추출합니다. -> DF 만들고 -> Excel로 만들어서 제공합니다. >> 여기까지 1차 작어
# TODO ::: WILL >> front 에서 table을 통해서 제공하고 데이터가 적절한지 확인할 수 있는 화면을 만든다., 프론트추가삭제기능, 결과 다시 가져와서 엑셀로 적용 끝.


if __name__ == "__main__":
    extract_text_from_horizontal_layout()
    # extract_text_from_updated_layout()
    # make_rectangle_layout()