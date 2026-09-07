import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    book_list = soup.find_all("a", title=True)

    # 不再print输出，直接写文件
    with open("books.txt", "w", encoding="utf-8") as f:
        for book in book_list:
            title = book["title"]
            f.write(title + "\n")

    print("✅数据已全部保存到 books.txt")

except Exception as e:
    print("出错：", e)
