import asyncio
import aiohttp
import feedparser
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

keywords = ["mode"]

async def fetch_feed(session, url):
    try:
        async with session.get(url) as response:
            content = await response.text()
            return content
    except Exception as e:
        logging.error(f"Erreur sur {url} : {e}")
        return None

async def parse_feed(url):
    async with aiohttp.ClientSession() as session:
        content = await fetch_feed(session, url)
        if content is None:
            return []

        feed = feedparser.parse(content)
        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.get("title", "N/A"),
                "link": entry.get("link", "N/A"),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", "N/A")
            })
        return articles

async def process_rss_url(url):
    logging.info(f"Looking in {url}")
    articles = await parse_feed(url)
    results = []
    for article in articles:
        for keyword in keywords:
            if keyword.lower() in article["title"].lower() or keyword.lower() in article["summary"].lower():
                # logging.info(f"{article['title']} ({article['published']}) - Mot-clé : {keyword}")
                # logging.info(f" {article['link']}")
                results.append({
                    "title": article['title'],
                    "published": article['published'],
                    "link": article['link'],
                    "keyword": keyword
                })
    return results

async def main():
    try:
        with open('rss_list.txt', 'r', encoding='utf-8') as f:
            rss_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("Fichier rss_list.txt non trouvé")
        return

    tasks = [process_rss_url(url) for url in rss_urls]
    results = await asyncio.gather(*tasks)

    output_file = 'resultat.txt'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result_list in results:
                for result in result_list:
                    f.write(f"📖 Titre : {result['title']}\n")
                    f.write(f"📅 Date de publication : {result['published']}\n")
                    f.write(f"🔗 URL : {result['link']}\n")
                    f.write(f"🔑 Mot-clé : {result['keyword']}\n\n")
        logging.info(f"Fichier {output_file} créé avec succès")
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture dans le fichier {output_file} : {e}")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())

    logging.info(f"Temps d'exécution : {time.time() - start_time} secondes")
