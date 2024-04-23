import puppeteer from "puppeteer";

const base_url = "https://www.albumoftheyear.org/genre/list.php";
(async () => {
  // Launch the browser and open a new blank page
  const browser = await puppeteer.launch({ headless: false, slowMo: 250 });
  const page = await browser.newPage();

  // Navigate the page to a URL
  await page.goto(base_url);
  await page.setViewport({ width: 1080, height: 1024 });

  const all_genres_cnt = await page.$(".genreList");
  const genre_divs = await all_genres_cnt.$$(":scope > *");
  const genre_link = await page.$(".showSubGenres");
  genre_link.click();
  genres_flat = [];
  genres_tree = [];
  for (let i = 0; i < genre_divs.length; i++) {
    if ((await genre_divs[i].$$(":scope > *").length) > 1) {
      const sub_genres = await page.$$(".subGenreRow");
      genres_flat.push({
        genre: await page.evaluate((el) => el.textContent, genre_divs[i]),
        children: [],
      });
      genres_tree.push({
        genre: await page.evaluate((el) => el.textContent, genre_divs[i]),
        children: [],
      });
    } else {
      genres_flat.push({
        genre: await page.evaluate((el) => el.textContent, genre_divs[i]),
      });
      genres_tree.push({
        genre: await page.evaluate((el) => el.textContent, genre_divs[i]),
      });
    }
  }

  await browser.close();
})();
