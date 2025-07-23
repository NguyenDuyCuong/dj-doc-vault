# TangThuVien Chapter Links Crawler

This repository contains a reusable script `craw_tangthuvien.py` that collects all chapter links for any story hosted on [truyen.tangthuvien.vn](https://truyen.tangthuvien.vn/).

## Requirements

```bash
pip install -r requirements.txt
```

`requirements.txt` already includes `crawl4ai` and its sub-packages.

## Usage

```bash
python craw_tangthuvien.py \
    --story_id 38060 \
    --slug tran-van-truong-sinh \
    --pages 15 \
    --out_dir output
```

Arguments:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--story_id` | Yes | Numeric ID that appears in the endpoint `/doc-truyen/page/{id}`. |
| `--slug` | Yes | Human-readable slug of the story, used to name the output file. |
| `--pages` | Yes | Last page index (0-based) returned by the API. Example: if there are 16 pages `0..15` set it to `15`. |
| `--out_dir` | No  | Directory where the chapter link file will be saved. Defaults to the current directory. |

The script will generate a file named `<slug>_chapter_links.txt` containing one chapter URL per line.

### Example Output

```
output/
└── tran-van-truong-sinh_chapter_links.txt
```

## How to obtain `story_id` and `pages`

1. Open the browser's developer tools on the story's table-of-contents page.
2. Navigate one page further in the list; observe the network request similar to:
   `https://truyen.tangthuvien.vn/doc-truyen/page/38060?page=0&limit=75&web=1`
3. The number after `/page/` is the `story_id`.
4. Keep increasing the `page` parameter until the response returns an empty list. The highest successful index is your `--pages` value.

## Extending or Integrating

* You can import `get_chapter_links_api` from the script and use it in your own code – it returns a Python `set` of chapter URLs.
* Feel free to rename the script; the functionality is decoupled from the filename.

## License

This repo is provided for personal use and study. Always respect the target website's robots.txt and terms of service when scraping.
