# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |   Basic, 1 vCore(s), 5 GB   | $18.49 |
| *Azure App Service*   |  Free F1 1 GB memory        | $4.20 |
| *Azure Functions*   |    serverless environment     | $2.40 |
| *Azure Service Bus*   |   Basic                     | $0.03 |
| *Azure Storage*   |   StorageV2 (general purpose v2)   |  $3.75   |

Free F1 1 GB memory

## Architecture Explanation
### Azure Web Apps
Azure Web Apps is a fully managed service that helps to develop and deploy enterprise-ready web applications. It provides powerful capabilities such as built-in development operations, continuous integration with Visual Studio Online and GitHub.

App Service provides high availability with of 99.5% SLA uptime.
Built-in autoscale and load balancing

Scaling the application on demand or Scaling down for non traffic hours gets easier.

Salient feature of Azure Web Apps are available on:  
https://azure.microsoft.com/en-us/services/app-service/web/

### Azure Functions
Azure Functions is a serverless architecture. 
So, being a developer, we can completely concentrate on the code, not on the server. 
Serverless Computing is also known as a "Function-as-a-Service". It eliminates the developer's time to take care of the infrastructure. With serverless, we can simply create and upload the code and then we can define the triggers or events which will execute the function.

Function App is used in the application because we can process the email only when there is a message in a service bus queue. We will not have to pay when the Function App is not active.

Salient feature of Azure Web Apps are available on:  
https://azure.microsoft.com/en-us/services/functions/
