# Zemfrog Quasar

Quasar Framework Integration

# Features

* Support vue v2
* Added Vuex & Vue-Router
* Integrated with Quasar


# Usage

Install this

```sh
pip install zemfrog-quasar
```

Add this to the `ZEMFROG_THEMES` configuration

```python
ZEMFROG_THEMES = ["zemfrog_quasar"]
```

# Quick Tutorial

In this theme, several jinja blocks are available, such as:

* `meta` - List of meta tags to include
* `links` - This is to be included in the head tag as (`link`, `title`, etc)
* `content` - This is to be included in the main tag (`div#q-app`)
* `js` - The js script that will be included, after vue, vuex, vue-router & quasar
* `vuex` - Configuration passed to vuex
* `vue_router` - Configuration passed to vue-router
* `vue` - Configuration passed to vue


## Layouts

Examples of using layouts:

```html
{% extends 'quasar/layout.html' %}
```

## Links

An example of using block links, below we add material icons. By default it doesn't come with an icon, so you have to add it yourself.

```html
{% block links %}
<link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons" rel="stylesheet" type="text/css">
{% endblock %}
```

## Content

An example of using block content:

```html
{% block content %}
<q-toolbar class="text-primary">
    <q-btn flat round dense icon="menu" ></q-btn>
    <q-toolbar-title>
    Toolbar
    </q-toolbar-title>
    <q-btn flat round dense icon="more_vert" ></q-btn>
</q-toolbar>
{% endblock %}
```

## Vue

Examples of using vue:

```html
{% block content %}
<q-toolbar class="text-primary">
    <q-btn flat round dense icon="menu" @click="active = !active"></q-btn>
    <q-toolbar-title>
    Is this active? <{ active }>
    </q-toolbar-title>
    <q-btn flat round dense icon="more_vert" ></q-btn>
</q-toolbar>
{% endblock %}
{% block vue %}
data() {
    return {
        active: false
    }
},
{% endblock %}
```

In the example above, there are several explanations. See below:

* We add `data` to vue via the `vue block`
* We also change the vue delimiter to `<{`, `}>`

# Quasar

If you use this, you can't use the self-closing tag. See here https://quasar.dev/start/umd#usage
