def change_tab():
    """
    Clicks on the 'Text generation' tab for direct usage upon character selection.
    """

    return """
    () => {
        var tabButtons = document.evaluate("//button[contains(., 'Text generation')]", document, null, XPathResult.ANY_TYPE, null );
        var chatTab = tabButtons.iterateNext();

        chatTab.click();
    }
    """


def hit_all_refreshes():
    """
    Refreshes all online carousels.
    """

    return """
    () => {
        var refreshes = document.querySelectorAll(".tavernai_slider_refresh");
        setTimeout(() => {
            for (let r of refreshes) {
                setTimeout(() => r.click(), 250);
            }
        }, 500)
    }
    """


def refresh_downloaded():
    """
    Refreshes all related information regarding downloaded characters.
    """

    return """
    () => {
        var refreshes = document.querySelectorAll(".tavernai_refresh_downloaded_charas");
        for (let r of refreshes) {
            setTimeout(() => r.click(), 250);
        }
    }
    """
