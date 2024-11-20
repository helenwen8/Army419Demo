// const loggedInUserDODID = "{{ current_user.id }}";
function fetchLoanedItems(loggedInUserDODID) {
    fetch(`/api/supply/loaned?userid=${loggedInUserDODID}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const supplyTableBody = document.getElementById("supplyTable").querySelector("tbody");
            supplyTableBody.innerHTML = ""; // Clear the table before adding new data

            data.forEach(item => {
                const row = document.createElement("tr");
                console.log(item)
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
                        <input type="text" placeholder="Initials" id="renew-initials-${item.Borrowing_ID}" />
                        <button onclick="renewItem('${item.Borrowing_ID}', '${loggedInUserDODID}')">Renew</button>
                    </td>
                `;
                supplyTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching loaned items:", error);
        });
}

function renewItem(borrowingId, loggedInUserDODID) {
    const initialsInput = document.getElementById(`renew-initials-${borrowingId}`);
    const initials = initialsInput.value.trim();
    console.log(borrowingId)
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
            borrowing_id: borrowingId,
            initials: initials
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // alert("Borrowing record successfully renewed.");
                console.log("Calling fetchLoanedItems...");
                fetchLoanedItems(loggedInUserDODID); 
            } else {
                alert(data.message || "Failed to renew the borrowing record.");
            }
        })
        .catch(error => {
            console.error("Error renewing borrowing record:", error);
            alert("An error occurred while renewing the borrowing record.");
        });
}


function fetchBorrowedItems(loggedInUserDODID) {
    fetch(`/api/supply/borrowing?userid=${loggedInUserDODID}`)
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
