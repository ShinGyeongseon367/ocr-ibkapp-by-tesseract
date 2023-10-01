# ocr-ibkapp-by-tesseract
Corporate card IBK application receipt list image text conversion

🛑 Stop This Project ! 

Reason: Stopping Tesseract because it is not accurate with the IBK APP font.

Afterwards, we plan to test again using NAVER CLOVA.

---
# Impossible to work using NAVER CLOVA OCR
**To use NAVER CLOVA OCR, an image storage (Public Server) is required.**

**🚨 Image preprocessing must be performed using NAVER CLOVA OCR.**

---
How to use
1. Crop the image
Please cut it based on the top and bottom and express only the list.
![ASIS](../../Downloads/풀샷.jpeg)
![TOBE](../../Downloads/작은샷.jpeg)
2. OCR (NAVER CLOVA)
[NAVER CLOVA OCR](https://clova.ai/ocr/?lang=ko)
Access and run OCR with the demo version.
![](../../Desktop/스크린샷 2023-10-01 오후 11.13.42.png)
3. Copy paste
Copy and paste them into the text file(assets/demo_sample.txt) in the code.

4. RUN main