async function fetchPrices() {
    try {
        const res = await fetch("/prices");
        const data = await res.json();
        if (data.gold && data.silver) {
            document.getElementById("gold").innerText = data.gold.toFixed(2);
            document.getElementById("silver").innerText = data.silver.toFixed(2);
            document.getElementById("sp500").innerText = data.sp500.toFixed(2);
        }
    } catch (err) {
        console.error("Error fetching prices", err);
    }
}

fetchPrices();
setInterval(fetchPrices, 10000);
