
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

    # Get connection to database
    conn = psycopg2.connect(host="p3-dbserver.postgres.database.azure.com",
                                    dbname="techconfdb",
                                    user="pgadmin@p3-dbserver",
                                    password=" ")
    cursor = conn.cursor()
    print('Connction to Databse...')

    try:
        # Get notification message and subject from database using the notification_id
        notification = cursor.execute(
            "SELECT message, subject FROM notification WHERE id = {};".format(notification_id)
        )
        print('Notification {}'.format(notification))

        # Get attendees email and name
        cursor.execute("SELECT first_name, email FROM attendee;")
        attendees=cursor.fetchall()
        print('Attendees fetch {}'.format(len(attendees)))

        # Loop through each attendee and send an email with a personalized subject
        print('Sending emails...')
        for att in attendees:
            print('Sending emailto {}, {}, {}'.format('info@techconf.com', att[1], notification))
            Mail("{}, {}, {}".format({'info@techconf.com'}, {att[1]}, {notification}))
           

        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        print('Updatin...')
        compl_date = datetime.utcnow()
        status = "{} attendees notified".format(len(attendees))
        update_db = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}', WHERE id = {};".format(status, compl_date, notification_id))
        logging.info("updated")
        conn.commit()


    except(Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        conn.rollback()

    finally:
        # Close connection
        cursor.close()
        conn.close()