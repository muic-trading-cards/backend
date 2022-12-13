# Cardz By Lantz
Presented by **Los 011 Amigos**.
## Website
http://cards.tanpantz.com
## Background
For trading card colllectors, it is  can be difficult to find specific/rare cards if they are scattered across multiple platforms (ebay, craigslist, etc). In order to alleviate this issue, we have created a centralized database that could act as the main hub for the trading card community. Users interact with a Flask webapp which allows them to upload, buy and sell cards of various categories.
## How it works
Cardz By Lantz is a online platform for trading and collecting cards of all kinds. From sports cards to collectible cards and even virtual cards, Cardz By Lantz has something for everyone. The website is easy to use and offers a wide variety of cards to choose from, making it a great place for card collectors and traders to find what they're looking for.

Users are able to add *cards* to their collection by uploading a image and writing a brief description/name. Aside from storing them in their collection, they are also able to sell them on the open market as listings (as well as also being able to purchase listings from others as well).
## Database Design
### ER Diagram
Below is the ER diagram designed for the card database.

![Schema](https://i.imgur.com/yK3kQd4.jpg)
## Original Page Design
For creating the initial design of the website we used [Figma](https://www.figma.com).

![](https://i.imgur.com/J7dh1FL.png)
![](https://i.imgur.com/66SDfE0.png)
![](https://i.imgur.com/ILTNKyD.png)
![](https://i.imgur.com/2J54vSt.png)
![](https://i.imgur.com/t1fjSrg.png)

## Deployment
The database runs on a digital ocean droplet, but this repository allows for use at any url.  

The url is set during the container creation by setting environment variables inside the `app/shared.py` file.  For deployment on the cloud we use github actions CI/CD.  Whenever a change is made and pushed to main, there is a script in `.github/workflows` that builds a docker image, publishes the image to ghcr.io, and then using an [action script](https://github.com/appleboy/ssh-action) to remotely execute a command on the digital ocean server to pull the image and restart the docker container with the new image.  All secret credentials such as login username, ssh keys, urls are stored using github secrets so they are not viewable to the public.  Then all environment variables mentioned above are stored in an environment file on the remote server, allowing the docker image to inject them when `docker run` is called.

## Security
From a security standpoint as mentioned in the last section any sensitive login information pertaining to the database, s3 container, and the website container, are all stored seperately and not in plain text.  These cannot be accessed from the repository alone.

Passwords for users are hashed using SHA256, so no plaintext storage passwords.

On the frontend buttons things like edit/delete are hidden from users who don't own the appropriate card.  However to prevent using a tool like postman to circumvent these protections, we also implement filtering in the backend as well.  This ensures that only owners of a certain card can edit their property.  Endpoints can only be accessed if those filtering conditions are met.
#### Admin Page
The admin page is quite limited in ablity, but admins can delete users from the website if they think the are nefarious.  It also is the only place via the website to add categories.  If a user wishes to have a category added they will have to contact an admin.

![](https://i.imgur.com/AyyrEOz.png)
