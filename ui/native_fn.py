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


def change_and_search_preview():
    """
    Clicks on the 'Card Previewer' tab for direct card preview.
    """

    return """
    () => {
        var tabButtons = document.evaluate("//*[@id='tavernai_ext_tabs']/div[1]/button[2]", document, null, XPathResult.ANY_TYPE, null );
        var previewer = tabButtons.iterateNext();

        previewer.click();
        
        var searchBtn = document.getElementById('tavernai_preview_search_button');
        setTimeout(() => searchBtn.click(), 250);
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


def refresh_recent_preview_dropdown():
    """
    Refreshes all related information regarding downloaded characters.
    """

    return """
    () => {
        var refreshes = document.querySelectorAll(".tavernai_card_preview_refresh_recent_dropdown");
        for (let r of refreshes) {
            setTimeout(() => r.click(), 250);
        }
    }
    """


def online_search_default_page_one():
    """
    Always selects page 1 on the result dataset.
    """

    return """
    () => {
        setTimeout(() => {
            const dataset_pages = document.querySelector("#tavernai_online_search_results > div.paginate");
            
            if (dataset_pages.children.length > 0) dataset_pages.children[0].click();    
        }, 300);
    }
    """
