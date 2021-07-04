# Analysis of costs, resources and solution choice

# VM Solution Costs
Based on a minimal cost calculation.
| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *SQL Database licensing* |   1v Core, 1GB memory, 5 GB database   |      free     |
| *Azure VM*   |     B1ls General purpose 2 vCPU, 8GB RAM, 4 Data disks    |     59.10 EUR / month         |
 *Blob Container*                   |   D1 v2: 1 vCPU, 2.5 GB RAM, 50 GB storage      |          83 EUR/month     |
| *Azure Storage account* |   1 account  10k transactions  StorageV1 (general purpose v1)   |  0.01 EUR              |
| *total*                   | Free and basic tier        |        142.11 EUR  MONTH    |

The VM solution would offer:
- High scalability: in case of increase in the number of users, the VMs can be grouped together
- Availability: dedicated servers both for compute power and security reasons
- Workflow: Support of Linux and Window VMs with custom images, more control on the development stack, more languages supported
- Costs: more compute power will mean higher costs


# App Service Solution Costs
Based on a minimal cost calculation.

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *SQL Database* |   1v Core, 5 GB Storage, Basic, Backup 7 days   |      21.70 EUR / month        |
| *Azure SQL Server*     |    Basic     |     4.95  EUR / month        |
 *Azure App Service Plan*   | F1: Free        |        0      |
| *App Service*                   | 1 instance (free plan)       | 0             |
| *Blob Database*                   |  General Purpose      |         19 EUR/month     |
| *total*                   | Free and basic tier        |        45.65 EUR  MONTH    |


The App Service solution would offer:
- Scalability: Vertical scaling limited to max of 4 CPUs and 14 GB of RAM, horizontal scaling with more machines
- Availability: High availability, auto-scaling and support of both Linux and Windows environment
- Workflow: Continuous deployment model with GitHub, Azure DevOps and use of major development languages
- Costs: granular on the base of the chosen plan

# Solution choice: App Service

In the choice of the type of solution, some key points are to be considered:

- Deploying a simple webapp with potential growth
- Scaling up of processing power might be a concern for later
- Cost-consciousness over speed and scalability
- Good response 
- Deployment with Python and Github, no other special needs


I would choose an App Service in this situation. Lightweight APIs tend to be well-suited to App Services over VMs, and won't approach the size limit for App Services very easily. Additionally, App Services cost less than VMs do. Lastly, since the ability to scale quickly is less of a concern, we don't need to factor that into the analysis.


I have chosen an App Service for the current deployment. The App Service is much cheaper and more flexible for lightweight webapps such as the one I implemented. The webapp will not approach the size limit for App Services very quickly as it runs on 1 vCPU with 5GB of RAM. By the time it will need more than 4 vCPUs and a max of 14GB of RAM, the app will be probably be very different with other functionalities in place and more users. This makes App Services a beter choice for now. Additionally, App Services cost less than VMs do. Lastly, since the ability to scale quickly is less of a concern in this development fase, we don't need to consider that in the analysis of the current situation.


### App changes that would change my choice to VMs


If and when the web app reaches a more mature phase with more users and more content, VMs would be an option to consider to migrate the current App Service from. In this case the costs would be higher but less relevant since the App reached a maximum of resources allocated for the App Service and has been therefore successfull. To maintain its success and continue its growth, a new development stack will probably be needed with more concern for security of the user data and for testing. The VMs would then offer more control on the development and the technology stack and might lead to different software solution in terms of operating system and development languages used. In such a scenario, a set of VMs rather than a lightweight App Service would be a more suitable choice. 
