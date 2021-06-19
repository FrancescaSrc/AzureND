## This folder will contains the Azure function code.

## Note:

- Before deploying, be sure to update your requirements.txt file by running `pip freeze > requirements.txt`
- Known issue, the python package `psycopg2` does not work directly in Azure; install `psycopg2-binary` instead to use the `psycopg2` library in Azure

The skelton of the `__init__.py` file will consist of the following logic:

```
import logging
from web.app.routes import attendees
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(host="p3-dbserver.postgres.database.azure.com",
                                    dbname="techconfdb",
                                    user="pgadmin@p3-dbserver",
                                    password="7june2021")
    cursor = conn.cursor()

    try:
        # Get notification message and subject from database using the notification_id
        notification = cursor.execute(
            "SELECT message, subject FROM notification WHERE id == {}; ".format(notification.id)
        )

        # Get attendees email and name
        cursor.execute(
            "SELECT email, first_name FROM attendee;"
        )
        attendees=cursor.fetchall()

        # Loop through each attendee and send an email with a personalized subject
        for att in attendees:
            Mail("{}, {}, {}".format({'fpaulin@solvedo.com'},{'att[]'}, {notification}))
           

        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        completed_date = datetime.now()
        status = '{} attendees notified'.format(len(attendees))
        update = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}', WHERE id = {};".format(status, completed_date, notification_id))
        conn.commit()


    except(Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        conn.rollback()

    finally:
        # TODO: Close connection
        cursor.close()
        conn.close()
```
