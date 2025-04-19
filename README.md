# NUS Taekwondo Attendance App

## Description

This application aims to streamline the attendance taking process for the NUSTKD EXCO, by automating the following steps:

1. Attendance recording for club members and de-duplication of entries.
2. Export of training attendance to Telegram.
3. Export of training attendance to attendance Excel sheet on Google Drive.

[Link to Application (Hosted on Heroku)](https://nustkd-attendance-app-e897e90f665b.herokuapp.com/)

### Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

## Features and Usage

### Add Attendance

1. Enter member's name into the input field.
   **Guidelines for name entry:**
   a. Names can be entered in either upper or lower case.
   b. Insert spaces in the name as necessary (e.g., for Chinese names).
   c. Do not enter the member's self-given English name.

2. Click on the member's status accordingly (Regular Student/Alumni/Exchange Student).

3. Click **Submit**.

### Get Current Training Date's Attendance

1. Click on **Get Today's Attendance**.

2. If the member's attendance is added/registered, then they should appear on the page.

### Export Attendance to Telegram

1. Click on **Export Attendance**.

2. Enter the day of the month to export attendance for.

3. Click on **Export to Telegram**.

4. A formatted message of attendees for the specified training date should be sent to the Telegram chat.

### Export Attendance to Excel Sheet (Google Drive)

1. Click on **Export Attendance**.

2. Enter the day of the month to export attendance for.

3. Click on **Export to Excel**.

4. Training attendance should be added to the attendance Excel sheet on Google Drive. Verify this by ensuring that the Excel sheet is updated correctly.
