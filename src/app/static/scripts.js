let datepicker_currents = document.getElementsByClassName('datepicker-current');
for (let el of datepicker_currents) {
    el.valueAsDate = new Date();
}

async function fetchItems(params) {
    let { page = 1, search = "" } = params;
    // if (search.length == 0) {
    //     return [];
    // }
    const url_params = new URLSearchParams({
        page: page,
    });
    if (search) {
        url_params.append('search', search)
    };
    items = await fetch(`/api/items?${url_params}`).then(response => response.json());
    return items.data;
}

async function addPurchase(receiptId, itemId) {
    await fetch(`/api/purchases`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            receipt_id: receiptId,
        }),
    });
}

document.addEventListener('alpine:init', () => {
    Alpine.data('itemList', () => {
        return {
            name: '',
            items: [],
            async updateItems($event) {
                if (this.name && !this.items.find(item => item.name == this.name)) {
                    this.items = (await fetchItems({ search: this.name })).items;
                }
            },
            async selectItem(item) {
                const urlParts = window.location.href.split('/');
                const receiptId = urlParts[urlParts.length - 1];
                await addPurchase(receiptId, item.id);
                this.name = '';
                this.items = [];
            },
        };
    });
});
