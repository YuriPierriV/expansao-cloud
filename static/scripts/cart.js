let cart = [];

function addToCart(productId) {
    const productElement = document.querySelector(`[data-id='${productId}']`);
    const name = productElement.getAttribute('data-name');
    const price = parseFloat(productElement.getAttribute('data-price'));

    cart.push({ product_id: productId, name, price });

    renderCart();
}

function randomOrderId() {
    return Math.floor(Math.random() * 1000000);
}

function renderCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = "";

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - R$ ${item.price.toFixed(2)}`;
        cartItems.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('order-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;

        if (cart.length === 0) {
            alert("Seu carrinho está vazio!");
            return;
        }

        const order = {
            email,
            order_id: randomOrderId(),
            details: cart
        };

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(order)
            });

            const result = await response.json();

            const message = document.getElementById('message');
            if (response.ok) {
                message.innerHTML = `<h3 style="color: green;">${result.message}</h3>`;
                cart = [];
                renderCart();
                form.reset();
            } else {
                message.innerHTML = `<h3 style="color: red;">Erro: ${result.error}</h3>`;
            }

        } catch (error) {
            console.error('Erro ao enviar:', error);
        }
    });
});
