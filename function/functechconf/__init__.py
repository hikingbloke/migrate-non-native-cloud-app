import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # Get dbconnection to database
    dbconnection = psycopg2.connect(dbname="postgres", user="bipinsa@mydemoserver", password="Mydatabase33#", host="mydemoserver.postgres.database.azure.com")
    dbconnection.autocommit = True
    cursor = dbconnection.cursor()

    try:
        # Get notification message and subject from database using the notification_id        
        cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))
        notification_details = cursor.fetchone()
        notification_message = notification_details[0]
        notification_subject = notification_details[1]

        # Get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()

        from_email = os.environ["ADMIN_EMAIL_ADDRESS"]

        # Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            first_name = attendee[0]
            email = attendee[2]
            personalized_message = '{}: {}'.format(first_name, notification_subject)
            Mail('{}, {}, {}, {}'.format(from_email, email, personalized_message, notification_message))

        notification_completed_date = datetime.now()

        notification_status = 'Notified {} attendees'.format(len(attendees))
        
        update_query = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))        

        dbconnection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # Close dbconnection
        cursor.close()
        dbconnection.close()
