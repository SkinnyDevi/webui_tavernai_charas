# A TavernUI Character extension for oobabooga's Text Generation WebUI

This extension features a character searcher, downloader and manager for any TavernAI
cards.

## General features
- Main page recent and random cards, as well as random categories upon main page launch
- Card filtering with text search, NSFW blocking* and category filtering
- Card downloading
- Card contents previewing
- Offline card manager
- Search and delete downloaded cards

**Disclaimer: As TavernAI is a community supported character database, characters may often be mis-categorized, or may be NSFW when they are marked as not being NSFW.*

This extension was made for [oobabooga's text generation webui](https://github.com/oobabooga/text-generation-webui).

## Installation
You need a little bit of coding knowldge (close to none, but the more the better).

If you used a 'one-click-installer', open the `CMD_FLAGS.txt` file inside your installation folder.

To activate the extension, you must add the following to an existing line or new line (if no other startup flags are used):
```
--extensions webui_tavernai_charas
```

With this, the extension activates and you will see upon restart of the WebUI a new section with the extension contents.

For more information on how to install and activate users, please refer to the [original documentation by oobaboga](https://github.com/oobabooga/text-generation-webui/blob/main/docs/Extensions.md)

## Support me!
This extension takes some time to make, and I love working on it and fixing it for the community.

Want to support my development? Donate me over [Paypal](https://paypal.me/skinnydevi)!

## Extension screenshots

Main extension page with recent and random cards
![MainSection](https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/docs/main-online.png)

Search online TavernAI cards
![CardSearcher](https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/docs/main-searcher.png)

Advanced search filtering with card categories
![SearcherCategories](https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/docs/searcher-categories.png)

Card previews from the card's image URL
![CardPreviewing](https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/docs/card-previewer.png)

Manage your offline cards
![OfflineCardManager](https://raw.githubusercontent.com/SkinnyDevi/webui_tavernai_charas/master/docs/offline-cards.png)


## Changelog

### [1.3.1]
Fixes:
* Fixes issue [#10](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/10) where temp folder wasn't being checked if it was created. Discovered by [@lisea2017](https://github.com/lisea2017) and [@Gamefriend996](https://github.com/Gamefriend996). Thank you for the support!

Additional:
* Added a [donate](https://paypal.me/skinnydevi) button below extension version.

### [1.3.0]
Features:
- Implements a recent preview dropdown list in the Card Preview tab (suggested by [@TheInvisibleMage](https://github.com/TheInvisibleMage) in issue [#7](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/7)). Thank you for the suggestion!

Fixes:
* Resolves a styling issue with the loader bar in the download notification.

<details>

<summary>
<h3>Past changelog</h3>
</summary>

### [1.2.4]
Fixes:
* Resolves issue [#8](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/8) and [#9](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/9) discovered by [@drago87](https://github.com/drago87). Thanks for the support!
* Works correctly with the latest version of text-generation-webui (29/01/2024)

### [1.2.3]
Fixes:
* Fixed some styling issues within the extension

### [1.2.2]
Fixes:
* Updated to the latest WebUI
* Patched errors related to removed functions

### [1.2.1]
Features:
- Added a search bar to search for categories in the Online Character Search tab

Fixes:
* Implemented a check for fixing disparity between the local extension's version and the local config's last recorded version

### [1.1.1]
Features:
* Implemented an update checker that displays a button inside the Downloaded Characters' tab, allowing the user to download and install the update with one click

Fixes:
* Categories in the Online Character Searcher tab now are displayed by alphabetical order

### [1.1.0]
Features:
- Added versioning
- Implemented a Card Preview tab that allows the user to preview a card's content through it's image URL. This refers to issue [#2](https://github.com/SkinnyDevi/webui_tavernai_charas/issues/2). Thank you to [@mykeehu](https://github.com/mykeehu) for the suggestion!
- Added a prompt before downloading to specify if the card wants to be previewed before downloading

Fixes:
* Split the main `charas_ui.py` file into submodules for readability
* Added a commonplace for all components
* General fixes, refactorings and improvements to the code base

</details>