import asyncio
import aiohttp
import feedparser
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

keywords = ["nutella"]

async def fetch_feed(session, url):
    try:
        async with session.get(url) as response:
            content = await response.text()
            return url, feedparser.parse(content)
    except Exception as e:
        logging.error(f"Erreur sur {url} : {e}")
        return url, None

def find_matching_articles(parsed_feed, keywords):
    articles = []
    for entry in parsed_feed.entries:
        content = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
        for keyword in keywords:
            if keyword in content:
                articles.append({
                    'title': entry.get('title', 'No title'),
                    'published': entry.get('published', 'No date'),
                    'link': entry.get('link', 'No link'),
                    'keyword': keyword
                })
                break
    return articles

async def process_rss_url(session, url):
    _, parsed_feed = await fetch_feed(session, url)
    if parsed_feed:
        return find_matching_articles(parsed_feed, keywords)
    return []

async def main():
    try:
        with open('rss_list.txt', 'r', encoding='utf-8') as f:
            rss_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("Fichier rss_list.txt non trouvé")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [process_rss_url(session, url) for url in rss_urls]
        output_file = 'resultat.txt'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for task in asyncio.as_completed(tasks):
                    results = await task
                    for result in results:
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
