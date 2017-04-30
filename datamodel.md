# This file contains all the details about models used.
## Problem
All the data regarding problems is stored in the table named "problems" in the database.
* The 'id' is the primary key , unique for problems.
* To prevent script attacks 'uid' is used for routing.
* 'title' and 'tags' column stores title and tags for each problem . It is not nullable.
* 'uploader' uses 'uid' of the user who uploaded the problem.
* 'problem_location' , 'io_location' , 'solution_location' , 'editorial_location' use time stamp to create hash which is used as the name of resp. files.

## User
All the data regarding users is stored in the table named "users" in the database.
* The 'id' is the primary key , unique for users.
* 'uid' uses time stamp to generate hash which is unique for every user.
* 'username' , 'email' , 'password' and 'role' are non-nullable enteries.
* 'total_submissions' stores the total number of submissions of the user.
* 'accepted' , 'wrong_answer' and 'tle' stores the number of solutions accepted , not accepted(wrong answer) , and not accepted(tle).
* 'check_password_hash' checks if the password entered is correct or not. It changes the entered password into key using hash function and then matches both the hashes.
* 'getIdentifiers' return user's details like username , email , role and his/her rank .
* 'getStats' returns number of solutions accepted , not accepted and total number of submissions of the user.

## Submission
All the data regarding submissions is stored in the table named "submissions" in the database.

* Primary key for this table is 'id'.
* 'uid' is generated using hashed time stamp so that it is unique for every submission.
* 'submission_timestamp' stores the time at which code was submitted.
* 'status' tells you whether the solution got accepted or not and if not then why .
* 'user_id' has stores the 'uid' of user. 
* 'problem_id' has the 'uid' of the corresponding problem.
* Functons operate as same in user.

## Comment
All the data regarding comments is stored in the table named "comments" in the database.
* The 'id' is the primary key , unique for every comment.
* 'uid' uses time stamp to generate hash which is unique for every comment.
* 'user_id' has stores the 'uid' of user. 
* 'problem_id' has the 'uid' of the corresponding problem.
* 'body' stores the comment added.
* 'getstats' returns 'uid' of the user who commented , 'uid' of the corresponding problem and the time at which comment was added.