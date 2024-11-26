-- Drop tables if they exist
DROP TABLE IF EXISTS Borrowing;
DROP TABLE IF EXISTS Supply;
DROP TABLE IF EXISTS User;

-- Create the Supply table
CREATE TABLE Supply (
    ID INTEGER NOT NULL PRIMARY KEY,   -- Unique identifier for each item
    NSN INTEGER,                     -- National Stock Number
    Serial_Num VARCHAR(255),
    Name VARCHAR(255),
    Description VARCHAR(255)            -- Description of the item
);

-- Create the User table
CREATE TABLE User (
    DODID VARCHAR(255) PRIMARY KEY,       -- Unique identifier for each user (e.g., Department of Defense ID)
    FirstName VARCHAR(255),               -- Users name
    LastName VARCHAR(255),       
    Email VARCHAR(255),                   -- Users email
    Phone VARCHAR(255),                   -- Users phone number
    Password VARCHAR(255)
);

-- Create the Borrowing table
CREATE TABLE Borrowing (
    Borrowing_ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- New unique identifier
    Item_ID VARCHAR(255),                 -- References Item_UUID in the Supply table
    Lender_DODID VARCHAR(255),            -- References DODID in the User table for the lender
    Borrower_DODID VARCHAR(255),          -- References DODID in the User table for the borrower
    Count INTEGER,                -- Number of items borrowed
    Reason VARCHAR(255),                  -- Reason for borrowing
    Checkout_Date VARCHAR(255),           -- Date of checkout
    Last_Renewed_Date VARCHAR(255),       -- Date of last renewal
    Due_Date VARCHAR(255),                -- Date the item is due
    Return_Date VARCHAR(255),             -- Date the item was returned
    Borrower_Initials VARCHAR(255),       -- Initials of the borrower
    FOREIGN KEY (Item_ID) REFERENCES Supply (ID),
    FOREIGN KEY (Lender_DODID) REFERENCES User (DODID),
    FOREIGN KEY (Borrower_DODID) REFERENCES User (DODID)
);
