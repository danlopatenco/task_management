## Task Management App (Back End) 
This Task Management App is a simple yet powerful tool for managing tasks and conversations between users. It's built with Django and uses Docker for easy setup and deployment.

### Prerequisites

Before begin, ensure that the following requirements:

Docker and Docker Compose are installed on machine.
Basic knowledge of Docker and containerization concepts.

## Getting Started
### Configuration
1. Clone the repository to local machine:


2. Create an .envrc file and fill it with environment variables based on the .envrc.example:

```
cp .envrc.example .envrc

```
3. The `docker-compose.yml` file contains the configuration for the application and database services. If necessary, adjust the environment variables and other settings in this file and the `.envrc`.

 Build and run the containers using docker-compose:
```
docker-compose up --build
```
After the build completes and the services are running, the application will be available at http://localhost:8585.

Once Docker Compose has successfully built and the containers are running, open another terminal window in the same directory to continue with the next steps for Database Initialization.



### Database Initialization
After the containers are up and running, need to make the database ready to use:
1. Change the permissions of the app_container.sh script to make it executable:
```
chmod 777 app_container.sh
```
2. Run the docker-compose ps command to find the correct name of the app container:
```
docker-compose ps
```
3. Update the `app_container.sh` script. Open the script in a text editor and locate the line with `CONTAINER_NAME`. Replace the placeholder name with the actual name of the container that you found using docker-compose ps. For example, if the correct container name is `tasks_management_backend_app_1`, change the line to:
```
CONTAINER_NAME="tasks_management_backend_app_1"
```
4. Enter the Django application container using the app_container.sh script:
```
./app_container.sh
```
5. Run:
```
source .envrc
```
6. Set up the database by running migrations:
```
./manage.py migrate
```

### Creating a Superuser
To create an admin account for Django's admin interface, run the following command and follow the prompts:
```
./manage.py createsuperuser
```
 access the Django admin site at `http://localhost:8585/admin`.

 ### Running Tests
To run the available tests for the application, execute the following command:
```
./manage.py test
```

### API Endpoints
Below are the available endpoints for the Task Management App:
#### Authentication
For endpoints that require authentication, use the following header:
```
Headers:
Authorization: Bearer {ACCESS_TOKEN}
```
Register a new user:
```
POST /api/auth/users/
{
  "username": "u1",
  "password": "pwd"
}
```
Login:
```
POST /api/auth/login/
{
  "username": "u1",
  "password": "pwd"
}
```
Refresh Token:
```
POST /api/auth/refresh/
{
  "refresh": "REFRESH_TOKEN"
}

```
Logout (Auth headers required):
```
POST /api/auth/logout/
Body:
{
  "refresh": "REFRESH_TOKEN"
}

```
Change Password (Auth headers required):
```
POST /api/auth/users/set_password/
{
  "new_password": "curr",
  "current_password": "new"
}
```

#### Projects
List Projects (Auth headers required):
```
GET /api/projects/project
```
Project Details (Auth headers required):
```
GET /api/projects/project/{project_id}
```
Create Project (Auth headers required):
```
POST /api/projects/project/
{
  "title":str,
  "description":str,
  "start_date":str("YYYY-MM-DD"),
  "end_date":str("YYYY-MM-DD") 
}
```
Delete Project (Auth headers required):
```
DELETE /api/projects/project/{project_id}
```
Update Project (Auth headers required):
```
PATCH /api/projects/project/{project_id}/
{
"model_field":"updated_value"
}
```

#### Tasks
List Tasks (Auth headers required):
```
GET /api/tasks/task/
```
Task Details (Auth headers required):
```
GET /api/tasks/task/{task_id}
```
Update Task (Auth headers required):
```
PATCH /api/tasks/task/{task_id}/
```
Delete Task (Auth headers required):
```
DELETE /api/tasks/task/{task_id}
```
Create Task (Auth headers required):
```
POST /api/tasks/task/
{
  "title": str,
  "description":str,
  "deadline":str("YYYY-MM-DD"),
  "status": CHOISE: 'in_progress' / 'completed' / 'delayed'
  "project_id":"2"
}
```

#### Time Tracking
Start Time Tracking for a Task (Auth headers required):
```
POST /api/time-tracker/time-trackers/start_tracking/
{
"task_id": int
}
```
Stop Time Tracking for a Task (Auth headers required):
```
POST /api/time-tracker/time-trackers/stop_tracking/
{
"task_id": int
}
```

#### Messaging
Create a Conversation (Auth headers required):
Create a new conversation by specifying the recipient's user ID and the initial message content.
```
POST /api/messages/conversations/
Body:
{
  "recipient_id": USER_ID,
  "initial_message": "MESSAGE_CONTENT"
}

```

Replace `USER_ID` with the ID of the user to start a conversation with and `MESSAGE_CONTENT` with initial message.

Reply to a Conversation (Auth headers required):
Send a message reply within an existing conversation.

```
POST /api/messages/messages/
Body:
{
  "conversation": CONVERSATION_ID,
  "content": "REPLY_MESSAGE_CONTENT"
}
```
Replace `CONVERSATION_ID` with the ID of the conversation to reply to and `REPLY_MESSAGE_CONTENT` with an message.

## Future Enhancements
As the project management tool evolves, there are several areas identified for potential improvements and 
features that could be implemented. These enhancements aim to streamline workflow, improve user experience, and add functionality:

#### 1. Access Control Management:
Implement a robust access control system that allows for roles like Senior Developers or Project Managers to have different levels of control over projects and tasks. This would include permissions to create, edit, and delete projects and tasks based on the user's role within the team.

#### 2. Real-time Messaging:
Upgrade the messaging system to support real-time communication using WebSockets. This would allow users to receive and send messages without the need to refresh the page, facilitating instant interaction between team members.

#### 3. Task Update and Comment Tracking:
Add a feature that tracks changes and comments on each task. This would provide a history of updates, allowing team members to view the progression of a task and any discussions related to it, enhancing collaboration.

#### 4. Project Update and Comment Tracking:
Similar to task tracking, implement tracking of updates and comments at the project level. This would keep all stakeholders informed about the latest changes and decisions made regarding the project's direction and milestones.


These enhancements will contribute to a more dynamic and collaborative environment for project management, and we look forward to continually improving the tool to meet the needs of our users.
