# LETS SWAP

## _A used items market place_

## Table of Contents

- [Summary](#summary)
- [Tech Stack](#tech-stack)
- [Features](#features)
<!-- - [Data Model](#data-model) -->
- [Local Installation](#installation)
- [About the Developer](#aboutme)
- [Acknowledgements](#acknowledgements)

## <a name="summary"></a>Summary

[![**Find my demo video here**](static/images/youtube-rs.jpg)](https://www.youtube.com/watch?v=SNf_pZP1Fj4 "LETS SWAP")

<br>
<br>
**LETS SWAP** is a platform where users can exchange their unwanted items with other users. This can be a great way to get rid of things you don't need anymore and get something new in return, without having to spend any money. With the sustainable living on the rise, swapping used items instead of buying new products means less clutter in life and less waste to the environment.

## <a name="features"></a>Features
<ul>
<li> This application allows users to explore items listing, search or filter by category </li>

<li> It also allows users to view basic information such as their username, email and address. They can also see the items they have listed and their real-time status. </li>

<li> Users can also make swap request to exchange item. They can click to view item detail and send a swap request by selecting their own listed item. Once the request is created, users can communicate via the comments section on each request to coordinate the exchange </li>

<li> Users can have a view of all their sent or received  requests, they can either cancel, reject, or accept the exchange requests. If a request is ACCEPTED, there will also be a database transaction to update the status of both items to SWAPPED to ensure the integrity of the transaction. </li>
</ul>

## <a name="tech-stack"></a>Tech Stack

**Back End:** Python3, Flask framework, SQLAlchemy, Postgresql database<br/>
**Password Security:** bcrypt
**Front End:** JavaScript, AJAX, JSON, Jinja2, Bootstrap5, HTML, CSS<br/>
**APIs:** Google Maps API, Image Kit API<br/>

## <a name="installation"></a>Local Installation

#### start local postgres
```
#mac
$ pg_ctl -D /usr/local/var/postgres start
#linux
$ pg_ctl start
```
#### bootstrap database
```
# Run once to initialize tables
$ psql -f sql_bootstrap.sql
```

#### secret file
```
pass secret under /venv/.env
```


#### item-exchange run
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ flask run
```
In your browser, visit <a href="http://localhost:5000/">http://localhost:5000/</a>


## <a name="acknowledgements"></a>Acknowledgements

I wish to extend my deepest gratitude to all the individuals who have been instrumental in my journey throughout this project, as well as the intensive 6-month coding bootcamp. I'm profoundly thankful for the knowledge I've acquired and for the unwavering support and encouragement from my Hackbright instructors and fellow cohortmates. In addition, I am deeply grateful to have received a scholarship from Walmart, which helped me to move one step closer to my dream of becoming a software engineer.My heartfelt thanks go out to my family and friends for their consistent support and encouragement during my studies. Your contributions have played a significant role in my success. Thank you all.

## <a name="aboutme"></a>About the Software Engineer

Lien Dao is a software engineer with several years of experience in sales analytics, and she is deeply passionate about solving business problems through technology while also remaining committed to learning new technologies. Her diverse background in business, data, and technology has shaped her into a well-rounded software engineer, enabling her to connect with individuals from diverse backgrounds within a team.

She is one of 28 candidates nationwide who have been awarded a full scholarship by Walmart to study full-stack software engineering.

Connect and learn more about Lien Dao on <a href="https://www.linkedin.com/in/lien-dao">LinkedIn</a>.

