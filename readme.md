# Attendance Reporting Application

The Attendance Reporting Application is a powerful tool designed to generate attendance reports for employees. It provides the capability to filter reports based on employee identification numbers and specific date ranges. The application consists of two main sections, each serving a specific purpose.

## Data Fetching Section

The first section of the application is responsible for fetching data from both the fingerprint and ERP (Enterprise Resource Planning) databases. To optimize performance, a cron job has been implemented to regularly retrieve the data. This approach ensures that the application runs smoothly and efficiently, even with large amounts of data.

## Reporting API Section

The second section of the application is an API that generates three types of reports: general reports, normal late reports, and absence reports. These reports are generated based on the employee details fetched from the ERP database. The API incorporates submitted absences to provide comprehensive attendance information.

To ensure security and restrict unauthorized access, the API utilizes JSON Web Token (JWT) authentication. This authentication mechanism guarantees that only authorized users can access the API and generate reports.

## Usage

1. Set up the necessary database connections for the fingerprint and ERP databases.

2. Configure the cron job to fetch data from the databases periodically.

3. Securely deploy the application and ensure that it is accessible to authorized users.

4. Access the API endpoints to generate attendance reports based on specific employee identification numbers and date ranges.

## Dependencies

The Attendance Reporting Application relies on the following technologies and frameworks:

- Cron job for data fetching
- JSON Web Token (JWT) for authentication
- Database connections to the fingerprint and ERP databases

Ensure that these dependencies are properly installed and configured before running the application.

## Contributing

Contributions to the Attendance Reporting Application are welcome! If you have any suggestions, enhancements, or bug fixes, feel free to open an issue or submit a pull request.
