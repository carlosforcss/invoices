var app = new Vue({
    el: '#saleController',
    delimiters: ['[[', ']]'],
    data: {
        message: 'Hello Vueee!',
        products: [],
        sales: [],
        selectedProduct: null,
        quantity: 1,
        newSale: {
            products: [],
            value: 0,
            discount: false,
        },
        errors: [],
        _products_urls: "/api/inventory/product/",
    },
    methods: {
        getTotal: function() {
            let total_in_lines = 0
            this.newSale.products.forEach(product => total_in_lines += product.value * product.quantity)
            if(this.newSale.discount) {
                total_in_lines -= total_in_lines * 0.30
            }
            return total_in_lines
        },
        selectProduct: function (selectedProduct) {
            this.selectedProduct = selectedProduct
        },
        addSelectedProduct: function () {
            if(this.selectedProduct) {
                this.newSale.products.push({...this.selectedProduct, quantity: this.quantity, total: this.quantity * this.selectedProduct.value})
                this.newSale.value += this.selectedProduct.value * this.quantity
                this.selectedProduct = null
                this.quantity = 1
            }
        },
        createSale: async function () {
            const lines = new Array()
            this.errors = []
            this.newSale.products.forEach(function (product) {
                lines.push({product: product.id, quantity: product.quantity})
            })
            const response = await api.sales.create({...this.newSale, lines: lines})
            if(response.id) {
                const successNotification = Toastify({
                    text: "Invoice created successfully.",
                    duration: 4000,
                })
                successNotification.showToast()
                this.newSale.products = []
                this.newSale.value = 0
                this.discount = null
                return null;
            }
            this.errors = response.errors.non_field_errors
        },
    },
    async mounted() {
        const products_response = await api.products.get()
        this.products = products_response
        this.products.forEach(product => product.quantity = 0)
    }
})
