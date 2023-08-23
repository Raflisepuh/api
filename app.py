from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/anime/<path:endpoint>', methods=['GET'])
def get_anime(endpoint):
    try:
        response = requests.get(endpoint)
        soup = BeautifulSoup(response.content, 'html.parser')
        anime = {}

        anime['title'] = soup.select_one('.jdlz').get_text().strip()
        anime['thumbnail'] = soup.select_one('.post-thumb img')['src']
        for el in soup.select('.info p'):
            key = el.select_one('b').get_text().lower().strip().replace(' ', '_')
            el.b.extract()
            value = el.get_text().split(':')[-1].strip()
            anime[key] = None if value == '' else value
        anime['sinopsis'] = soup.select_one('.lexot > p').get_text().strip()

        anime['list_download'] = []
        for el in soup.select('#dl .smokeddlrh'):
            download_link = []
            title = el.select_one('.smokettlrh').get_text().strip()

            for ele in soup.select('.smokeurlrh'):
                type_ = ele.select_one('strong').get_text().strip()
                links = []
                for elem in ele.select('a'):
                    name = elem.get_text().strip()
                    url = elem['href']
                    links.append({'name': name, 'url': url})
                download_link.append({'type': type_, 'links': links})

            for ele in soup.select('.smokeurl'):
                type_ = ele.select_one('strong').get_text().strip()
                links = []
                for elem in ele.select('a'):
                    name = elem.get_text().strip()
                    url = elem['href']
                    links.append({'name': name, 'url': url})
                download_link.append({'type': type_, 'links': links})

            anime['list_download'].append({'title': title, 'download_link': download_link})

        return jsonify({'success': True, 'data': anime}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
