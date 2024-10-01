<p align="center">
    <a href="https://github.com/paulocoutinhox/kaktos" target="_blank" rel="noopener noreferrer">
        <img width="180" src="extras/images/logo.png" alt="Kaktos Logo">
    </a>
    <br>
    <br>
    Python Static Site Generator for Serverless Applications 🚀
    <br>
</p>

<br>

# κάκτος - Kaktos

[![Kaktos](https://github.com/paulocoutinhox/kaktos/actions/workflows/build.yml/badge.svg)](https://github.com/paulocoutinhox/kaktos/actions/workflows/build.yml)

Kaktos is a powerful **Python Static Site Generator** designed to create highly efficient **serverless** applications. Why pay for hosting when you can deploy a completely static site for free?

Create beautiful static websites, e-commerce stores, blogs, landing pages, and sales pages with **advanced pagination** and **dynamic features**, all without the hassle of server-side dependencies! 💻

## ✨ Features

- **Static Website Generator** – Create responsive, fast, and secure static sites 🖼️
- **Static E-commerce** – Build fully functioning static shopping websites 🛒
- **Static Blog** – Advanced blog with pagination and dynamic content 📝
- **Landing Pages & Sales Pages** – Perfect for creating high-conversion pages for any purpose 🛍️
- **Easy to Use** – Intuitive design that requires no server-side programming 💡
- **Serverless** – Deploy to platforms like Netlify, Cloudflare, or Render with no need for server management ☁️
- **Many Free Hosting Options** – Many companies offer free hosting for static sites, as no server-side processing is required 🌐
- **Fast & Secure** – Static sites are inherently faster and more secure ⚡
- **No Hosting Fees** – Fully serverless deployment means **no hosting costs** 🆓
- **SEO Optimized** – Generate clean, SEO-friendly pages 🕵️‍♂️
- **Customizable Templates** – Based on the powerful Jinja2 templating engine 🎨

## 🤔 Why Kaktos?

With **Kaktos**, you can deploy your website without worrying about server management, database configuration, or paying for hosting. Focus on your content, and let Kaktos handle the rest. Enjoy the benefits of a **serverless architecture**, which has become a major trend in web development, reducing operational costs and simplifying the deployment process for companies of all sizes.

- No need to manage infrastructure
- No ongoing hosting fees
- Scalable and fast deployment
- Ideal for websites, blogs, e-commerce, and landing pages

## 🔄 All-in-One Solution

Unlike most static site generators, which focus on specific tasks, **Kaktos** provides an **all-in-one** solution.

Whether you need to build a blog, an e-commerce store, a landing page, or any other static website, Kaktos brings it all together in one platform, simplifying your workflow and allowing you to manage everything in a single place.

## 🎬 Demo

**Cloudflare:**

[https://kaktos.pages.dev](https://kaktos.pages.dev)

**Netlify:**

[https://kaktos.netlify.app](https://kaktos.netlify.app)

**Amplify:**

[https://main.d27ze19drzixy0.amplifyapp.com](https://main.d27ze19drzixy0.amplifyapp.com)

**Render:**

[https://kaktos.onrender.com](https://kaktos.onrender.com)

## Requirements

- Python 3.8+

## 🚀 How to Get Started

Install python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## 💻 Development

To work in development mode, you only need execute one command:

```bash
python3 kaktos.py
```

When you change any file locally, the server will `process` it again and `auto-refresh` on browser.

This command *always force* use development mode, with or without environment variable.

## 🏭 Production

To generate production files, you only need execute one command:

```bash
python3 kaktos.py build
```

All files will be generated in `build` folder.

If you set environment variable `KAKTOS_DEBUG=True`, kaktos will build all files for development mode, example:

```bash
KAKTOS_DEBUG=True python3 kaktos.py build
```

If you want start a web server to test files inside `build` folder use:

```bash
python3 kaktos.py serve
```

## 📦 Deploying with One Click

**Netlify:**

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/paulocoutinhox/kaktos)

**Render:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/paulocoutinhox/kaktos/tree/render-support)

## 🏗️ Project Structure

- `kaktos.py` = main file that process your command
- `requirements.txt` = python dependency list
- `templates/layouts` = folder for all layouts that pages can inherit
- `templates/pages` = folder for pages that will be generated
- `templates/shared` = folder for parts of layouts that can be shared with other layouts
- `modules` = kaktos modules
- `modules/config.py` = configuration file
- `files` = folder that contains all assets and custom files
- `extras/config` = folder that contains some configurations for dynamic sample data

## 🔧 Commands

Each command supported by **Kaktos** is a Python file located in the `modules/commands/` folder.

To add new commands, simply create a new Python file in the `modules/commands/` folder and implement the `def run(params={})` method within it.

## 📝 Templates

All templates (html files) are based on Jinja2 library. You can see it here:

https://jinja.palletsprojects.com/en/3.0.x/

## 🛠️ Troubleshooting

#### **• Python version**

Each service that build the static content automatically use a specific python version.

If you need change the python version used to build all files and pages, edit file `runtime.txt` and change to `3.8`, `3.9` or other.

These services that im using have this python version:

- Netlify: Python 3.8 (https://docs.netlify.com/configure-builds/available-software-at-build-time/)
- Cloudflare Pages: Python 3.11.5 (https://developers.cloudflare.com/pages/configuration/language-support-and-tools)

#### **• Template changed, but not reloaded**

Invalid Jinja2 syntax can prevent your HTML template from being built.

Check your terminal to see the error message, the HTML file and the line number where invalid syntax was detected.

## ☕ Buy me a coffee

<a href='https://ko-fi.com/paulocoutinho' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi1.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## 🖼️ Images

All images for demo i got from:

https://unsplash.com/

## 📜 License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2021-2024, Paulo Coutinho
