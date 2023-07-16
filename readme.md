
# Attendance Reporting Application 

This application is designed to generate attendance reports , which can be filtered based on employee identification numbers, as well as specific date ranges.The application is divided into two sections. 

The first section is responsible for fetching data from both the fingerprint and ERP databases.This task is performed by a cron job, which was implemented to enhance the application's performance, as directly fetching the data would cause the application to run slowly.

The second section is an API that generates three types of reports: general, normal late, and absence reports. The employee details are fetched from the ERP database, and submitted absences are included in the report.

Additionally, this application uses JSON Web Token (JWT) for authentication to secure the API and restrict access to authorized users only.
