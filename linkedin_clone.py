
import logging, os, time
this_script = os.path.basename(__file__)
logging.basicConfig(filename=this_script+'.log', level=logging.INFO)

def log_action(func):
    def wrapper(*args, **kwargs):
        t = time.localtime()
        action_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", t)
        logging.info(f"{action_timestamp} - Running {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        return result
    return wrapper


class Company():

    all_companies = {}
    
    @log_action
    def __init__(self, name, CEO, industry, offices=None, headcount=0, id=None):
        self.name = name
        self.CEO = CEO
        self.industry = industry
        self.headcount = headcount
        self.offices = offices if offices else []
        self.id = "C" + str(len(self.all_companies))
        self.all_companies[self.id] = self

    @log_action
    def add_office(self, location, headcount):
        self.offices.append((location, headcount))
        self.headcount += headcount

    def list_offices(self):
        return self.offices
    
    def get_headcount(self):
        print(f'{self.name} has {self.headcount} employees:')
        for (location, headcount) in self.offices:
            print(f'{headcount} employees in {location}')

    def print_company_details(self):
        print(f'Name: {self.name}, CEO: {self.CEO}')
        self.get_headcount()

    @classmethod
    def list_all_companies(cls):
        print('Listing all companies:')
        for company in cls.all_companies.values():
            print(f'ID: {company.id}, Name: {company.name}')

    @classmethod
    def id_search(cls, id):
        return cls.all_companies[id]

    def list_company_jobs(self):
        for job in [job for job in Company.Job.all_jobs.values() if self.name == job.company.name]:
            job.print_job_details()


    class Job():

        all_jobs = {}

        @log_action
        def __init__(self, company, location, title, description=None, id=None, applicants=None):
            self.company = company
            self.location = location
            if not location in dict(company.offices):
                return
            self.title = title
            self.description = description if description else None
            self.applicants = applicants if applicants else []
            self.id = "J" + str(len(self.all_jobs))
            self.all_jobs[self.id] = self

        def print_job_details(self):
            print(f'* {self.title} at {self.company.name} located in {self.location}')
            print(self.description) if self.description else None
            print()
            print(f'Applicants: {len(self.applicants)}')
            print(f'Job ID: {self.id}')
            print()

        @classmethod
        def list_all_jobs(cls):
            print('Listing all jobs:')
            for job in cls.all_jobs.values():
                job.print_job_details()

        @classmethod
        def id_search(cls, id):
            return cls.all_jobs[id]


    class Employee():

        all_employees = {}
        
        @log_action
        def __init__(self, name, location, Employer=None, id=None, applications=None):
            self.name = name
            self.Employer = Employer if (Employer and type(Employer) == Company) else None
            self.location = location
            self.id = "E" + str(len(self.all_employees))
            self.applications = applications if applications else []
            self.all_employees[self.id] = self

        @log_action
        def apply(self, jobID):
            job = Company.Job.id_search(jobID)
            if self.id in job.applicants or jobID in self.applications:
                pass
            else:
                self.applications.append(jobID)
                job.applicants.append(self.id)

        def print_employee_details(self):
            return f"Name: {self.name}, ID: {self.id}, Employer: {self.Employer}, Located: {self.location}"


def menu_main():
    print("""
    What would you like to see?
        1. Companies
        2. Jobs
        3. Candidates
        4. Exit
    """)

def menu_companies():
    print("""
    What would you like to do?
        1. List all companies
        2. List jobs for a company
        3. Search companies by name
        4. Back
    """)

def menu_jobs():
    print("""
    What would you like to do?
        1. List all jobs
        2. List jobs for a company
        3. Search companies by name
        4. Search jobs by title/description
        5. Apply for a job
        6. Back
    """)

def menu_candidates():
    print("""
    What would you like to do?
        1. List all candidates
        2. Back
    """)


if __name__ == "__main__":

    google = Company("Google", "Sundai Pichai", "Internet Cloud computing Computer software, Computer hardware Artificial intelligence")
    google.add_office('Bucharest', 500)
    google.add_office('Berlin', 800)
    #google.get_headcount()

    facebook = Company("Facebook", "Mark Zuckerberg", "Social networking, advertising, and business insight solutions")
    facebook.add_office('Bucharest', 350)

    job1 = google.Job(google, 'Bucharest', 'Software Developer', """
        At least 3 years of experience with Linux
        At least 5 years working with Python, including Pandas
        Working experience with Maven, Artifactory, Gitlab
    """)

    job2 = google.Job(google, 'Bucharest', 'Cloud Engineer', """
        At least 3 years of experience with Linux
        At least 5 years working with GCP
        Working experience with Jenkins, Terraform and Ansible
    """)

    job3 = facebook.Job(facebook, 'Bucharest', 'Cloud Engineer', """
        At least 3 years of experience with Linux
        At least 5 years working with GCP
        Working experience with Jenkins, Terraform and Ansible
    """)

    emp1 = Company.Employee('Test User', 'Paris')
    emp1.apply('J1')

    while 1 == 1:
        menu_main()
        opt = input("Enter: ")
        match opt:
            case '1':
                while 1 == 1:
                    menu_companies()
                    opt = input("Enter: ")
                    match opt:
                        case '1':
                            print()
                            Company.list_all_companies()
                            input("Press Enter to return...")
                        case '2':
                            companyID = input("\nEnter Company ID: ")
                            company = Company.id_search(companyID)
                            company.list_company_jobs()
                            input("Press Enter to return...")
                        case '3':
                            regex = input("\nEnter search pattern: ")
                            results = [company for company in Company.all_companies.values() if regex.lower() in company.name.lower() ]
                            for company in results:
                                print()
                                company.print_company_details()
                        case '4':
                            break
            case '2':
                while 1 == 1:
                    menu_jobs()
                    opt = input("Enter: ")
                    match opt:
                        case '1':
                            print()
                            Company.Job.list_all_jobs()
                            input("Press Enter to return...")
                        case '2':
                            companyID = input("\nEnter Company ID: ")
                            company = Company.id_search(companyID)
                            company.list_company_jobs()
                            input("Press Enter to return...")
                        case '3':
                            regex = input("\nEnter search pattern: ")
                            results = [company for company in Company.all_companies.values() if regex.lower() in company.name.lower() ]
                            for company in results:
                                print()
                                company.print_company_details()
                        case '4':
                            regex = input("\nEnter search pattern: ")
                            results = [job for job in Company.Job.all_jobs.values() 
                                       if regex.lower() in job.title.lower() or regex.lower() in job.description.lower() ]
                            for job in results:
                                print()
                                job.print_job_details()
                            input("Press Enter to return...")
                        case '5':
                            jobID = input("\nEnter Job ID: ")
                            empID = input("\nWho will be applying for this job?\nEnter Employee ID: ")
                            candidate = [emp for emp in Company.Employee.all_employees.values() if emp.id == empID]
                            candidate[0].apply(jobID)
                            input("Press Enter to return...")
                        case '6':
                            break

            case '3':
                menu_candidates()
                opt = input("Enter: ")
                match opt:
                    case '1':
                        print()
                        for emp in Company.Employee.all_employees.values():
                            print(emp.print_employee_details())
            case '4':
                break
        