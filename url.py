import os
import requests
from bs4 import BeautifulSoup

url = "https://twitter.com/"  # 取得するURL
save_dir = "web_files"  # ファイルを保存するディレクトリのパス

# URLからHTML、CSS、JavaScriptファイルを取得する関数
def get_html_css_js_files(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    html = str(soup)
    css = ""
    js = ""

    # <link>タグからCSSファイルのURLを取得し、CSSを取得する
    for link in soup.find_all("link"):
        if link.get("rel") == ["stylesheet"]:
            css_url = link.get("href")
            if css_url.startswith("//"):
                css_url = "https:" + css_url
            elif css_url.startswith("/"):
                css_url = url + css_url
            else:
                css_url = url + "/" + css_url
            css_res = requests.get(css_url)
            css += css_res.text

    # <script>タグからJavaScriptファイルのURLを取得し、JavaScriptを取得する
    for script in soup.find_all("script"):
        if script.get("src"):
            js_url = script.get("src")
            if js_url.startswith("//"):
                js_url = "https:" + js_url
            elif js_url.startswith("/"):
                js_url = url + js_url
            else:
                js_url = url + "/" + js_url
            js_res = requests.get(js_url)
            js += js_res.text

    return html, css, js

# HTML、CSS、JavaScriptをそれぞれファイルに書き込む
def write_files(html, css, js):
    os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成する
    with open(os.path.join(save_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    with open(os.path.join(save_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

    with open(os.path.join(save_dir, "script.js"), "w", encoding="utf-8") as f:
        f.write(js)

# メイン処理
if __name__ == "__main__":
    html, css, js = get_html_css_js_files(url)
    write_files(html, css, js)
