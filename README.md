# Games tracker
Games Tracker is an app that allows you to create a list of your games, which are fetched from your Steam account. You can mark games that you've completed, as well as add or remove games from your table.

# Demonstration video
This [short video](https://www.youtube.com/watch?v=GwrM_HVMHec) demonstrates the functionality of the Steam Games Tracker app, showcasing features like user login, game fetching, and management.

## Steps to Run the Application
**1. Open a terminal**

Open the terminal on your operating system.

**2.Navigate to the project folder**

Use the cd command to move into the directory where your project is located. For example:
```
cd project
```
**3.Run the application using flask run**

In the terminal, type the following command:
```
flask run
```

## Technologies
* Python
* Flask
* HTML
* CSS

## Features
### Login:
![image](https://github.com/DonMateos/cs50-app/blob/main/login.PNG?raw=true)
The "Login" page of the Steam Games Tracker application features a form with fields for both the username and password, which are required for logging in. If there is an error, such as invalid credentials, an error message is displayed in red. The page also provides links for new users to register or to return to the home page.
### Register page:
![image](https://github.com/DonMateos/cs50-app/blob/main/register.PNG?raw=true)
The "Register" page features a form with fields for the username and password, both required to create an account. If a user already has an account, they can log in through a link to the login page. The navigation bar on both pages includes links to the home, login, and registration pages.
### Home page:
![image](https://github.com/DonMateos/cs50-app/blob/main/home.PNG?raw=true)
The "Home" page of the Games Tracker application features several key elements. The navbar at the top includes links to the home, login, register, and my games pages, with the navigation options changing depending on whether the user is logged in. If the user is not logged in, a login form is displayed with fields for the username and password, along with an option to register for new users. Once logged in, users can enter their Steam profile URL to fetch their Steam games, with a button to submit the URL. If an error occurs, a message is shown. The page also includes an instructions section with clear, step-by-step guidance on how to fetch games, such as setting the Steam profile to public, obtaining a Steam API key, and pasting the profile URL. A guide link and an image are provided to help users locate their Steam profile URL.
### My games page:
![image](https://github.com/DonMateos/cs50-app/blob/main/my%20games.PNG?raw=true)
The "My Games" page in the Games Tracker application displays a list of games the user has added, with a navbar featuring links to the home page, my games, and logout options. Users can add new games by entering their name in an input field and clicking the "Add Game" button. If no games are added yet, a message prompts users to fetch games from the home page first. The page includes a table showing the list of games, with checkboxes to mark completion status and a delete button to remove games from the list. Additionally, there is an "Update Completion Status" button to update the selected games' completion statuses, and relevant error or success messages are shown as needed.

## Files
* app.py - this Flask app lets users log in, register, and manage their Steam games. It fetches games from Steam using a profile URL, allows adding, deleting, and marking games as completed, and displays them in a sorted list.

* templates/home.html – the home page of the application, containing the login form and instructions for fetching games.
* templates/login.html – the login form, allowing users to access the application.
* templates/register.html – the registration form, enabling users to create a new account.
* templates/my_games.html – the page displaying the user's game list, allowing them to add, delete, and update the completion status of games.
* static/styles.css - file defines global styles for the application, including the layout, fonts, and body styling. It customizes the navigation bar, form elements (login, register, and fetch games), and table display for games, with hover effects and responsive design. The file also includes button and error message styling to enhance the user interface.

## Conclusion
Working on this project with Flask was a fascinating experience. I had the opportunity to explore and use many new tools and concepts that were completely unfamiliar to me. I dedicated significant time to studying and testing before implementing the code. If I were to improve anything, it would be to allow users to log in via their Steam profile, which would then enable the app to fetch their game library directly. Unfortunately, I couldn’t achieve that functionality. Additionally, I would enhance the app’s appearance, but this is my first project of this kind. Hopefully, in future projects, I’ll be less limited by my current skills.
