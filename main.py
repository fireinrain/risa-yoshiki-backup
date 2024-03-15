from bs4 import BeautifulSoup
import random
import aiohttp
import asyncio
import os

# 硬编码的User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36",
    # 添加更多User-Agent字符串
]


async def fetch_html(url: str, user_agent: str) -> str:
    headers = {'User-Agent': user_agent}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_html_with_code(url: str, user_agent: str) -> (str, int):
    headers = {'User-Agent': user_agent}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text(), response.status


async def download_image(image_url: str, user_agent: str, pname: str, folder: str = "images"):
    # Ensure the folder to save images exists
    download_folder = folder + os.sep + pname
    os.makedirs(download_folder, exist_ok=True)
    # Get the filename of the image
    filename = os.path.join(download_folder, image_url.split("/")[-1])

    headers = {'User-Agent': user_agent}
    # Asynchronously download the image
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(image_url) as response:
            content = await response.read()
            # Save the image
            with open(filename, 'wb') as f:
                f.write(content)
    print(f"Image saved as {filename}")


async def parse_and_download_images(html: str, user_agent: str, pname: str):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.select('body > div.container.pt-3 > div.mb-4.container-inner-fix-m > img')
    for img in img_tags:
        src = img.get('src')
        if src:
            image_url = f"https://meitulu.me{src}"
            await download_image(image_url, user_agent, pname)
            await asyncio.sleep(1)


async def parse_and_print_divs(html: str) -> [(str, str)]:
    result = []
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.select('body > div.container.pt-3 > div.row.my-gutters-b > div')
    for div in divs:
        a_tags = div.find_all('a')
        product_mame = div.select_one('a > div')
        if a_tags and product_mame:
            href = a_tags[0].get('href')
            pname = product_mame.text
            print(f"{pname},{href}")
            result.append((pname, href))
    return result


async def fetch_product_images(pname: str, link: str):
    url = f'https://meitulu.me{link}'
    random_user_agent = random.choice(USER_AGENTS)
    for i in range(1, 20):
        if i == 1:
            url = url
        else:
            link_split = link.split(".")
            new_url = link_split[0] + "_" + str(i) + ".html"
            url = f'https://meitulu.me{new_url}'
        html, code = await fetch_html_with_code(url, random_user_agent)
        if code == 404:
            break
        await parse_and_download_images(html, random_user_agent, pname)


async def main():
    url = 'https://meitulu.me/t/jimulisha/'
    random_user_agent = random.choice(USER_AGENTS)
    html = await fetch_html(url, random_user_agent)
    plist = await parse_and_print_divs(html)
    for p in plist:
        await fetch_product_images(p[0], p[1])


if __name__ == "__main__":
    asyncio.run(main())
