import puppeteer from "puppeteer";

// const base_url = "https://www.albumoftheyear.org/genre/list.php";
const base_url = "https://pptr.dev/faq";
(async () => {
  // Launch the browser and open a new blank page
  const browser = await puppeteer.launch({ headless: false, slowMo: 1000 });
  const page = await browser.newPage();

  // Navigate the page to a URL
  await page.goto(base_url);

  const all_genres_cnt = await page.waitForSelector(".genreList");
  console.log(all_genres_cnt.length);

  const children = await page.$x('//*[@class="genreList"]//*');

  const fullTitle = await all_genres_cnt?.evaluate((el) => el.textContent);

  for (const genre_div in all_genres_cnt) {
    for (const genre_children in genre_div) {
    }
  }
  // Print the full title
  console.log('The title of this blog post is "%s".', fullTitle);

  await browser.close();
})();
