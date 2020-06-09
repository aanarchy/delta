# Delta
Delta is a web/QR code based authentication system built using python, imutils and ZBar. The server will be based on flask and SQLAlchemy. Multi connection sockets are implemented using selectors.

## Compatibility
Delta is based on python; Therefore, it can run on virtually any computer system with sufficient processing power that has a webcam.

## Explanation
Delta uses input from a webcam which is provided by imutils. Zbar analyses the video frame by frame to look for a QR code. The data is then decoded. The client checks the SQL database for a user unique UUID obtained from the QR code. If there is a match, the server then checks the current status of the user. If the user is logged out, the system logs the user as ‘logged in’ then checks the current time against the 'late time’ of the school. If the user is late, the system logs the user as “late” and adds it to the record of the times the student has been late. Otherwise, the system logs the user as “logged out”.

## Features:
The Scanner runs on python so it can be used anywhere.
The ID card can be an file or on the web.
The verifier will be on the server itself.

## To do:
- Possibly implement continuous multi connections by offloading some input checks on client instead of the server.
- Use UUIDs instead of simple numbers
- Replace local sockets with API
- Possibly replace SQLAlchemy with NoSQL databases (Redis & MongoDB)
