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
