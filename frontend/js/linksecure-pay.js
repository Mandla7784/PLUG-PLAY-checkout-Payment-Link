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

let currentPaymentLink = null;


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

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Unable to load payment link");
        }

        currentPaymentLink = result;

        productName.textContent = result.product_name;

        productDescription.textContent =
            result.description || "";

        productPrice.textContent =
            `${result.currency} ${result.amount}`;

        payButton.textContent =
            `Pay ${result.currency} ${result.amount}`;

    } catch (error) {
        console.error("Payment link error:", error);

        productName.textContent = "Unable to load product";
        productDescription.textContent = error.message;

        payButton.disabled = true;
    }
}


checkoutForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!currentPaymentLink) {
        paymentStatus.textContent =
            "Payment link is not available.";
        return;
    }

    payButton.disabled = true;
    payButton.textContent = "Processing...";
    paymentStatus.textContent = "";

    try {
        const response = await fetch(
            `${API_BASE_URL}/checkout/pay`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    idempotency_key: crypto.randomUUID(),
                    payment_link_token: paymentLinkToken,

                    // Backend ignores these values
                    // and uses the payment link values.
                    amount: 0,
                    currency: "XXX"
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
           const errorMessage =
            typeof result.detail === "string"
        ? result.detail
        : JSON.stringify(result.detail);

        throw new Error(
                errorMessage || "Payment could not be created"
);
        }

        paymentStatus.textContent =
            `Payment created successfully. Status: ${result.status}`;

        payButton.textContent = "Payment Pending";

    } catch (error) {
        console.error("Payment error:", error);

        paymentStatus.textContent = error.message;

        payButton.disabled = false;

        payButton.textContent =
            `Pay ${currentPaymentLink.currency} ${currentPaymentLink.amount}`;
    }
});


loadPaymentLink();