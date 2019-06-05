### Delta 

# Description
Delta is a web/QR code based authentication system built using python, OpenCV and ZBar. The server will be based on flask and SQLite.

# Compatibility 
Delta is based on python; Therefore, it can run on virtually any computer system with sufficient processing power that has a webcam. 

# Explanation
Delta uses input from a webcam which feeds it into OpenCV. OpenCV analyses the video frame by frame to look for a QR code. ZBar then decodes the QR code and checks the SQL database for a user unique UUID obtained from the QR code. If there is a match, the server then checks the current status of the user. If the user is logged out, the system logs the user as ‘logged in’ then checks the current time against the 'late time’ of the school. If the user is late, the system logs the user as “late” and adds it to the record of the times the student has been late. Otherwise, the system logs the user as “logged out”. 

*Example:*
Student goes to school. The student scans his/her unique QR code at the front gate and he’s logged in. His parents are notified.
After school, the student scans the QR code once more and he’s logged out. Once again, his parent are notified.

# Features:
The Scanner runs on python so it can be used anywhere. 
The ID card can be an file or on the web.
The verifier will be on the server itself.

To do:
AES encryption for 
