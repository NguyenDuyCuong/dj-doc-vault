import asyncio
import argparse
from pathlib import Path
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
import re

async def get_chapter_links_api(story_id: int, last_page: int, crawler: AsyncWebCrawler, run_config: CrawlerRunConfig):
    """Crawl all paginated list pages starting from `list_url` and return a set of chapter links.

    The function keeps requesting pages by following pagination links until no new chapter links are found.
    This approach works for sites that use JavaScript-powered pagination.
    """
    collected_links: set[str] = set()
    api_template = (
        f"https://truyen.tangthuvien.vn/doc-truyen/page/{story_id}?limit=75&web=1&page={{page}}"
    )

    for page in range(0, last_page + 1):
        api_url = api_template.format(page=page)
        result = await crawler.arun(url=api_url, config=run_config)
        if not result.success:
            print(f"Skip page {page}: {result.error_message}")
            continue

        new_links = {
            link["href"]
            for link in result.links["internal"]
            if "chuong-" in link["href"]
        }
        before = len(collected_links)
        collected_links.update(new_links)
        added = len(collected_links) - before
        print(f"Page {page}: +{added} chapters (total {len(collected_links)})")

    return sorted(collected_links)


async def download_chapters(links: list[str], crawler: AsyncWebCrawler, run_config: CrawlerRunConfig, dest: Path):
    """Download content of each chapter link and save as markdown files in *dest* directory."""
    dest.mkdir(parents=True, exist_ok=True)
    for idx, link in enumerate(links, start=1):
        res = await crawler.arun(url=link, config=run_config)
        if not res.success:
            print(f"Failed to crawl {link}: {res.error_message}")
            continue

        # Extract chapter number from URL or title
        m = re.search(r"chuong-(\d+)", link)
        chap_num = m.group(1) if m else f"{idx}"
        filename = dest / f"chapter_{chap_num}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(res.markdown)
        print(f"Saved chapter {chap_num} -> {filename}")

async def main():
    # CLI arguments
    parser = argparse.ArgumentParser(description="Crawl chapter links from TangThuVien")
    parser.add_argument("--story_id", type=int, required=True, help="Numeric ID in /doc-truyen/page/{id}")
    parser.add_argument("--slug", required=True, help="Story slug used for filename, e.g. tran-van-truong-sinh")
    parser.add_argument("--pages", type=int, required=True, help="Last page index (0-based)")
    parser.add_argument("--out_dir", default=".", help="Directory to save output files and chapters")
    args = parser.parse_args()

    story_id = args.story_id
    last_page = args.pages
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,

        # Content processing
        process_iframes=True,
        remove_overlay_elements=True,

        # Cache control
        cache_mode=CacheMode.ENABLED  # Use cache if available
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        chapter_links = await get_chapter_links_api(story_id=story_id, last_page=last_page, crawler=crawler, run_config=run_config)

        print("\n======= FOUND CHAPTER LINKS =======")
        for link in sorted(chapter_links):
            print(link)

        # Save to file
        output_path = output_dir / f"{args.slug}_chapter_links.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for link in sorted(chapter_links):
                f.write(link + "\n")
        print(f"Saved {len(chapter_links)} links to {output_path}")

        # Download chapter contents
        chapters_dir = output_dir / args.slug
        print(f"\nDownloading chapter contents to {chapters_dir} ...")
        await download_chapters(chapter_links, crawler, run_config, chapters_dir)
        print("Download completed.")

if __name__ == "__main__":
    asyncio.run(main())
