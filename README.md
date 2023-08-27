# A TavernUI Character extension for oobabooga's Text Generation WebUI

This extension features a character searcher, downloader and manager for any TavernAI
cards.

## General features
- Main page recent and random cards, as well as random categories upon main page launch
- Card filtering with text search, NSFW blocking* and category filtering
- Card downloading
- Offline card manager
- Search and delete downloaded cards

**Disclaimer: As TavernAI is a community supported character database, characters may often be mis-categorized, or may be NSFW when they are marked as not being NSFW.*

This extension was made for [oobabooga's text generation webui](https://github.com/oobabooga/text-generation-webui).

## Installation
You need a little bit of coding knowldge (close to none, but the more the better).

If you used a 'one-click-installer', open the `webui.py` file inside your installation folder. Near the top of the file, you should see some text (variable) containing the words 'CMD_FLAGS = ' + some other stuff. 

To activate the extension, you must add the following to that variable:
```py
CMD_FLAGS = "--extensions webui_tavernai_charas"
```

With this, the extension activates and you will see upon restart of the WebUI a new section with the extension contents.

For more information on how to install and activate users, please refer to the [original documentation by oobaboga](https://github.com/oobabooga/text-generation-webui/blob/main/docs/Extensions.md)

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

### [1.1.0]
Features:
- Added versioning
- Implemented a Card Preview tab that allows the user to preview a card's content through it's image URL
- Added a prompt before downloading to specify if the card wants to be previewed before downloading

Fixes:
* Split the main `charas_ui.py` file into submodules for readability
* Added a commonplace for all components
* General fixes, refactorings and improvements to the code base