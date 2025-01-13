# Final Capstone Project

Hello, and welcome to my capstone project for ALX Africa's Back-End Program!

This project represents the culmination of my learning journey,
and I am thrilled to share it with you. The focus of this project is on
building a Library Management System (LMS) API, designed to help users 
efficiently manage the borrowing and returning of books 
within a library setting.

#
## Purpose

The goal of this project is to demonstrate my understanding of building 
APIs using the Django Rest Framework (DRF) and applying various concepts 
and tools I've learned throughout the program. 
I choose this project because as someone who enjoys reading it is only logical 
I choose a project that aligns with my interests.

#
## Repository Structure

This repository contains all the resources and code for the project:

### General Overview: 
This README provides a summary of the project.
Check out [**API-Specific Documentation**]() for detailed instructions on 
using the LMS API, navigate to the _**LMS/api/api_Readme.md**_ directory and 
refer to the project-specific README file.

### Acknowledgments
Special thanks to all my ALX Cohort 2 peers and mentors. What would I have 
done without you. Your feedback and suggestions were greatly appreciated.

#

## Commit History

```
This section is to explain all I did in my commit history. 
However access to my original github account by the public has been revoked.
While I am working with the github staff to restore that
I just thought to include what I worked on. It is currently 
incomplete but untill I complete it. Here goes 
```
#
### First Commit Deliverables

In this initial phase, I focused on setting up the foundational aspects of the project:

- Configured project settings, designed the database schema, and set up environment variables.
- Initiated work on the accounts app, developing a custom user manager and user model, with email as the username field.
- Introduced a LibraryProfile model (one-to-one related) to store supplementary user information, such as roles and permissions.
- Wrote unit tests using Django’s TestCase to verify the functionality of models and methods.
- Generated clear documentation for the codebase with ChatGPT assistance.

### Challenges Faced:
- #### **Email Case Sensitivity:**
    It was challenging to figure out how to make my fields case-insensitive, 
    especially since Django treats email fields as unique but case-sensitive 
    by default. Initially, I used the ``django_case_insensitive_fields`` package
    as a workaround. However, at some point, it stopped working as intended,
    and I couldn’t pinpoint what went wrong. Ultimately, I decided to remove it.

- #### **Writing Test Cases:** 
   As a beginner, finding clear guidance was quite challenging. I spent time 
   studying examples from similar projects and carefully adapted their methodologies to fit my code.

**Note:** Migration files were ignored in this commit since the database schema was still evolving.

### Second Commit Deliverables

- Developed the API app, including the Book and BookInfo models.
- Registered the new models with the Django admin app.
- Created and tested signals for automated creation of child models and editing attributes.
- Visualized model relationships using a DBML schema.

### Challenges Faced:
- #### **Documentation:** 
    I struggled with explaining methods and functions in a technical 
    yet concise manner. To address this, I used ChatGPT to help refine the 
    docstrings and annotations. While this improved the clarity,
    I still believe there's room for further refinement.

- #### **Tests:** 
    Writing tests before the code was a real challenge for me. Most of the 
    examples in the tutorials I watched were too basic and didn't match the 
    complexity of my project. As a result, I ended up writing the code first 
    and then searching for resources online, particularly similar projects on 
    GitHub, to understand how their tests were structured.
    [TestDriven.io](https://testdriven.io/) proved to be an invaluable resource,
    and using ChatGPT further streamlined the process, making it easier to write effective tests.

- #### **Library Integration:** 
    I initially faced confusion when trying to incorporate third-party 
    packages like ``isbnlib`` and ``django_case_insensitive_fields``.
    My goal was to make certain fields in my database case-insensitive
    to simplify querying later.
    However, the ``djago_case_insensitive_fields`` package didn’t work as expected.
    After watching some YouTube tutorials, I realized I could achieve the
    same result by writing a custom method to normalize the text or field
    before saving it. I then called this normalization method in my model's
    save method, which turned out to be a much simpler and more reliable solution.

**Next Steps:** Develop the Checkouts and Transactions models.

### Third Commit Deliverables

- Enhanced the CheckOut model to track actively borrowed books and added 
    an ArchivedCheckOut model for records of returned books.

- Signals were implemented to automatically create related models and 
    decouple dependencies for maintainability.

- Wrote comprehensive unit tests to validate model methods and signal functionality using unittest.mock.

#### **Challenges Faced:**
- #### **Tests:** 
    Writing unit tests for signals was particularly challenging because of the 
    limited official documentation available. To overcome this, I relied heavily
    on external resources like Stack Overflow, GitHub forums, Django forums, 
    articles, and YouTube tutorials. These resources were invaluable in 
    helping me understand, write, and implement the tests effectively.

**Next Steps:** Develop serializers for all models and write tests for data validation and transformation logic.

### Fourth Commit Deliverables

- Wrote Serializers for all models in the Database and developed custom 
    validation methods for serializers, such as; password validation, ISBN validation among others.

- Created apiviews leveraging ModelViewSet developing CRUD operations 
    for all models and introduced a ReadOnlyModelViewSet for checkout history.

- Installed Djoser for token-based authentication with SimpleJWT.

- Wrote test cases for books and user-related endpoints and views.

#### **Challenges Faced:**
- #### **Serialization Errors:** 
   I spent a lot of time working on serialization. Initially, I couldn’t 
   decide between ``HyperlinkedModelSerializer`` and ModelSerializer, but 
   the REST Framework docs clarified that the former aligns better with 
   RESTful design. My biggest challenge was with the CheckoutSerializer,
   which had two foreign keys. I avoided nested serializers for simplicity
   and opted for a ``ModelSerializer``, but I kept encountering key errors in
   the create method. The issue was passing the book instance to the serializer
   instead of its primary key. Even after writing a custom create method,
   I struggled with retrieving data from validated_data due to incorrect key names.
   The code is currently functional but feels clunky, so I plan to revisit it.
   Additionally, I haven’t written automated tests for all serializers, which
   is something I’ll address later.

- #### **Exhaustion:** 
    I was really exhausted from reading documentation, and trying to
    figure out the errors and what they meant.

- #### **Swagger Documentation:** 
    I struggled with editing the descriptions in the Swagger UI.
    Most of my research pointed towards building a custom schema
    generator for more control over the documentation. For now, I've
    just implemented it, but I feel the documentation is still lacking in some areas.
    I will tackle this later.

- #### **Deployment:**
    Although I successfully deployed the project on 
    [PythonAnywhere](enamyaovi.pythonanywhere.com), I faced initial
    challenges with reading my environment variable file. My project
    relies on python-decouple to read values from my .env file, but the
    allowed hosts were not being read correctly. After hardcoding the
    allowed hosts in the settings file, everything started working fine.
    I plan to revisit the issue later.

**Next Steps:** Refine Swagger documentation and explore deployment on Render for comparison.

### **Reflections**

This journey has been challenging yet fulfilling. Six months ago, 
I couldn’t have imagined creating APIs, but here I am, having built
and deployed one! While the process involved hurdles like serialization
errors, testing difficulties, and deployment challenges, 
the learning experience has been invaluable. 

Thank you for reading. I look forward to continuing to grow and tackle new projects!
