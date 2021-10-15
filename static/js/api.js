function getCsrfToken() {
    const csrfTokenInput = document.querySelector("input[name='csrfmiddlewaretoken']")
    const csrfToken = csrfTokenInput.value
    return csrfToken
}

const getHeaders = () => new Headers({
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken(),
})

async function fetcher(url, data, method) {
    const response = await fetch(url, {
        method: method,
        body: JSON.stringify(data),
        headers: getHeaders(),
    })
    const json_response = await response.json()
    if(!json_response.id) {
        return {errors: json_response}
    }
    return json_response
}


function apiPrototype(base_url) {
    return {
        url: base_url,
        async get() {
            const response = await fetch(this.url)
            const json_response = await response.json()
            return json_response
        },
        async getOne(object_id) {
            const response = await fetch(`${this.url}${object_id}/`)
            const json_response = await response.json()
            return json_response
        },
        async update(object_id, data) {
            const errors = this.validators.validateUpdate(data)
            if(!Object.entries(errors).length) {
                const response = await fetcher(`${this.url}${object_id}/`, data, "PUT")
                return response
            }
            return errors
        },
        async create(data) {
            const errors = this.validators.validateCreate(data)
            if(!Object.entries(errors).length) {
                const response = await fetcher(`${this.url}`, data, "POST")
                return response
            }
            return errors
        },
        validators: {
            validateUpdate (data) {
                return {}
            },
            validateCreate (data) {
                return {}
            },
        }
    }
} // end function


function buildApi() {
    return {
        products: {
            ...apiPrototype("/api/inventory/product/")
        },
        sales: {
            ...apiPrototype("/api/sales/sale/"),
        }
    } // end object
} // eend function

const api = buildApi()