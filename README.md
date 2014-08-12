#Caesium Quickstart

[Caesium Project Homepage](http://www.github.com/urbn/Caesium)

The purpose of this project is to be a starting point for the Caesium python framework.

## Installation

- Ensure that mongodb is running in your environment.
- bash install.sh
- source venv/bin/activate
- python app.py
- For auto reload while developing, add --debug

See app.py for implementation.

##Scheduling
Requests that you want to schedule should have a "ttl" header with a UTC
timestamp as the value for the time you would like this document to be scheduled.

Scheduled actions map to RESTful verbs, POST with ttl would be a scheduled insert, PUT with ttl is a scheduled PATCH to the object,
and DELETE with ttl is a scheduled delete.  Deletes do not delete from the revisions collection for that object type.

##Example Scheduled Requests Flow

In the following flow, we will create a new resource, update it with a scheduled patch, Get it again to see those changes, then delete.

POST /comment

Headers:
- Content-Type: application/json
- ttl: 1401678643

```
{
    "title": "Comment Title",
    "comment": "Check out this new awesome comment",
    "id": "53ea6636717cc88c7b499a54"
}
```

PUT /comment/53ea6636717cc88c7b499a54

Headers:
- Content-Type: application/json
- ttl: 1401678643

```
{
    "title": "My Comment Title Update",
    "new_attribute": 12345
}
```

GET /comment/53ea6636717cc88c7b499a54
```
{
    "id": "53ea6636717cc88c7b499a54",
    "title": "My Comment Title Update",
    "comment": "Check out this new awesome comment",
    "new_attribute": 12345
}
```

DELETE /comment/53ea6636717cc88c7b499a54

Headers:
- ttl: 1401678643

###Non-Scheduled Requests

If you want to use Caesium synchronously, it is entirely ok to just remove the "ttl" header and the request will be actioned
immediately without creating a revision.  Very similar to how a standard API works on a RESTful resource.

Also see:
- http://www.tornadoweb.org/en/stable/
- http://motor.readthedocs.org/en/stable/index.html

