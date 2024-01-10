# Food Drive Tracker
## Purpose
This is an API and web application and API
for the Church of Scientology Ventura and
it's food drive. Its purpose is to allow
Church staff members to easily check in
customers at the point of "sale".

## Structure
Its structure is as follows:
* A check-in module which will search
either a name or barcode and will return
a customer to be checked in which will
then add it to the check-in stack for
the day
* An add new customer module which is
self-explanatory. Once the customer is
added they will automatically be added
to the check-in stack
* A dashboard for the staff to see
statistics and be able to see graphs
of various demographics and values
* It will also serve as a RESTful API
so its database can be kept exactly
in line with "Pantry Trak", Food Share's
website.
* An external source will upload the
check-in stack and will also update the
database of the web app.
