import asyncio
import json
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext


async def main() -> None:
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=1,
        headless=True,
        browser_type='chromium',
    )

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        context.log.info(f'Processing {context.request.url} ...')

        page = context.page
        await page.wait_for_load_state('networkidle')

        items = await page.query_selector_all('[data-test="currency__rates-form__result-item"]')
        context.log.info(f'Found {len(items)} offers')

        offers = []
        for item in items:
            def text(el):
                return el.inner_text() if el else None

            bank_el = await item.query_selector('[data-test="currenct--result-item--name"]')
            address_el = await item.query_selector('[data-test="currency--result-item--address"]')
            special_offer_el = await item.query_selector('[data-test="text"].boiOce')
            buy_el = await item.query_selector('[data-test="currency--result-item---rate-buy"] [data-test="text"]:last-child')
            sell_el = await item.query_selector('[data-test="currency--result-item---rate-sell"] [data-test="text"]:last-child')
            refresh_el = await item.query_selector('[data-test="currency--result-item--refresh-date"]')
            logo_link_el = await item.query_selector('[data-test="currency--result-item--logo"]')
            logo_img_el = await item.query_selector('[data-test="currency--result-item--logo"] img')

            offer = {
                'bank_name': await bank_el.inner_text() if bank_el else None,
                'rate_type': await address_el.inner_text() if address_el else None,
                'special_offer': await special_offer_el.inner_text() if special_offer_el else None,
                'buy_rate': await buy_el.inner_text() if buy_el else None,
                'sell_rate': await sell_el.inner_text() if sell_el else None,
                'updated_at': await refresh_el.inner_text() if refresh_el else None,
                'link': await logo_link_el.get_attribute('href') if logo_link_el else None,
                'logo_url': await logo_img_el.get_attribute('src') if logo_img_el else None,
            }
            offers.append(offer)

        await context.push_data(offers)

    await crawler.run(['https://www.banki.ru/products/currency/landing/9/'])

    data = await crawler.get_data()
    crawler.log.info(f'Extracted {len(data.items)} records')

    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data.items, f, ensure_ascii=False, indent=2)

    crawler.log.info('Saved to results.json')


if __name__ == '__main__':
    asyncio.run(main())
