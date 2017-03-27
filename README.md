# Project Assignment (DO NOT MERGE WITHOUT REVIEW) 

## Use materializeCSS throughout the project. Make sure you use these links while making the templates.
# IT IS ESSENTIAL YOU KNOW THE DIFFERENCE BETWEEN s6 and m6 col widths
## Note that the page is divided into a container, which is then divided into 12-columns
## s12 => On a small (mobile) display, the content will be full width (12 of 12)
## m6 => On a medium (laptop) display, the content will be half width (6 of 12)
## Use offset-m<x> to move a div by x units in the specified display size

Use materializeCSS throughout the project. Make sure you use these links while making the templates.
Copy the ` template.html ` onto your PC and work in it to have less issues later on. DO NOT MAKE CHANGES outside of the container

CSS : https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/css/materialize.min.css
` <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/css/materialize.min.css" rel="stylesheet" type="text/css"> `

jQuery: ` <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script> `

JS  : https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/js/materialize.min.js
` <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/js/materialize.min.js"></script> `

ICONS : ` <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">`

(Materialize has been hosted in the repo itself; use it for convienience; You would still need to include jQuery and Icons for everything to work properly.)
The structure will be uploaded soon. Fork your own copies and push changes to them and submit a PR for merging into the final project.
The layouts have been uploaded in the group; template work can be started. 


# How to Run

Run the following command in your terminal

` python2.7 run.py <port> `

(Specify your desired port, or keep blank for the default (8000))

# Templates completed so far:

- Homepage
- Problem Page
- Login Page
- Signup Page
- Admin Profile
- User Profile

# Writeup 

## Users:

- Solver: User can browse/search through problems, submit solutions to problems, view his stats, etc.
- Setter: Admin can set problems; keep record of all problems submitted.

## Entities:

- Home - Problem page with display of problems according to tags, and date uploaded.
- Profile page - View submissions/uploads alongwith textual and graphical statistics about submissions
- Problem page - Contains information about said problem, along with display of few testcases and a solution upload section.

## Features:

- Users can either register as a solver or setter.
- User can browse through problems, search by tags or name, and attempt.
- Submissions can be made in C, C++, python2, python3.
- No API used; checking done from stratch. 
- Supports error messages, syntax errors, TLE, SEG fault
- Admin can upload solution in either C or C++
- Both users are provided with a variety of statistics to evaluate their performance 
