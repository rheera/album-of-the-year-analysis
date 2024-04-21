import puppeteer from "puppeteer";

const base_url = "https://pptr.dev/faq";
(async () => {
  // Launch the browser and open a new blank page
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  // Navigate the page to a URL
  await page.goto(base_url);
  await page.setViewport({ width: 1080, height: 1024 });

  const all_genres_cnt = await page.$$(".menu__list");
  console.log(all_genres_cnt.type);
  console.log(all_genres_cnt[0]);
  console.log(
    await elementHasClass(all_genres_cnt[0], "theme-doc-sidebar-menu")
  );
  const children = await page.evaluate(() => {
    return Array.from(document.querySelector(".menu__list").children).length;
  });
  console.log(await children);

  let $parent = await page.$(".menu__list");
  let $childs = await $parent.$$(":scope > *");
  console.log($childs);
  //   for (let i = 0; i < all_genres_cnt.length; i++) {
  //     const img = await all_genres_cnt[i].$eval("li", (i) =>
  //       i.getProperty("className")
  //     );
  //     console.log(img);
  //     // const link = await all_genres_cnt[i].$eval("a", (a) =>
  //     //   a.getAttribute("href")
  //     // );
  //     // console.log(link);
  //   }

  //   const fullTitle = await all_genres_cnt?.evaluate((el) => el.textContent);

  //   for (const genre_div in all_genres_cnt) {
  //     for (const genre_children in genre_div) {

  //     }
  //   }
  //   // Print the full title
  //   console.log('The title of this blog post is "%s".', fullTitle);

  await browser.close();
})();

export async function elementHasClass(el, className) {
  const classNames = (
    await (await el.getProperty("className")).jsonValue()
  ).split(/\s+/);

  return classNames.includes(className);
}
