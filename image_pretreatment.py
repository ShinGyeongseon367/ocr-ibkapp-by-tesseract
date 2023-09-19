import cv2
import matplotlib.pyplot as plt
from pytesseract import pytesseract
import re


def extract_text_from_horizontal_layout():
    # 이미지 읽기
    image = cv2.imread('./assets/sample001.jpg', cv2.IMREAD_COLOR)

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
        text = pytesseract.image_to_string(roi, lang='eng+kor')

        # 결과 출력
        print(f"Section {i + 1}:")
        print(text)
        print("----------------------")
    # End


def extract_text_from_updated_layout():
    # 이미지 읽기
    image = cv2.imread('./assets/sample001.jpg', cv2.IMREAD_COLOR)

    # 이미지의 높이와 너비 가져오기
    height, width, _ = image.shape

    # 각 영역의 높이 계산
    section_height = height // 10

    # 10개의 영역에 대해 사각형 그리기
    for i in range(10):
        start_y = section_height * i
        end_y = section_height * (i + 1)

        # 섹션 내에서 레이아웃 정의하기
        layouts = [
            (0, start_y, int(width * 0.6), int(start_y + section_height * 0.6)),  # 첫 번째 레이아웃
            (0, int(start_y + section_height * 0.6), int(width * 0.6), end_y),  # 두 번째 레이아웃
            (int(width * 0.6), start_y, width, end_y)  # 세 번째 레이아웃
        ] # 3등분

        layouts2 = [
            (0, start_y, int(width * 0.6), end_y),  # 첫 번째 레이아웃
            (int(width * 0.6), start_y, width, end_y)  # 두 번째 레이아웃
        ] # 레이아웃 좌우로 구별

        print(f"---- Section {i + 1} ----")
        # 각 레이아웃에 대한 텍스트 추출하기
        for idx, (x1, y1, x2, y2) in enumerate(layouts):
            roi = image[y1:y2, x1:x2]
            text = pytesseract.image_to_string(roi, lang='eng+kor')
            print(text)
            print("------------------------")
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
        cv2.rectangle(image, (0, start_y), (int(width * 0.6), int(start_y + section_height * 0.55)), (255, 0, 0),
                      2)  # 첫 번째 사각형 (파란색)
        cv2.rectangle(image, (0, int(start_y + section_height * 0.55)), (int(width * 0.6), end_y), (255, 0, 0),
                      2)  # 두 번째 사각형 (파란색)
        cv2.rectangle(image, (int(width * 0.6), start_y), (width, end_y), (255, 0, 0), 2)  # 세 번째 사각형 (파란색)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


if __name__ == "__main__":
    extract_text_from_horizontal_layout()
    extract_text_from_updated_layout()
    # make_rectangle_layout()