new Vue({
    el: '#order_class',
    delimiters: ['[[', ']]'],
    data: {
    tasks: []
    },
    created: function() {
        const vm = this;
        axios.get('/api/')
        .then(function(response) {
        vm.tasks = response.data
        })
    }
})