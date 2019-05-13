
# Inkshop is about people.

It's an all-in-one system for businesses and organizations that do things the right way.  Batteries are included - manage your website, mailing list, store, and reporting all in one.  It's free.

There are tons of good systems out there.  Inkshop sticks out because it's people-focused.  It treats you, your customers, and your visitors like people, not data points.

That means no creepy tracking, no big-data segmentation, and encryption baked-in to provide strong privacy protection for both you and your customers.

Feedback, improvements, and contributions are welcome. :)

*Note on naming:*  It's entirely possible this project will be renamed Shopmonsters.  And have monsters.   We'll see. :)

## Project Overview:

When it's at 1.0, this project will let you:
- Manage an email list, using best practices for deliverability
- Host a website, with pages and blog posts
- Sell downloadable digital products
- Sell hosted digital products, including customer authentication and secure data storage
- Understand what pages are generating the most traffic
- Create shortened URLs for sharing with social media
- Show up on Google and other search engines with good visibility
- Test different versions of content on your site
- Share posts to social media
- Protect your sanity against trolls and abusive people
- Export and backup every bit of data in the system.  Import it back again.

It won't ever let you:
- Spam people who haven't fully consented to receive your mailings
- Personally identify a single site visitor
- Include creepy tracking software like the Facebook pixel.
- Track whether people have opened the messages you've sent.
- Break GDPR or similar laws


Some core principles that set it apart:

**Real email.**<br/>
Engaged subscription, built on active, positive consent and auto-unsubscribing.

Get amazing deliverability and response by sending emails only to people who have shown you that they're interested and want to keep hearing from you.

**Fast.**<br/>
Built around the very best practices, and without all the bulk of tracking software, your site renders _fast_.  Like you won't see the screen refresh fast.  On mobile and desktop.

**Complete.**<br/>
One of the big trends has been having a specialized system for everything, and plugging them into each other.  But that means your and your customer's data is spread out in a dozen places you can't control.  Inkshop bucks that trend, and puts everything you need in one user-friendly place.

**Compliant.**<br/>
Inkshop does things the right way, and so you'll automatically comply with current - and future - privacy regulation.


## Current status:

[![TravisCI](https://travis-ci.org/inkandfeet/inkshop.svg?branch=master)](https://travis-ci.org/inkandfeet/inkshop)


I'm bootstrapping this project on my own site, [Ink and Feet](https://inkandfeet.com).   It's currently running my [mailing list](https://inkandfeet.com/letter) on it (but not my site yet). However, unless you're a professional programmer or super risk tolerant, I wouldn't advise you move your list over to it just yet.  It's been two weeks. Give it at least a month or two. :)

You can read more about the decision to move to inkshop in [this open letter.](https://inkandfeet.com/letter-april-28-2019-ants-being-watched-and-building-a-better-future)

I'll be moving from a setup with:
- Static site generated by inkblock, and served by Dreamhost and Cloudflare
- Mailing list managed by Ontraport
- Redirects and url shortening run by inkdots and Bitly.
- Analytics from Google Analytics and Woopra
- A/B testing from Optimizely
- Digital product sales managed by Ontraport and Teachery


Right now, it handles:
- Subscribe
- Create mailing lists
- Send message to a mailing list
- Import data
- Unsubscribe
- Love and positive consent
- Receive replies
- Create pages and posts
- Build templates for your website
- Add links (with thumbnails)
- Host static site resources


## Bootstrapping

```bash
git clone https://github.com/inkandfeet/inkshop.git
cd inkshop

cp env.sample .env
# Edit .env with your values

cp initial_data.yml.sample initial_data.yml
# Edit initial_data.yml with your basic information.

docker network create inkshop
docker-compose up
docker-compose run db bash
$ createdb inkshop -h db -U $POSTGRES_USER

# Load your initial data
docker-compose run inkshop python3 manage.py load_initial_data

```


## Running tests

Tests are wrapped with [polytester](https://github.com/skoczen/polytester).

One-offs:

```bash
docker-compose run inkshop pt
```

Development:

```bash
docker-compose run inkshop pt --autoreload
```


## Migrating from other services.

Ontraport:


```bash
python3 manage.py import_ontraport_csv --subscribers subscribers.csv --hard_bounce hard_bounces.csv  --newsletter my-newsletter
```


## Opinionated, and built on:
- [Pyca Cryptograpy](https://github.com/pyca/cryptography) for encryption.
- Cloudflare for DNS, Caching, and Development redirects
- Mailgun for email sending.
- AWS S3 for uploads and static file serving.
- Postgres for database.
- Redis for caching and queuing.
- Docker for encapsulation and dev ease.
- Heroku for deployment.



## Current working list

Next Week:
- handle subscribes between scheduling and sending
- delete flow finished
- poll mailgun (or webhook) for hard bounces
- add fallback gif
- scale down workers
- Move all inkmail helpers to tasks?  Think about abstraction this.
- Auto-delete any un-clicked confirmations after 7 days.
- Handle if people click them later, make sure we never delete people who were already subscribed, etc.


## Open threads the architecture isn't decided on yet.
- Repackage for production w/ Docker? https://github.com/caktus/dockerfile_post/
- How are replies in app handled?  [Prior art](https://medium.com/issacaption/using-a-custom-domain-in-gmail-for-free-with-mailgun-and-sendgrid-2c54e681f378)
- Structure for GDPR dump.  JSON?  Zip?
- Structure for full-system export/import.  JSON?  Zip?
- Import flow for people who don't have double-opt-in records.
