import json
import requests

def main_fetch(gpid):
    def cookies(filename='cookies.txt'):
        cookies = {}
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                request_cookies = data.get("Request Cookies", {})
                for name, value in request_cookies.items():
                    cookies[name] = value
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        return cookies
    def headers(gpid): return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://118.190.20.162',
        'Connection': 'keep-alive',
        'Referer': 'http://118.190.20.162/view.page?gpid='+gpid,
    }
    def data(gpid): return { 'cmd': 'description', 'gpid': gpid }
    return requests.post('http://118.190.20.162/problem.Problem.dt', cookies=cookies(), headers=headers(gpid), data=data(gpid))


if __name__ == '__main__':
    # just compose your procedure...
    def fetch():
        res=[]
        with open('list.txt', 'r') as f:
            for gpid in json.load(f): 
                response = main_fetch(gpid)
                if response.ok: res.append(response.json())
                else: res.append(None)
        return res
    def save(res): 
        with open('res.json', 'w') as f: json.dump(res, f, indent=4)
    def convert_to_html(res):
        html_content= '<!DOCTYPE html>\n<html>\n<head>\n<title>CSP Problems</title>\n</head>\n<body>\n'
        html_content += '<ul>\n'
        for item in res: html_content += f'<li><a href="#{item["gpid"]}">{item["title"]}</a></li>\n'
        html_content += '<div>\n'
        html_content += '</ul>\n'
        for item in res: html_content += f'<hr /><div id="{item["gpid"]}"><h2>{item["title"]}</h2><p>{item["content"]}</p></div>\n'
        html_content += '</div>\n'
        html_content += '</body>\n</html>'
        with open('index.html', 'w') as f: f.write(html_content)
    res=fetch()
    save(res)
    convert_to_html(res)
    # with open('res.json', 'r') as f: convert_to_html(json.load(f))
