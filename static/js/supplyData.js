// const loggedInUserDODID = "{{ current_user.id }}";

function fetchLoanedItems(loggedInUserDODID, sort="", order="") {
    fetch(`/api/supply/loaned?userid=${loggedInUserDODID}&sort=${sort}&order=${order}`)
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
                    <td>${item.Due_Date || ""}</td>
                    <td>${item.Return_Date || ""}</td>
                    <td>
                        <input type="text" placeholder="Initials" id="renew-initials-${item.borrowID}" />
                        <button onclick="renewItem('${item.borrowID}', '${loggedInUserDODID}')">Renew</button>
                    </td>
                    <td>
                        <input type="text" placeholder="Initials" id="return-initials-${item.borrowID}" />
                        <button onclick="returnItem('${item.borrowID}', '${loggedInUserDODID}')">Process Return</button>
                    </td>
                `;
                supplyTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching loaned items:", error);
        });
}

function returnItem(borrowingId, loggedInUserDODID) {
    const initialsInput = document.getElementById(`return-initials-${borrowingId}`);
    const initials = initialsInput.value.trim();
    console.log(borrowingId)
    if (!initials) {
        alert("Please enter your initials.");
        return;
    }

    fetch(`/api/supply/return`, {
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
                // alert("Borrowing record successfully returned.");
                console.log("Calling fetchLoanedItems...");
                fetchLoanedItems(loggedInUserDODID);
            } else {
                alert(data.message || "Failed to return the borrowing record.");
            }
        })
        .catch(error => {
            console.error("Error returning borrowing record:", error);
            alert("An error occurred while returning the borrowing record.");
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


function fetchBorrowedItems(loggedInUserDODID,sort="", order="") {
    fetch(`/api/supply/borrowing?userid=${loggedInUserDODID}&sort=${sort}&order=${order}`)
        .then(response => response.json())
        .then(data => {
            console.log(loggedInUserDODID)
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


function sortTable(header) {
    const column = header.getAttribute("column");
    const currentOrder = header.className;
    console.log(column);
    console.log(currentOrder);
    const newOrder = currentOrder === "sort-asc" ? "desc" : "asc";

    // Update order attribute
    header.className = "sort-" + newOrder;

    // Fetch sorted data
    fetchBorrowedItems(loggedInUserDODID, column, newOrder);
}