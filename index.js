import puppeteer from 'puppeteer-core';

async function run() {
	let browser;

	try {

		const auth = 'brd-customer-hl_f6571868-zone-scraping_browser1:t0szjoghu448';

		browser = await puppeteer.connect({
			browserWSEndpoint: `wss:\\${auth}@brd.superproxy.io:9222`
		});

		const page = await browser.newPage();
		page.setDefaultNavigationTimeout(2 * 60 * 1000);

		await page.goto('https://www.amazon.com/Best-Sellers/zgbs');

		// ============================================================

		const selector = '.a-carousel';

		await page.waitForSelector(selector);
		const el = await page.$(selector);

		const text = await el.evaluate(e => e.innerHTML);

		console.log(text);

		// ============================================================

		// const products = await page.evaluate(() => {
		// 	const productList = [];
		
		// 	// Select all list items with class 'a-carousel-card'
		// 	const items = document.querySelectorAll('.a-carousel-card');
		
		// 	items.forEach((item) => {
		// 	  const productName = item.querySelector('div.p13n-sc-truncate-desktop-type2').textContent.trim();
		// 	  const productPrice = item.querySelector('span._cDEzb_p13n-sc-price_3mJ9Z').textContent.trim();
		
		// 	  productList.push({ name: productName, price: productPrice });
		// 	});
		
		// 	return productList;
		//   });
		
		//   console.log(products);

		// ================================================
		

		return;

	} catch (e) {
		console.error('scrape failed', e);
	}
	finally {
		await browser?.close();
	}
}

run()