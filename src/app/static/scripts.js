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
            purchases: [],
            receiptId: null,
            async init() {
                const urlParts = window.location.href.split('/');
                this.receiptId = urlParts[urlParts.length - 1];
                this.refreshPurchases(this.receiptId)
            },
            async updateItems($event) {
                if (this.name && !this.items.find(item => item.name == this.name)) {
                    this.items = (await fetchItems({ search: this.name })).items;
                }
            },
            async refreshPurchases() {
                const purchases = await fetch(`/api/receipts/${this.receiptId}/purchases`).then(response => response.json());
                this.purchases = purchases.data.purchases;
            },
            async selectItem(item) {
                await addPurchase(this.receiptId, item.id);
                this.name = '';
                this.items = [];
                await this.refreshPurchases()
            },
        };
    });
});
