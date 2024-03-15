# Family Budget API

## Kellton requirements
1. Description
The application should allow for creating several users. Each user can create a list of any
number of budgets and share it with any number of users. The budget consists of income
and expenses. They are grouped into categories. It is required to create a REST or
GraphQL API and a database. The project should contain authorisation, tests, fixtures,
filtering and pagination.
2. Technologies
Any. Whatever would be best in your opinion (including JS frameworks).
3. Requirements
Entire project should be available as an open source project on GitHub. Please commit
your work on a regular basis (rather than one huge commit). The project should contain a
README file with information on how to install the application in a local environment.
4. Deploy
5. Please use Docker for orchestration (docker-compose).


## Getting started:
- to build and run use ```docker compose up``` command from the project directory. 
- access with: ```http://127.0.0.1:8000/```
- login details: ```username: test, password: test```

## Authentication:
all api endpoints require authenticated user. See Getting started section for credentials. For this excercise purpose 
I have used standard authentication method (username and password)

## Authorisation:
For this excercise all budgets viewable only for users with admin permission. 
Otherwise users can view their own budgets or budgets that are shared with them

## Architecture
1. I took simplified approach. Architecture consists of following models:
* Budget: Each budget model
* BudgetOperation: any operation related to Budget model. Amount field indicates it's type expense (negative) 
or income (positive)

2. I have assumed that shared budgets are editable both by budget owners and chosen users.
3. As budget context derives from given timeframe. I have added date filters to both budget and operations views. 

## Api endpoints overview
All standard CRUD methods were added.

### additional filters to list views:

### api/budgets/ 
* ```?type=owned/shared``` determines whether only budgets owned or shared will be returned. Defaults to both
* ```?detailed=true``` if true any foreign relations (like budget operations or user details) will be in detail
* ```?date_start=YYYY-MM-DD&date_end=YYYY-MM-DD``` returns only budgets with operations within the given date range
* ```?search=[string]``` returns only budgets with name partially matching search term

### api/operations/
* ```?budget_id=[int]``` returns only operations related to specific budget
* ```?date_start=YYYY-MM-DD&date_end=YYYY-MM-DD``` returns only operations within the given date range
* ```?search=[string]``` returns only budgets with name partially matching search term

## Tests
unit and functional tests added on build

## Fixtures
Fixtures load automatically when you run project. 
To run manually run ```docker compose exec server python manage.py loaddata apps/budgets/fixtures/initial_data.json```

## Pagination
Page number pagination added

## Model restrictions:
no restriction on future dates as user might want to input future dates

