let cart = [];

function addToCart(id, name, price) {
    cart.push({ id, name, price });
    alert(name + " added to cart!");
    localStorage.setItem("cart", JSON.stringify(cart));
}
