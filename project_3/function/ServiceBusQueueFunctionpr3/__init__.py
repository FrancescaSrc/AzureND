import logging
import azure.functions as func
import psycopg2
from datetime import datetime
from sendgrid.helpers.mail import Mail
from mailer import Mailer
from mailer import Message


def main(msg: func.ServiceBusMessage):
  
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)
    
    # Get connection to database
    try:
        conn = psycopg2.connect(host="p3-dbserver.postgres.database.azure.com",
                                    dbname="techconfdb",
                                    user="pgadmin@p3-dbserver",
                                    password="7June2021")
       # logging.info('Connction to Databse established...{}'.format(conn))                              
        cursor = conn.cursor()
        logging.info('Connction to Databse established...')
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)

    try:
        # Get notification message and subject from database using the notification_id
        notification = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
        print('Notification query done')

        # Get attendees email and name
        cursor.execute("SELECT first_name, email FROM attendee;")
        attendees=cursor.fetchall()
        logging.info('Attendees fetched {}'.format(len(attendees)))

        # Loop through each attendee and send an email with a personalized subject
        logging.info('Sending emails...')
        for att in attendees:
           # Mail('{}, {}, {}'.format({'admin@techconf.com'}, {att[1]}, {notification}))
           # could not get a Sendgrid API so I used a different method, this code is taken from the mailer framework examples
            message = Message(From="info@solvedo.com", To=str(att[1]), charset="utf-8")
            message.Subject = "Confirmation notification"
            message.Body = str(notification)
            sender = Mailer('webreus.email')
            sender.send(message)

        # Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        logging.info('Updating database...')
        compl_date = datetime.utcnow()
        status = "Notified {} attendees!".format(len(attendees))
        update_db = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, compl_date, notification_id))
        logging.info("DB is updated")
        conn.commit()


    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        conn.rollback()

    finally:
        # Close connection
        cursor.close()
        conn.close()