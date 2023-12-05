## Django Multi Marketplace App

The all is a sophisticated marketplace app built using Django, catering to two distinct user groups: cafe shoppers and clients. The app provides an interactive platform where cafe shoppers can add coffees, and clients can make purchases using the Stripe payment gateway.

## Overview

- **User Groups:** The app accommodates two primary user groups: cafe shoppers and clients, each with distinct functionalities.

- **Coffee Management:** Cafe shoppers can add new coffees to the marketplace, showcasing a variety of offerings.

- **Stripe Integration:** Clients can make purchases securely using the Stripe payment gateway, ensuring a reliable and seamless payment experience.

- **Authentication and Authorization:** User authentication and authorization are implemented using the default Django auth session and Google OAuth2, enhancing security and user trust.

- **Email Notifications with Celery:** Celery is utilized to send emails, providing an asynchronous and efficient method for handling email notifications.

- **Geolocation Services:** Geolocation services are implemented to obtain client longitude/latitude. The Haversine algorithm is used to determine the nearest coffee shop, enhancing the user experience.

- **Custom Context Processors:** Custom context processors are employed to enhance the user experience by providing functionalities like fetching coffee information and cart details.

- **Database Optimization:** The app can be tweaked to use two databases, one for reading and another for writing, optimizing database operations.

- **Redis Caching:** Redis is used for caching in certain sections, improving performance and responsiveness.

## Project Structure
```plaintext
/dmvc
|-- cat
|-- coffee
|-- docker-compose.yml
|-- orders
|-- templates
|-- venv
|-- bazaar
|-- clients
|-- core
|-- dockerfile
|-- manage.py
|-- requirements.txt
|-- users
```

## Getting Started
1. Explore the Django app structure, including models, views, and templates.
2. Run the application using `python manage.py runserver`.
3. Test the functionalities related to adding coffees, making purchases, and other marketplace features.

Feel free to contribute, report issues, or provide feedback. Let's collaborate to enhance and optimize the Django Marketplace (DMVC)!
