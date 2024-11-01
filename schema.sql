-- Create the Supply table
CREATE TABLE Supply (
    Item_UUID TEXT PRIMARY KEY,   -- Unique identifier for each item
    NSN TEXT,                     -- National Stock Number
    Description TEXT,             -- Description of the item
    Count INTEGER                 -- Number of items available
);

-- Create the User table
CREATE TABLE User (
    DODID TEXT PRIMARY KEY,       -- Unique identifier for each user (e.g., Department of Defense ID)
    Name TEXT,                    -- User's name
    Email TEXT,                   -- User's email
    Phone TEXT                    -- User's phone number
);

-- Create the Borrowing table
CREATE TABLE Borrowing (
    Item_ID TEXT,                 -- References Item_UUID in the Supply table
    Lender_DODID TEXT,            -- References DODID in the User table for the lender
    Borrower_DODID TEXT,          -- References DODID in the User table for the borrower
    Count INTEGER,                -- Number of items borrowed
    Reason TEXT,                  -- Reason for borrowing
    Checkout_Date TEXT,           -- Date of checkout
    Last_Renewed_Date TEXT,       -- Date of last renewal
    Borrower_Initials TEXT,       -- Initials of the borrower
    FOREIGN KEY (Item_ID) REFERENCES Supply (Item_UUID),
    FOREIGN KEY (Lender_DODID) REFERENCES User (DODID),
    FOREIGN KEY (Borrower_DODID) REFERENCES User (DODID)
);
