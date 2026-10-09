export default async function run(page) {
  await page.goto('http://127.0.0.1:8000/');
  await page.waitForSelector('#header-lang-toggle');
  const select = async lang => {
    await page.locator('#header-lang-toggle').click();
    await page.locator(`button[onclick="changeLanguage('${lang}')"]`).click();
    await page.waitForTimeout(1500);
    return {
      label: await page.locator('#lang-text').innerText(),
      htmlLang: await page.locator('html').getAttribute('lang'),
      dashboard: await page.locator('[data-i18n="nav_dashboard"]').innerText()
    };
  };
  const hindi = await select('hi');
  const marathi = await select('mr');
  await page.locator('#nav-item-fields').click();
  await page.waitForTimeout(500);
  const farms = await page.locator('#view-fields').innerText();
  await page.locator('#nav-item-weather').click();
  await page.waitForTimeout(500);
  const weather = await page.locator('#view-weather').innerText();
  await page.locator('#nav-item-advisory').click();
  await page.waitForTimeout(500);
  const advisory = await page.locator('#view-advisory').innerText();
  return {
    hindi,
    marathi,
    farmsHasEnglishLabel: farms.includes('Register New Farm') || farms.includes('Loading registered farm plots'),
    weatherHasEnglishLabel: weather.includes('Live Weather Telemetry') || weather.includes('Temperature'),
    advisoryHasEnglishLabel: advisory.includes('Integrated Pest Management') || advisory.includes('Print Advisory')
  };
}
