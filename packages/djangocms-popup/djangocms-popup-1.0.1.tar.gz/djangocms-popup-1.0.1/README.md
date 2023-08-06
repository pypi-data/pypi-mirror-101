<div align="center">
<img src="https://gitlab.com/kapt/open-source/djangocms-popup/uploads/40864e2cc6b7a882a4412048fac46103/image.png" alt="DjangoCMS-popup" />
</div>

## Install

1) Install module
   ```
   python3 -m pip install djangocms-popup
   ```

2) Add it to your INSTALLED_APPS
   ```
       'djangocms_popup',
   ```

3) Launch your django-cms site, it should be here!

![](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/5bbbc877a1e68a440852f390c2259152/image.png)

### Requirements

* `django-cms`: Obviously
* `django-sekizai`: Only for the template. *So you can uninstall it if you create your own templates.*

## Features

### A popup

![DjangoCMS-popup demo](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/bb3f075066cbedcf4918c3fe2eaf554a/djangocms-popup.webm)

### An Admin list of popups that you can access from a button in your taskbar

![DjangoCMS-popup demo list](https://gitlab.com/kapt/open-source/djangocms-popup/uploads/681ab27b24dfc5c16b051589aec5725a/djangocms-popup-list.webm)

## Configuration

* `DJANGOCMS_POPUP_ADD_LIST_BUTTON` (default is `True`): Disable this setting to disable the button in the toolbar.

## Customize it!

The template included in this project serves demonstration purpose only, it's up to you to integrate it into your graphic charter by creating a file in `templates/popup/popup_plugin.html`.

## How it works

It's a classic djangocms-plugin, with all the stuff in `admin.py`, `cms_plugins.py`, `cms_toolbars.py` and `models.py`.

The "fun" part is in the template.

The child plugins will be rendered inside a div which have a `visibility` property (see [MDN doc](https://developer.mozilla.org/en-US/docs/Web/CSS/visibility)).

Then, a _very_ dumb script (in vanilla javascript) will display the div with a delay using `setTimeout`, and will add an event listener on a small button (that will show/hide the popup when clicked).

If the option "*Allow the popup to be reopened if it is closed*", the small button will still be visible, even if you refresh the page.

The state of the popup is stored inside the localStorage (the id is `popup_is_open_{{ instance.id }}`), so a closed popup won't reopen at a page reload.

*Warning!* The plugin uses the `visibility` property! So if any of the plugins you put inside the popup have a `visibilit: visible` property it will be shown!
