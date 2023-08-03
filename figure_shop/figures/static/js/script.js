function addItem(itemId) {
    console.log(itemId);
    var url = '/service/cart/' + itemId + '/add_to_cart/';
    fetch(url, {method: 'GET', })
    .then(response => location.reload())
    .catch(error => console.error(error));
}

function deleteItem(itemId) {
    console.log(itemId);
    var url = '/service/cart/' + itemId + '/remove_from_cart/';
    fetch(url, {method: 'GET', })
    .then(response => location.reload())
    .catch(error => console.error(error));
}

