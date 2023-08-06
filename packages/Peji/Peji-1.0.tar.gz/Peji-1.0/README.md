# Pēji

**Pēji** (Japanese: ページ, "page") is simple way to generate small static sites (one or more pages).

If you need to collect several pages from the Markdown, then Pēji are great for you.

**Note**: Pēji is not intended to generate a blog site. Its single pages only. You can link pages with hyper-links, but you have to do it manually.

Features:

- [Python-Markdown](https://python-markdown.github.io/) is used.
- Code syntax highlighting via [Pygments](https://pygments.org/).
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) template engine.
- Custom style and layout for specific page.
- Site menu bar can be edited through the config.
- YAML config file.

## Installation and quickstart

Install Pēji globally or into virtual environment:

```bash
pip install Peji
```

Create your site:

```bash
peji create mysite
cd mysite/
```

Create your first page and place it into `mysite/pages/`:

`index.md`:

```markdown
---
title: My first page
---

# My heading

It works!
```

Build your site:

```
peji build
```

Site will be placed in `./mysite/build`.

Also you can run Python built-in HTTP Server:

```bash
python3 -m http.server --directory build/
```

## License

Pēji is released under The Unlicense. See [https://unlicense.org/](https://unlicense.org/) for detais.
