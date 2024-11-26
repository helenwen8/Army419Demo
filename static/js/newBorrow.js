const apiItemURL = "/api/supplybyidentifier";
const apiBorrowerURL = "/api/users";
// const lender = lenderDODID; // Injected from Flask
let debounceTimeout;

// Function to fetch dropdown data
async function fetchDropdownData(url, query, optionsDiv) {
    try {
        const response = await fetch(`${url}?identifier=${query}`);

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

        option.setAttribute("data-id", item.ID || item.DODID); // Store ID/DODID
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
    inputField.value = option.textContent; // Set the display text in the input
    inputField.setAttribute("data-id", option.getAttribute("data-id")); // Store the actual ID in data-id
    console.log(option.getAttribute("data-id"))
    inputField.parentElement.querySelector(".dropdown-options").classList.remove("show"); // Hide the dropdown
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
