// api connection 

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";


const paymentLinkToken = new URLSearchParams(
    window.location.search
).get("token");


const productName = document.getElementById("product-name");
const productDescription = document.getElementById("product-description");
const productPrice = document.getElementById("product-price");
const checkoutForm = document.getElementById("checkout-form");
const paymentStatus = document.getElementById("payment-status");
const payButton = document.getElementById("pay-button");


//  function for loadig  payment link 
async function loadPaymentLink() {
    if (!paymentLinkToken) {
        productName.textContent = "Payment link missing";
        productDescription.textContent =
            "Please open the checkout using a valid payment link.";
        payButton.disabled = true;
        return;
    }

    try {
         const response = await fetch(
            `${API_BASE_URL}/payment-links/${paymentLinkToken}` 
         );


             if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Unable to load payment link");
    }