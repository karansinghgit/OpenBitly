# Prompt History

A verbatim log of the prompts driving development of openbitly, in chronological order.

---

## 1

> I want you to read through this repository and get an understanding of it. What we're currently building is a simple URL shortener that has a Django backend and a react-and-wet front end. What I also want you to do is add a prompt history markdown file, which will essentially be a verbatim log of all the prompts that I give to you. I want you to commit that as well.

---

## 2

> I want you to improve the front end styling without using any additional UI libraries. What the UI should look like is:
> - There should be a clean dashboard header with the name of the product, which is open bit.ly.
> - There should be a prominent form right below it.
> - Below that, there should be a list of the links, showing the short link as well as the destination.
> Later I'll also ask you to add a click count, but let's just tackle that a little later. Overall, the system should be responsive and should work well on mobile. Try not to add too many new dependencies; just try to keep it simple.

---

## 3

> I would like to improve how the front end currently looks. It should have a more premium feel. I prefer to use a color that pops out. We can go ahead with something like neon green along with monochromatic colors like black and white. Let's try to experiment.

> reject URLs pointing back at our own host to avoid any loops

---

## 4

> I want you to add click analytics to create a click model where every row will be mapped to a visit with a foreign key to the link. Let's add the timestamp, the refer, and the user agent, and we'll do this in a separate table rather than a counter column. I want you to record the click inside the redirect view synchronously, but just add a comment over there in case we ever need to move it into a queue if the redirect API is seeing heavy traffic

---

## 5

> add the click count to the UI and add the appropriate API for that
>
> meanwhile, also make the page light mode. use black in some places for contrast.

---

## 6

> Next, I want you to add a test suite with Django's test framework. Add test cases for all the APIs that we have. Add test cases for the base62 URL shortener business logic, and make sure you keep the tests short and readable

---

## 7

> I want you to now containerize the application for a server deployment. There should be a Dockerfile added that runs Django with Gunicorn, and add a docker-compose file that will have the app as well as Caddy in front of it. I'll be using Caddy to serve the React build as well as proxy API routes to Django. Apart from that, I should just be able to docker-compose up to deploy and also keep the SQLite on a separate volume.

---

## 8

> add a simple readme summarizing the application.
>
> add a design decision section that i will be adding to as well as instructions to clone and run locally if needed.

---

## 9

> can you add a copy button next to each url to make it easy to test the functionality for an end user?
