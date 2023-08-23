from fastapi import FastAPI
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

@app.get("/anime/{endpoint:path}")
async def get_anime(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        anime = {}

        anime['title'] = soup.select_one('.jdlz').get_text().strip()
        anime['thumbnail'] = soup.select_one('.post-thumb img')['src']

        info_elements = soup.select('.info p')
        for el in info_elements:
            key = el.select_one('b').get_text().lower().strip().replace(' ', '_')
            el.b.extract()
            value = el.get_text().split(':')[-1].strip()
            anime[key] = None if value == '' else value

        anime['sinopsis'] = soup.select_one('.lexot > p').get_text().strip()

        anime['list_download'] = []
        download_elements = soup.select('#dl .smokeddlrh')
        for el in download_elements:
            download_link = []
            title = el.select_one('.smokettlrh').get_text().strip()

            for ele in el.select('.smokeurlrh, .smokeurl'):
                type = ele.select_one('strong').get_text().strip()
                links = []
                for elem in ele.select('a'):
                    name = elem.get_text().strip()
                    url = elem['href']
                    links.append({'name': name, 'url': url})

                download_link.append({'type': type, 'links': links})

            anime['list_download'].append({'title': title, 'download_link': download_link})

        return {'success': True, 'data': anime}
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
