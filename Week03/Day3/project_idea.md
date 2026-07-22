I want to build an application that helps car owners organize all maintenance invoices in one place because paper invoices are easy to lose.

Users should be able to register multiple cars, each with its make, model, year, VIN number, and current mileage. Every maintenance invoice should include the service center, service date, total cost, performed services, replaced parts, and an uploaded photo or PDF of the invoice.

The system should automatically calculate the total maintenance cost for each vehicle and display the maintenance history in chronological order. It should also remind users about upcoming maintenance based on mileage or date, such as oil changes or tire replacement.

In the future, I would like to use OCR and AI to extract information automatically from uploaded invoices instead of entering everything manually. The application could also classify maintenance types and estimate future maintenance costs.

The project will use Python for the backend, SQLite for the database, and a simple interface. Uploaded invoices should be stored separately from the database.

Users should not be allowed to save invoices without selecting a vehicle, and the total cost should always be greater than zero.