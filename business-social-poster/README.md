# Business Social Poster

Automatically posts to your Facebook Pages once a day, using Facebook's
Graph API and GitHub Actions (free, runs in the cloud, no manual steps
once it's set up).

## How it works
- `posts.json` in each business folder holds a list of posts (caption,
  and optionally an image_url).
- `progress.json` tracks which post was used last, so each day it moves
  to the next one and loops back around when it reaches the end.
- `post_to_facebook.py` reads the next post and publishes it to the
  Facebook Page.
- `.github/workflows/daily-post.yml` runs that script automatically,
  once a day, using GitHub's free scheduler.

## One-time setup (per business Page)
1. In your repo's Settings → Secrets and variables → Actions, add:
   - `FB_PAGE_TOKEN` — the Page Access Token for that business's Page
   - `FB_PAGE_ID` — the numeric Page ID for that business's Page
2. Add a folder for the business (e.g. `fall-decor/`) with its own
   `posts.json`.
3. Copy the `post-horse-blanket-washing` job in `daily-post.yml`, give
   the copy a new name, and point its `POSTS_FILE` / `PROGRESS_FILE` at
   the new business's folder, with its own secrets if using a
   different Page.

## Adding more posts
Just edit `posts.json` for that business and add more entries — no
code changes needed. The script will keep cycling through whatever is
in the list, in order, looping back to the start when it runs out.

## Finding your Page ID
In Graph API Explorer, run `me/accounts` — it lists each Page you
manage along with its `id`. That's the value for `FB_PAGE_ID`.
