import datetime
import uuid

class Application():
    def __init__(self, company, role, category, deadline, status, link, date_created):
        self.id = uuid.uuid4().hex
        self.company = company
        self.role = role
        self.category = category
        self.deadline = deadline
        self.status = status
        self.link = link
        self.date_created = date_created
        
    def days_left(self):
        return (datetime.datetime.strptime(self.deadline, "%Y-%m-%d").date() - datetime.datetime.now().date()).days
    
    def to_json(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "category": self.category,
            "deadline": self.deadline,
            "status": self.status,
            "link": self.link,
            "date_created": self.date_created,
            "days_left": self.days_left()
        }
    
class ApplicationList():
    def __init__(self):
        self.applications = []
        
    def initialize(self):
        self.applications = [
            Application("Google", 
                        "Data & AI", 
                        "Tech", 
                        "2024-08-10",
                        "Not Started", 
                        "https://www.google.com",
                        "2024-08-07"),
        ]

    def add(self, application):
        self.applications.append(application)
        
    def to_json(self):
        return [application.to_json() for application in self.applications]
    
    def delete(self, id):
        self.applications = [application for application in self.applications if application.id != id]
    
