
# QRKot Application
<img width="2874" height="1615" alt="cats" src="https://github.com/user-attachments/assets/44f2c762-1df8-42b8-b939-b3e8250ebecc" />

## Table of Contents

* [Application Overview](#application-overview)
    * [Projects](#projects)
    * [Donations](#donations)
    * [Users](#users)
* [Technical Details and Requirements](#technical-details-and-requirements)
    * [Users](#users-1)
    * [Projects](#projects-1)
    * [User Permissions](#user-permissions)
    * [Donations](#donations-1)
* [Donation Process](#donation-process)
* [Deployment Instructions](#deployment-instructions)
* [System Requirements](#system-requirements)

---

## Application Overview

This project is an API service for the charity foundation **QRKot** that supports cats.  

The foundation collects donations for various targeted projects, for example:
* medical treatment for cats in need,
* setting up cat colonies in basements,
* food for stray cats,
* or any other goals related to supporting the cat population.  

### Projects

The QRKot foundation can host multiple target projects. Each project has a name, description, and target amount to raise. Once the required amount is collected, the project is closed.  

Donations are allocated to projects based on the *First In, First Out* principle: all donations go to the earliest opened project. When that project reaches its goal and closes, donations start flowing into the next one.  

### Donations

Each user can make a donation and add a comment. Donations are not project-specific — they go into the foundation, not directly to a particular project.  

Every donation is automatically applied to the first open project that hasn’t yet reached its goal. If the donation exceeds the required amount, or if there are no open projects, the remaining money is reserved until a new project is opened. When a new project is created, any reserved donations are automatically invested in it.  

### Users

Projects can only be created by administrators.  

Any user can see the list of all projects, including required and invested amounts (for both open and closed projects).  

Registered users can make donations and view the list of their own donations.  

---

## Technical Details and Requirements

### Users

* Uses **FastAPI Users** library.  
* Bearer transport and JWT strategy are implemented.  
* Auth Router, Register Router, and Users Router are connected.  
* User deletion is forbidden: the delete endpoint is overridden as deprecated.  

### Projects

Projects are represented by the `CharityProject` model, mapped to the `charityproject` database table.  

Columns of `charityproject`:
* `id` — primary key  
* `name` — unique project name, required string (1–100 characters)  
* `description` — required text field (≥1 character)  
* `full_amount` — target amount, integer (>0)  
* `invested_amount` — invested amount, integer (default=0)  
* `fully_invested` — boolean, whether the required sum has been collected (default=False)  
* `create_date` — project creation date, DateTime, set automatically  
* `close_date` — project closing date, DateTime, set automatically when the project is fully funded  

### Donations

Donations are represented by the `Donation` model, mapped to the `donation` table.  

Columns of `donation`:
* `id` — primary key  
* `user_id` — ID of the donating user (FK to user.id)  
* `comment` — optional text field  
* `full_amount` — donation amount, integer (>0)  
* `invested_amount` — amount invested into projects, integer (default=0)  
* `fully_invested` — boolean, whether the full donation was allocated (default=False)  
* `create_date` — donation creation date, DateTime, set automatically  
* `close_date` — date when the donation was fully invested, DateTime, set automatically  

### User Permissions

* Any visitor (including unauthenticated) can view the list of all projects.  
* Superusers can:  
  - create projects,  
  - delete projects that have no funds,  
  - update project name, description, or target amount (not less than already invested).  
* Nobody can:  
  - change invested amounts through the API,  
  - delete or edit closed projects,  
  - modify creation or closing dates.  
* Any registered user can make donations.  
* A registered user can view only their own donations (fields: `id`, `comment`, `full_amount`, `create_date`).  
* Superusers can view all donations with all fields.  
* Donations cannot be edited or deleted by anyone.  

---

## Donation Process

Immediately after a new project or donation is created, the **investment process** begins (updating `invested_amount`, setting `fully_invested` and `close_date` when necessary).  

* If a new project is created and there are unallocated donations, they are automatically invested into the new project.  
* If a new donation is made while there are open projects, the donation is automatically allocated to them.  

[:arrow_up:Back to Table of Contents](#table-of-contents)  

---

## Deployment Instructions

* Clone the repository:  
  `git clone https://github.com/4its/QRkot_spreadsheets.git`  
* Enter the folder:  
  `cd QRkot_spreadsheets`  
* Create a virtual environment:  
  `python3 -m venv venv`  
* Activate the environment:  
  `. venv/bin/activate`  
* Install dependencies:  
  `pip install -r requirements.txt`  
* Apply migrations:  
  `alembic upgrade head`  
* Run the server:  
  * Simple: `uvicorn main:app`  
  * With autoreload: `uvicorn main:app --reload`  

### Swagger Documentation
Available at (with the server running, default settings):  
http://127.0.0.1:8000/docs  

---

## System Requirements

* Python 3.9  
* FastAPI 0.78.0  
* SQLite  

---

## Project Author
[**Vilmen Abramian**](https://github.com/VilmenAbramian),  vilmen.abramian@gmail.com

Sprint 24
