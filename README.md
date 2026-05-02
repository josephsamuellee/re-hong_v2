# Re Hong Technology — marketing site (re-hong.com)

Static marketing site for **Re Hong Technology**, a Taiwan-based CNC machining and process-integration partner (Taoyuan). Built for **Cloudflare Pages**: no bundler, fast builds, easy previews.

## Local preview

From this directory:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`.

## Cloudflare Pages

1. Push this repository to GitHub (see below).
2. In the Cloudflare dashboard: **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. Select the repository and use these settings:
   - **Framework preset**: None
   - **Build command**: *(leave empty)*
   - **Build output directory**: `/` (repository root, where `index.html` lives)

Production URLs will match your Pages hostname until you attach a custom domain.

### Custom domain (re-hong.com)

1. In the Pages project: **Custom domains** → **Set up a domain** → enter `re-hong.com` (and `www` if desired).
2. At your DNS provider, add the records Cloudflare shows (or delegate DNS to Cloudflare).
3. TLS certificates are issued automatically once DNS validates.

### Assets note

Product photos and the logo were copied from `~/Documents/baba_website` into this repo (`/logo.png`, `/images/products_*.jpg`). Update images there and recopy if branding changes.

## GitHub repository

Initialize and push (replace `YOUR_USER` with your GitHub username):

```bash
cd ~/Documents/re-hong_v2
git init
git add .
git commit -m "Add Re Hong marketing site for Cloudflare Pages"
git branch -M main
git remote add origin https://github.com/YOUR_USER/re-hong_v2.git
git push -u origin main
```

If you use the GitHub CLI and are logged in:

```bash
gh repo create re-hong_v2 --public --source=. --remote=origin --push
```

## SEO files

- [`robots.txt`](robots.txt) — allows crawlers; references the sitemap.
- [`sitemap.xml`](sitemap.xml) — lists `https://re-hong.com/` and `https://re-hong.com/careers.html`.

Update the site URL in both files if you use a different hostname during staging.

## License

Site content is for Re Hong Technology. All rights reserved.
