import json
import time
from typing import Dict
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URLS = [
    ""
]


def make_driver():
    options = Options()
    # не headless — многие WAF/антиботы блокируют
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def scroll_to_bottom(driver, pause=0.6, max_loops=30):
    """Плавно доскролливаем до конца страницы (на случай ленивой подгрузки)."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    loops = 0
    while loops < max_loops:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # финальный микроскролл вверх-вниз — добить ленивые блоки
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 200);")
            time.sleep(pause / 2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause / 2)
            if driver.execute_script("return document.body.scrollHeight") == last_height:
                break
        last_height = new_height
        loops += 1


def extract_article(driver) -> Dict[str, str]:
    try:
        # Ждём загрузки страницы
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(1)  # Дополнительная пауза для JS

        # Прокрутка страницы для загрузки контента
        scroll_to_bottom(driver, pause=0.3, max_loops=10)

        # ========== ПОИСК ЗАГОЛОВКА ==========
        title = ""
        title_selectors = [
            # Популярные варианты
            (By.TAG_NAME, "h1"),
            (By.CSS_SELECTOR, "h1.title"),
            (By.CSS_SELECTOR, "h1.entry-title"),
            (By.CSS_SELECTOR, "h1.post-title"),
            (By.CSS_SELECTOR, "article h1"),
            (By.CSS_SELECTOR, ".article-title"),
            (By.CSS_SELECTOR, "[class*='title'] h1"),
            # Для новостных сайтов
            (By.CSS_SELECTOR, "h1[itemprop='headline']"),
            (By.CSS_SELECTOR, "h1.headline"),
            # Wikipedia
            (By.ID, "firstHeading"),
            # Medium
            (By.CSS_SELECTOR, "h1[data-testid='storyTitle']"),
        ]

        for by, selector in title_selectors:
            try:
                element = driver.find_element(by, selector)
                title = element.text.strip()
                if title and len(title) > 3:
                    print(f"Заголовок найден ({selector}): {title[:50]}...")
                    break
            except:
                continue

        # Если не нашли, берём title страницы
        if not title:
            title = driver.title.strip()
            print(f"Использован title страницы: {title[:50]}...")

        # ========== ПОИСК ОСНОВНОГО КОНТЕНТА ==========
        text_parts = []

        # Стратегия 1: Ищем основной контейнер контента
        content_selectors = [
            # Общие контейнеры
            (By.TAG_NAME, "article"),
            (By.CSS_SELECTOR, "main article"),
            (By.CSS_SELECTOR, "[role='article']"),
            (By.CSS_SELECTOR, ".article-content"),
            (By.CSS_SELECTOR, ".post-content"),
            (By.CSS_SELECTOR, ".entry-content"),
            (By.CSS_SELECTOR, ".content-body"),
            (By.CSS_SELECTOR, "[class*='article'][class*='body']"),
            (By.CSS_SELECTOR, "[class*='post'][class*='body']"),
            # Wikipedia
            (By.ID, "mw-content-text"),
            # Medium
            (By.TAG_NAME, "article"),
            # Общий main
            (By.TAG_NAME, "main"),
        ]

        content_container = None
        for by, selector in content_selectors:
            try:
                container = driver.find_element(by, selector)
                # Проверяем, что контейнер содержит достаточно текста
                if container.text.strip() and len(container.text.strip()) > 100:
                    content_container = container
                    break
            except:
                continue

        # Стратегия 2: Собираем текст из найденного контейнера или со всей страницы
        if content_container:
            # Из контейнера берём параграфы и заголовки
            elements = content_container.find_elements(
                By.CSS_SELECTOR,
                "p, h2, h3, h4, li, blockquote, pre"
            )
        else:
            # Fallback: берём со всей страницы, но более избирательно
            elements = driver.find_elements(By.TAG_NAME, "p")

        # Собираем текст, фильтруя служебные элементы
        skip_patterns = {
            "cookie", "согласие", "privacy", "subscribe", "newsletter",
            "реклама", "advertisement", "sponsored", "комментари",
            "читайте также", "related", "share", "tweet", "facebook"
        }

        seen = set()  # Избегаем дубликатов
        for element in elements:
            text = element.text.strip()

            # Базовые фильтры
            if not text or len(text) < 10:
                continue
            if text in seen:
                continue

            # Проверка на служебный текст
            text_lower = text.lower()
            if any(pattern in text_lower for pattern in skip_patterns):
                continue

            text_parts.append(text)
            seen.add(text)

        full_text = " ".join(text_parts)

        # Если получили совсем мало текста, пробуем более агрессивный сбор
        if len(full_text) < 200:
            all_p = driver.find_elements(By.TAG_NAME, "p")
            full_text = " ".join([p.text.strip() for p in all_p if p.text.strip() and len(p.text.strip()) > 20])

        print(f"Текст извлечён: {len(full_text)} символов, {len(text_parts)} фрагментов")

        return {
            "title": title or "Без заголовка",
            "text": full_text if full_text else "Текст не найден"
        }

    except Exception as e:
        print(f"Критическая ошибка в extract_article: {e}")
        import traceback
        traceback.print_exc()
        return {
            "title": driver.title.strip() if driver.title else "Ошибка",
            "text": "Ошибка извлечения контента"
        }


def get_next_filename(base_name="parsed_data", extension=".json"):
    """Находит следующий доступный номер для имени файла."""
    counter = 1
    while True:
        filename = f"{base_name}{counter}{extension}"
        if not os.path.exists(filename):
            print(f"Будет создан файл: {filename}")
            return filename
        counter += 1


def main():
    print("Запуск парсера...")
    driver = make_driver()
    results = []

    try:
        for url in URLS:
            print(f"\nОбработка URL: {url}")
            try:
                driver.get(url)
                time.sleep(2)  # Даём странице загрузиться

                item = extract_article(driver)
                results.append({
                    "title": item["title"],
                    "url": url,
                    "text": item["text"]
                })
                print(f"OK: {url} (символов: {len(item['text'])})")

            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")
                import traceback
                traceback.print_exc()

    finally:
        print("\nЗакрытие браузера...")
        driver.quit()

    # Сохранение результатов
    if results:
        filename = get_next_filename()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nГотово! Сохранено {len(results)} записей в файл '{filename}'")
    else:
        print("\nНет данных для сохранения")


if __name__ == "__main__":
    main()
    
