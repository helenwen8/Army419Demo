function fetchLoanedItems() {
    fetch("/api/supply/loaned?userid=6028029736")
        .then(response => response.json())
        .then(data => {
            const supplyTableBody = document.getElementById("supplyTable").querySelector("tbody");
            supplyTableBody.innerHTML = ""; // Clear the table before adding new data

            data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.LastName || ""}</td>
                    <td>${item.FirstName || ""}</td>
                    <td>${item.DODID || ""}</td>
                    <td>${item.NSN || ""}</td>
                    <td>${item.Name || ""}</td>
                    <td>${item.Serial_Num || ""}</td>
                    <td>${item.Count || ""}</td>
                    <td>${item.Checkout_Date || ""}</td>
                    <td>${item.Last_Renewed_Date || ""}</td>
                    <td></td>
                `;
                supplyTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching loaned items:", error);
        });
}

function fetchBorrowedItems() {
    fetch("/api/supply/borrowing?userid=6028029736")
        .then(response => response.json())
        .then(data => {
            const supplyTableBody = document.getElementById("supplyTable").querySelector("tbody");
            supplyTableBody.innerHTML = ""; // Clear the table before adding new data

            data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.LastName || ""}</td>
                    <td>${item.FirstName || ""}</td>
                    <td>${item.DODID || ""}</td>
                    <td>${item.NSN || ""}</td>
                    <td>${item.Name || ""}</td>
                    <td>${item.Serial_Num || ""}</td>
                    <td>${item.Count || ""}</td>
                    <td>${item.Checkout_Date || ""}</td>
                    <td>${item.Last_Renewed_Date || ""}</td>
                    <td></td>
                `;
                supplyTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching borrowed items:", error);
        });
}
