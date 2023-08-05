from PIL import Image, ImageDraw, ImageFont # 사진 편집기 불러오기
import textwrap # 자동 텍스트 웹핑 라이브러리
import smtplib, os
from email import encoders # 이메일 보내기 라이브러리
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


class MySelf:
    def __init__(self, name, year, gender, *hobby):
        if 15 >= len(name):
            self.name = name
        else:
            raise Exception("Out of Name len (15 letters)")
        if 10 >= len(year):
            self.year = str(year)
        else:
            raise Exception("Out of year len (10 letters)")
        if 6 >= len(gender):
            self.gender = gender
        else:
            raise Exception("Out of gender len (6 letters)")
        self.hobby = hobby
        self.hobby = ', '.join(self.hobby)

    def introduction(self, text):
        return_text = ""
        data = textwrap.wrap(text=text, width=round((200 / 2) / 10))
        n = 0
        for i in range(0, len(data)):
            n += 1
            data.insert(n, "\n")
            n += 1

        for get_text in data:
            return_text += get_text

        self.introduction = return_text
        return {"error": False, "code": "Success","message": "성공적으로 자기소개를 설정했습니다."}
        # return "성공적으로 자기소개서를 설정했습니다.\n"


    def check(self):
        return_text = f"이름: {self.name}\n나이: {self.year}\n성별: {self.gender}\n취미: {self.hobby}\n \n{self.introduction}"
        return return_text

    def create_image(self, width, height, font, font_size=15, font_color=(255, 255, 255), background_color=(0, 0, 0), title="자기소개서"):
        img = Image.new("RGB", (width, height), color=background_color)
        fnt = ImageFont.truetype(font, font_size, encoding="UTF-8")

        textPosition01 = 10
        textPosition02 = 10

        draw = ImageDraw.Draw(img)
        draw.text((textPosition01, textPosition02), f"이름: {self.name}\n나이: {self.year}\n성별: {self.gender}\n취미: {self.hobby}\n \n{self.introduction}", font=fnt, fill=font_color)

        img.save(f"{title}.png")
        return {"error": False, "code": "Success", "message": "성공적으로 사진을 생성했습니다."}


class Email:
    def __init__(self, from_address, password, to_address): # 이메일과 비밀번호 받기
        self.from_address = from_address
        self.password = password
        self.to_address = to_address

    def send(self, title="자기소개서", send_text, image="자기소개서.png"):
        # 이메일 제목
        msg = MIMEMultipart()
        msg['Subject'] = title

        # 이메일 내용
        text = MIMEText(str(send_text))

        # 이메일 제목과 내용 합치기
        msg.attach(text)

        # <----- 보내기 ------>
        s = smtplib.SMTP('smtp.gmail.com', 587) # 587: google smpt 서버의 포트 번호
        s.starttls() # 서버 접속
        s.login(self.from_address, self.password) # 로그인

        # 파일 첨부
        files = r"" + image
        files = files.encode("utf-8")

        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(files, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=image)
        msg.attach(part)

        msg['To'] = self.to_address
        s.sendmail(self.from_address, self.to_address, msg.as_string())
        s.quit()
        return {"error": False, "code": "Success", "message": "성공적으로 이메일을 보냈습니다."}