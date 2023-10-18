function openSwapInfo() {
  const swapInfo = document.getElementsByClassName("swap-info")[0];
  swapInfo.classList.remove("d-none");
  swapInfo.classList.add("d-flex");
}

function closeSwapInfo() {
  const swapInfo = document.getElementsByClassName("swap-info")[0];
  swapInfo.classList.remove("d-flex");
  swapInfo.classList.add("d-none");
}

async function updateExchangeRequest(exchange_request_id, status) {
    console.log(exchange_request_id, status);
  
    const response = await fetch(`/exchanges/${exchange_request_id}?status=${status}`, {
      method: "PUT",
    });
  
    if (!response.ok) {
      // Handle error
      const errorMessage = await response.text();
      alert(errorMessage);
      return;
    }
  
    // Request was successful
    window.location.href = "/messages";
  }