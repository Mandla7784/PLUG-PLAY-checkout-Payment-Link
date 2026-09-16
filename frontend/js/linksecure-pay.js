// api connection 

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";


const paymentLinkToken = new URLSearchParams(
    window.location.search
).get("token");
