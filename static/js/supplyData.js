// const loggedInUserDODID = "{{ current_user.id }}";
function fetchLoanedItems(loggedInUserDODID) {
    fetch(`/api/supply/loaned?userid=${loggedInUserDODID}`)
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
                    <td>
                        <input type="text" placeholder="Initials" id="renew-initials-${item.Serial_Num}" />
                        <button onclick="renewItem('${item.Serial_Num}')">Renew</button>
                    </td>
                `;
                supplyTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching loaned items:", error);
        });
}

function renewItem(serialNum) {
    const initialsInput = document.getElementById(`renew-initials-${serialNum}`);
    const initials = initialsInput.value.trim();

    if (!initials) {
        alert("Please enter your initials.");
        return;
    }

    fetch(`/api/supply/renew`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            serial_num: serialNum,
            initials: initials
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Item successfully renewed.");
                fetchLoanedItems(); // Refresh the table
            } else {
                alert(data.message || "Failed to renew the item.");
            }
        })
        .catch(error => {
            console.error("Error renewing item:", error);
            alert("An error occurred while renewing the item.");
        });
}

function fetchBorrowedItems() {
    fetch("/api/supply/borrowing?userid=${loggedInUserDODID}")
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
