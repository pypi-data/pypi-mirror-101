# DjangoCMS FAQ

Frequently asked questions plugin for Django CMS, with an API to load questions from another page!

## Install

1) Install module
   ```
   python3 -m pip install djangocms-faq
   ```

2) Add it to your INSTALLED_APPS
   ```
       "djangocms_faq",
   ```

3) Add the API endpoint to your `urls.py` (if you want to use the Faq Search Plugin):
    ```python
        path("djangocms-faq/", include("djangocms_faq.urls")),
    ```

4) Launch your django-cms site, it should be here!

    ![](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/4d774d9e28e4125db633e80234569c2e/image.png)

### Requirements

* `django-cms`: Obviously
* `django-sekizai`: For default templates (you can uninstall it if you use custom templates without sekizai). Not required in this package (it's a requirement of django-cms).

## Features

### A faq

Add **faq container** plugins (which have a title and can contain only faq questions plugins).

Then, add **faq questions** plugins that can contain text/image/videos plugins (that provide answers)!

You can also add keywords to your FAQ questions, because you may want your users to find a specific answer to a general question.

![Here's a small demo video](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/c255a0763de90fd10dff72a013c2990e/create-faq-demo.webm)

### A search plugin that uses an API

Ask a question to the FAQ and the plugin will return with the corresponding questions/answers.

![Here's another small demo video](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/7762aa21673c498686f5b19c3cc37a54/create-faq-search-plugin-demo.webm)

*Quick note: since the form uses javascript **and** a simple view, that means that the search works without javascript too!*

### Select in which FAQ the searches will be applied

![](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/eb973135b140f8fcf7fe455aed3ffca5/image.png)

Display format is `Faq Container − {FAQ Name} − {Page title}`.

## Configuration

* `DJANGOCMS_FAQ_ENABLE_API` (default is `True`): Enable or not the API endpoint and the Faq Search plugins.

    *If you create a Faq Search Plugin and then set this setting to `False`, then you will be greeted with a cool `KeyError 'FaqPluginSearchPublished'` error message. Please do not do this.*

* `DJANGOCMS_FAQ_ANSWER_PLUGINS` (default is `["TextPlugin", "FilePlugin", "VideoPlayerPlugin"]`): Add plugins that can be added to your answers!

* `DJANGOCMS_FAQ_SHOW_KEYWORDS_QUESTION` (default is `True`): Display keywords in the questions of a FAQ.

* `DJANGOCMS_FAQ_SHOW_KEYWORDS_ANSWER` (default is `True`): Display keywords in answers (faq search plugin).

## API

When you're searching for something in the input, searches will be made using the API if you don't type anything for 1 second (see `templates/faq_search.html`).

Here's the format:

```json
[
  {
    "question": "question title",
    "slug": "question-title",
    "url": "/page-url/",
    "keywords": ["keyword", "keywords", "..."]
  },
  {
    "question": "question title 2",
    "slug": "question-title2",
    "url": "/page-url/",
    "keywords": ["keyword", "keywords", "..."]
  },
]
```

## Customize it!

The template included in this project is for demonstration purposes only, it is up to you to integrate it into your graphic charter by creating a file in `templates/faq/faq_plugin.html`.

## How it works

Faq container & questions are classic django-cms plugins, see in `cms_plugins.py` for more informations.

Faq search plugin is a django-cms plugin, and uses on top of that an API endpoint using vanilla javascript (the default template uses `fetch`, which is [not compatible](https://caniuse.com/fetch) with IE).

The API endpoint is a single view that returns json (see `views.py`).

Since the function to get answers from a "question" str is used two times (in the view for the API and in the FaqPluginSearchPublisher plugin), I've put it in a file named `utils.py`.
