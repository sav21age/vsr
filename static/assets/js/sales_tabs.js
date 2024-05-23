const triggerTabList = document.querySelectorAll('#salesTabs a');
if (triggerTabList.length) {
    triggerTabList.forEach(triggerEl => {

        const tabTrigger = new bootstrap.Tab(triggerEl);

        triggerEl.addEventListener('click', event => {

            event.preventDefault();
            tabTrigger.show();

            // save tab target
            localStorage.setItem('active-tab', event.target.getAttribute('href'));

        });
    });

    // get the active tab id, set default
    const activeTabId = localStorage.getItem('active-tab') || '#discount';

    console.log(activeTabId);

    // find the element that triggers the tab
    const activeTab = [...triggerTabList].find(el => el.getAttribute('href') === activeTabId);

    // click the element to trigger the tab
    // in case it's not found, click the first tab
    if (activeTab) {
        activeTab.click();
    } else {
        triggerTabList[0].click();
    }
}