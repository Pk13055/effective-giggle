# Project Assignment-DOJE(Online Judge) 

## How to Run
1.	change permissions of effective-giggle 
	change permissions of /var/run 

2. update /etc/nginx/site-available/default
with:-
server {
    listen 5000;
	listen 443 ssl;
	ssl_certificate /etc/nginx/ssl/nginx.crt;
	ssl_certificate_key /etc/nginx/ssl/nginx.key;

	server_name 0.0.0.0;

	location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
		alias /home/shubh/Major_Project/effective-giggle/app/;
		}
    
	 location /media/ {
        alias /home/shubh/Major_Project/effective-giggle/app/static/images;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///var/run/project.sock;
	}
    
	
}

3. update the location path of socket in uwsgi.ini and /etc/nginx/site-available/default
3.1 make sure your directory path has no " "(spaces)  

4. Run the following command in your terminal to start 	  the server

	uwsgi --ini uwsgi.ini
	sudo service nginx restart

##	To stop nginx
	sudo service nginx stop 

` python2.7 run.py <port> `

(Specify your desired port, or keep blank for the default (8000))

## Generate Database

Run the following files in order 

` python2.7 user_gen.py <no> `
` python2.7 problem_gen.py <no> `
` python2.7 comment_gen.py <no> `

* where `<no>` is the number of users/problems/comments you want to generate 
* you do not need to delete your db copies as they're covered by your =gitignore= 

## Used materializeCSS throughout the project.

CSS : https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/css/materialize.min.css
` <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/css/materialize.min.css" rel="stylesheet" type="text/css"> `

jQuery: ` <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script> `

JS  : https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/js/materialize.min.js
` <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.1/js/materialize.min.js"></script> `

ICONS : ` <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">`

(Materialize has been hosted in the repo itself; use it for convienience; You would still need to include jQuery and Icons for everything to work properly.)
The structure will be uploaded soon. Fork your own copies and push changes to them and submit a PR for merging into the final project.

## Writeup 
- Users:
 - Solver: 
 	- User can browse/search through problems, submit solutions to problems, view his stats, etc.
 	- User can add various fields like profile picture,location,email id and organization,
 - Setter: Admin can set problem statements, what language is that problem available in, time limit for each language, sample input/output files.
 - Both users are presented with conciliated statistics regarding their problems, submissions, status, etc.

- Entities:
 -User:
 	- Each User has a username, password, rating, number of problems solved, score and type(solver, setter)
 	- Certain user properties depend on the type of user, ie, solver or setter
 -Problem:
 	- Each problem has a statement, sample input, sample output, language, solution, topic tags

- Main Pages:
 - Home - Problem page with display of problems according to tags, and date uploaded.
 - Profile page - View submissions/uploads alongwith textual and graphical statistics about submissions
 - Problem page - Contains information about said problem, along with display of few testcases and a solution upload section.
 - Editorial Page - this contains the solution/hints for the particular problem along with a section for users to discuss their queries.

- Features:
 - Users can either register as a solver or setter.
 - User can browse through problems, search by tags or name, and attempt.
 - User can solve/set problems in any of the allowed/supported languages (domain = C, C++, python2, python3)
 - Supports error messages, syntax errors, TLE, SEG fault
 - User can search problems by tags 

 - Submissions can be made in any of the allowed languages (domain =  C, C++, python2, python3)
 - No API used; checking done from stratch. (no need to mention this)
 - Admin can upload solution in either C or C++ (replace)

 - Both users are provided with a variety of statistics to evaluate their performance.
 	- Users:
 		- Number of WA
 		- Number of AC
 		- Number of TLE
 		- Number of submissions
 		- Efficiency
 		- Ranking 
 		- (note that this is per problem as well as in total per user)
 		- Data is presented in the form of (downloadable) charts and a histogram

 	- Admins:
 		- Total of people who submitted 
 		- WA, TLE, AC per problem submitted
 		- Admin can add various details about his profile like organization,email id,location,profile picture.
 		- Add tags to the problem for easy search by the user who is solving these types of problem. 
