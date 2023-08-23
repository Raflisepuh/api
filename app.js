const express = require('express');
const request = require('request-promise');
const cheerio = require('cheerio');

const app = express();
const port = 3000;

app.get('/anime/:endpoint', async (req, res) => {
    try {
        const { endpoint } = req.params;
        const response = await request.get(endpoint);

        const $ = cheerio.load(response);
        const anime = {};

        anime.title = $('.jdlz').text().trim();
        anime.thumbnail = $('.post-thumb').find('img').attr('src');
        $('.info').find('p').each((i, el) => {
            const key = $(el).find('b').text().toLowerCase().trim().replace(' ', '_');
            $(el).find('b').remove();
            const value = $(el).text().split(':').pop().trim();
            anime[key] = value === '' ? null : value;
        });
        anime.sinopsis = $('.lexot > p').text().trim();

        anime.list_download = [];
        $('#dl').find('.smokeddlrh').each((i, el) => {
            const download_link = [];
            const title = $(el).find('.smokettlrh').text().trim();

            $('.smokeurlrh').each((j, ele) => {
                const type = $(ele).find('strong').text().trim();

                const links = [];
                $(ele).find('a').each((k, elem) => {
                    const name = $(elem).text().trim();
                    const url = $(elem).attr('href');

                    links.push({ name, url });
                });

                download_link.push({ type, links });
            });

            $('.smokeurl').each((j, ele) => {
                const type = $(ele).find('strong').text().trim();

                const links = [];
                $(ele).find('a').each((k, elem) => {
                    const name = $(elem).text().trim();
                    const url = $(elem).attr('href');

                    links.push({ name, url });
                });

                download_link.push({ type, links });
            });

            anime.list_download.push({ title, download_link });
        });

        return res.json({ success: true, data: anime });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
