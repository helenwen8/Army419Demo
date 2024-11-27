// const loggedInUserDODID = "{{ current_user.id }}";

function fetchLoanedItems(loggedInUserDODID, sort="borrowID", order="asc") {
    fetch(`/api/supply/loaned?userid=${loggedInUserDODID}&sort=${sort}&order=${order}`)
        .then(response => response.json())
        .then(data => {
            console.log('dataaaa', data)
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


function fetchBorrowedItems(loggedInUserDODID, sort="borrowID", order="asc") {
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

function sortTableHelper(header) {
    const column = header.getAttribute("column");
    console.log(column);
    const currentOrder = header.className;
    // if descending OR none, flip to ascending
    const newOrder = currentOrder === "sort-asc" ? "desc" : "asc";

    // make all table headers NONE
    header.parentNode.childNodes.forEach(sibling => {sibling.className = ""});

    // Update order attribute for the current selected column
    header.className = "sort-".concat(newOrder);
    console.log(header.className);

    // return items needed to sort
    return [column, newOrder];
}

function sortLoanedTable(header) {
    let [column, newOrder] = sortTableHelper(header);

    // Fetch sorted data
    fetchLoanedItems(loggedInUserDODID, column, newOrder);
}

function sortBorrowedTable(header) {
    let [column, newOrder] = sortTableHelper(header);

    // Fetch sorted data
    fetchBorrowedItems(loggedInUserDODID, column, newOrder);
}


// funnily enough borrow table also uses the id supplytable
// so we will just reuse this function......
function searchLoaned() {
    var input = document.getElementById("searchLoanedInput");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("supplyTable");
    var tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td");

        // make sure at least one field matches
        var flag = false;
        for (var j = 0; j < td.length; j++) {
            var txtValue = td[j].textContent || td[j].innerText;

            if (txtValue && txtValue.toUpperCase().indexOf(filter) > -1) {
              flag = true; // keep
            }
        }
        if (flag) {
            tr[i].style.display = "";
            
        } else {
            tr[i].style.display = "none";
        }
    }
}
