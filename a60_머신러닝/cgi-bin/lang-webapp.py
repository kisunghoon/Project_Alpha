import cgi, cgitb, os.path  
import html
import joblib

cgitb.enable()   
clf = joblib.load(r'D:\DevRoot\DataSet\lang\lang\freq.pkl') 

def show_form(text, msg=""):
    print("Content-Type: text/html; charset=euc-kr")
    print("")
    print("""
        <html>
            <body>
                <form>
                    <textarea name="text" rows="8" cols="40">{0}</textarea>
                    <p><input type="submit" value="판정"></p>
                    <p>{1}</p>
                </form>
            </body>
        </html>
    """.format(html.escape(text), msg))
    
def detect_lang(text):
    # 알파벳 출현 빈도 구하기
    text = text.lower()

    # 알파벳인 경우 해당 알파벳의 빈도수 ++
    cnt = []
    for i in range(26):
        ch = chr(i + ord('a'))
        cnt.append(text.count(ch))
    
    total = sum(cnt)
    if total == 0: return "입력이 없습니다"
    
    freq = list(map(lambda n: n / total, cnt))
    
    # 언어 예측하기
    res = clf.predict([freq])
    
    # 언어 코드를 한국어로 변환하기
    lang_dic = {
        "en": "영어",
        "fr": "프랑스어",
        "id": "인도네시아어",
        "tl": "타갈로그어"
    }
    return lang_dic[res[0]]     # 응? 왜 res[0] 이지?    




def main():
    form = cgi.FieldStorage()  # request parameter 등을 갖고 있는 form 객체 받아오기
    text = form.getvalue("text", default="")  # name="text"
    msg = ""
    if text != "":
        lang = detect_lang(text)  # 언어 판독 (AI가동)
        msg = "판정 결과:" + lang

    show_form(text, msg)

if __name__ == "__main__":
	main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    