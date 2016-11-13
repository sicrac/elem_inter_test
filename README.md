# BACKGROUND

Since this is not a server thought to be responsive but instead optimized for mobile
applications, it doesn't make sense to keep the original images pointed by the url in the csv file
(and use an approach based for example on `django-imagekit`).
Images will be thus edited on the fly during downloading and saved on the desired size directly.

Being those image supposed to be used by mobile devices it is not about large images,
therefore storing  them as blob fields in the database, supposing perhaps to improve performances
by using for example a file system cache, it would be a reasonable solution.  
However, lacking sympathy for digital data blobbed in relational databases, i still chosen to store images in the file system directly.
In the event that it becomes necessary using of multiple servers in load balancing to cope with a huge amount of requests,
we might use a distributed key value database for storing the images.

# ASSUMPTIONS ABOUT CSV DATA

The sometimes incorrect structure of the csv file requires me to make some assumptions.

1. The extra information erroneously entered in a title can be found only after a comma: **those information will be ignored**.  
2. Extra lines may be contained in a title after the title itself: **those lines will be ignored**.  
3. The extra information in a description can be found only within an html `i` tag: **those information will be preserved (while the `i` tag stripped)**.  
4. The description may mistakenly be contained inside the html `b` tag: **those information will be preserved (while the `b` tag stripped)**.  

# SET UP

`git clone https://github.com/zimonc/elem_inter_test.git`  
`cd elem_inter_test`  
`virtualenv env`  
`source env/bin/activate`  
`pip install -r requirements.txt`  
`fab select_settings:env=dev`
`python manage.py test`  
`python manage.py migrate`
`python manage.py load_csv`
`python manage.py runserver`

About the `select_settings` fab command, there are 4 valid environment: **dev**, **tst**, **acc**, **prd**.
Only the **dev** one is working.

The operation of downloading csv data and related images is implemented by a custom **django-admin** command whose name is `load_csv`:

`python manage.py load_csv [--url <csv_url>] [--preserve]`

If no url is specified, a default one will be taken (that of the test).


# REST API

It exposes resources for two operations:

  - **Search images by title and or description**
  - **Get raw image data**

### Search images by title and or description

> METHOD `GET`  
> PATH `/api/images`  
>  QUERY STRING `search=<search>`

`search` is a sequence of alphanumeric characters

It returns a response of type application/json and content as following:

`[{"id":126,"title":"Item 1","description":"Description 1","image":"126.png"}, ... ,{"id":144,"title":"Item 19","description":"Description 19","image":null}]`

### Get raw image data

> METHOD `GET`  
> PATH `/api/images/<id>`

It returns a response of type `image/*`
