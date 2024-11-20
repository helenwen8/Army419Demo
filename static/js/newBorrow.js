const apiItemURL = "/api/supplybyidentifier";
const apiBorrowerURL = "/api/users";
const lenderDODID = "{{ current_user.id }}"; // Injected from Flask
let debounceTimeout;

// Function to fetch dropdown data
async function fetchDropdownData(url, query, optionsDiv) {
    try {
        const response = await fetch(`${url}?query=${query}`);
        const data = await response.json();
        renderOptions(data, optionsDiv);
    } catch (error) {
        console.error("Error fetching data:", error);
        optionsDiv.innerHTML = '<div class="dropdown-option">Failed to load options</div>';
    }
}

// Function to render dropdown options
function renderOptions(data, optionsDiv) {
    optionsDiv.innerHTML = ""; // Clear existing options
    if (data.length === 0) {
        optionsDiv.innerHTML = '<div class="dropdown-option">No options found</div>';
        return;
    }
    data.forEach(item => {
        const option = document.createElement("div");
        option.classList.add("dropdown-option");

        if (item.Name) {
            option.textContent = `Name: ${item.Name}`;
        } else if (item.DODID) {
            option.textContent = `DODID: ${item.DODID}`;
        } else {
            option.textContent = `Serial: ${item.Serial_Num}`;
        }

        option.setAttribute("data-id", item.id || item.DODID); // Store ID/DODID
        option.onclick = () => selectOption(option, optionsDiv.parentElement.querySelector("input"));
        optionsDiv.appendChild(option);
    });
}

// Debounced fetch function for dropdowns
function debouncedFetch(url, inputId, optionsDivId) {
    const query = document.getElementById(inputId).value;
    const optionsDiv = document.getElementById(optionsDivId);

    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
        fetchDropdownData(url, query, optionsDiv);
    }, 300);
}

// Item-specific fetch and rendering
function debouncedItemFetch() {
    debouncedFetch(apiItemURL, "item-search", "item-options");
}

// Borrower-specific fetch and rendering
function debouncedBorrowerFetch() {
    debouncedFetch(apiBorrowerURL, "borrower-search", "borrower-options");
}

// Handle option selection
function selectOption(option, inputField) {
    inputField.value = option.textContent; // Set selected value in input
    inputField.setAttribute("data-id", option.getAttribute("data-id")); // Store selected ID
    inputField.parentElement.querySelector(".dropdown-options").classList.remove("show");
}

// Toggle dropdown visibility
function toggleDropdown(show, optionsDivId) {
    const optionsDiv = document.getElementById(optionsDivId);
    if (show) {
        optionsDiv.classList.add("show");
    } else {
        optionsDiv.classList.remove("show");
    }
}

// Submit form data
function submitForm() {
    const item = document.getElementById("item-search").value;
    const borrower = document.getElementById("borrower-search").value;
    const count = document.getElementById("count").value;
    const date = document.getElementById("date").value;
    const initials = document.getElementById("initials").value;

    const data = {
        item: item,
        lender: lenderDODID,
        borrower: borrower,
        count: parseInt(count),
        reason: document.getElementById("reason").value,
        date: date,
        initials: initials
    };

    fetch("/api/borrow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseMessage").innerText = data.message;
            document.getElementById("supplyForm").reset();
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("responseMessage").innerText = "An error occurred.";
        });
}

// Attach events
window.onload = () => {
    fetchDropdownData(apiItemURL, "", document.getElementById("item-options")); // Initial item data
    fetchDropdownData(apiBorrowerURL, "", document.getElementById("borrower-options")); // Initial borrower data
};

document.getElementById("item-search").addEventListener("focus", () => {
    toggleDropdown(true, "item-options");
});

document.getElementById("borrower-search").addEventListener("focus", () => {
    toggleDropdown(true, "borrower-options");
});

document.getElementById("item-search").addEventListener("input", debouncedItemFetch);
document.getElementById("borrower-search").addEventListener("input", debouncedBorrowerFetch);

window.addEventListener("click", (event) => {
    if (!document.querySelector("#item-search").parentElement.contains(event.target)) {
        toggleDropdown(false, "item-options");
    }
    if (!document.querySelector("#borrower-search").parentElement.contains(event.target)) {
        toggleDropdown(false, "borrower-options");
    }
});
