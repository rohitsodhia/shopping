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
            selectItem(item) {
                addPurchase(item.id);
                this.name = '';
                this.items = [];
            },
        };
    });
});
