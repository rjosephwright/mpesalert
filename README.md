mpesalert
=========
This is a Django application which includes most of its functionality in a management command called sender.py. Its purpose is to send alerts
when someone has sent a transaction to a Paybill number. The sender does everything via a scraper, by logging into Safaricom's management
interface for customers with a Paybill number. The login is configurable through the Django admin UI. Thus, the admin UI is exposed to the end user,
with the end user being a customer who has a Paybill number.
