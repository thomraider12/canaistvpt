import aiohttp
import asyncio

async def testar_stream(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                print(f"✅ Funciona: {url}")
            else:
                print(f"❌ Erro ({response.status}): {url}")
    except Exception as e:
        print(f"⚠️ Erro ao aceder: {url} -> {e}")

async def main():
    # Caminho para o ficheiro M3U
    m3u_path = 'pt.m3u'

    # Ler o ficheiro M3U
    with open(m3u_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extrair apenas os links após linhas com #EXTINF:
    urls = []
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF:') and i + 1 < len(lines):
            url = lines[i + 1].strip()
            if url.startswith('http'):
                urls.append(url)

    # Sessão assíncrona para testar as streams
    async with aiohttp.ClientSession() as session:
        tasks = [testar_stream(session, url) for url in urls]
        await asyncio.gather(*tasks)

# Executar o script
asyncio.run(main())