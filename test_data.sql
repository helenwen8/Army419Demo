INSERT INTO 
Supply (NSN, Name, Serial_Num, Description) 
VALUES (Null, 'OCCS', Null, Null),
    (Null, Null, '26081663', Null),
    (Null, 'Battery', Null, Null),
    (Null, Null, '25778138', Null),
    (Null, Null, '25780882', Null),
    (Null, 'OCCS Charger', Null, Null),
    (Null, 'Foldable Tables', Null, Null),
    (Null, 'Protractor', Null, Null),
    (Null, 'White Board', Null, '10 by 10 white board'),
    (6910123888071, 'Weapons Effect Signature Simulator', '1322A125', 'DA DVC 01-2561/1'),
    (586812451, 'Tube Launcher', Null, Null),
    (72193006600, 'Backpack', Null, 'Green');

INSERT INTO 
User (DODID, FirstName, LastName, Email, Phone) 
VALUES (6246120335, 'Joseph', 'Mayo', 'scott@army.com', '7225265193'),
    (6028029736, 'Scott', 'Clancy', 'joseph@army.com', '5185207573'),
    (5124865241, Null, 'Sauls', 'sauls@army.com', '8798190633'),
    (8815194770, 'Eric', 'Chambers', 'eric@army.com', '5253009893'),
    (8817346652, 'Devin', 'Irelan', 'devin@army.com', '6751060212');

INSERT INTO 
Borrowing (Item_ID, Lender_DODID, Borrower_DODID, Count, Reason, Checkout_Date, Last_Renewed_Date, Borrower_Initials) 
VALUES (1, 6028029736, 5124865241, 1, 'Need to use', '09/26/2024', '09/26/2024', Null ),
(3, 6028029736, 8815194770, 1, 'Need to switch batteries', '10/27/2024', '11/27/2024', Null ),
(2, 8817346652, 6028029736, 2, Null, '09/26/2023', '10/26/2023', Null ),
(4, 6028029736, 8815194770, 1, Null, '09/26/2023', '10/26/2023', Null ),
(5, 6246120335, 6028029736, 5, Null, '09/26/2023', '10/26/2023', Null ),
(6, 6028029736, 8817346652, 3, Null, '09/26/2023', '10/26/2023', Null ),
(7, 6028029736, 8817346652, 1, Null, '09/26/2023', '10/26/2023', Null );







-- API notes:
-- insert or update
-- if you insert the same item (the NSN), it should just increase the count

-- if inserting the same DODID, show error
