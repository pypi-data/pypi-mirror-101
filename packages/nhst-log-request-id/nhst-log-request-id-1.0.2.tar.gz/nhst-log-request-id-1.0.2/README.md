nhst-log-request-id
=====================

**Django middleware and log filter to attach a unique ID to every log message generated as part of a request.**

**Author:** This repository forked and updated form here [github](https://github.com/dabapps/django-log-request-id) written by Jamie Matthews, [@j4mie](https://twitter.com/j4mie)

-------

```
DEBUG [33031a43fc244539895fef70c433337e] myproject.apps.myapp.views: Doing something in a view
DEBUG [33031a43fc244539895fef70c433337e] myproject.apps.myapp.forms: The form validated successfully!
DEBUG [33031a43fc244539895fef70c433337e] myproject.apps.myapp.models: Doing some model magic
DEBUG [33031a43fc244539895fef70c433337e] myproject.apps.myapp.views: Redirecting to form success page
```

How?
----

**The request ID is stored in a thread local**. Use of thread locals is not generally considered best practice for Django applications, but seems to be the only viable approach in this case. Pull requests with better ideas are welcome.

Installation and usage
----------------------

First, install the package: `pip install nhst-log-request-id`

Add the middleware to your `MIDDLEWARE_CLASSES` setting. It should be at the very top.

```python
MIDDLEWARE_CLASSES = (
    'nhst_log_request_id.middleware.RequestIDMiddleware',
    # ... other middleware goes here
)
```

Add the `nhst_log_request_id.filters.RequestIDFilter` to your `LOGGING` setting. You'll also need to update your `formatters` to include a format with the new `request_id` variable, add a handler to output the messages (eg to the console), and finally attach the handler to your application's logger.

If none of the above made sense, study [Django's logging documentation](https://docs.djangoproject.com/en/dev/topics/logging/).

An example `LOGGING` setting is below:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'nhst_log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(correlationId)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
```

And following settings for consistant log messages across other projects

```
LOG_REQUEST_ID_HEADER = 'HTTP_X_CORRELATION_ID'
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = 'X-Correlation-Id'
REQUEST_ID_PROPERTY_NAME = 'correlationId'
```

You can then output log messages as usual:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("A wild log message appears!")
```

To check `json` object of final log which will be sync with `ELK Stack` in local, add following line in you `local.py` setting

```
LOGGING["handlers"]["console"]['formatter'] = "json"
```

And in browser, you can see `X-Correlation-Id:` in response header of any request which coming through configured pipeline.

Ougoing request from django app
-------------------------------

To include `correlationId` in ougoing request from configured django app to other app, we can access current `correlationId` from `local` object of `nhst_log_request_id` package. You can modify request header of outgoing request in a centralize place.

import this in you code:

```
from nhst_log_request_id import DEFAULT_REQUEST_ID_PROPERTY_NAME, REQUEST_ID_PROPERTY_NAME_SETTING, REQUEST_ID_RESPONSE_HEADER_SETTING, local
```

and modify request before sending request:

```
if(local):
    header_property = getattr(settings, REQUEST_ID_RESPONSE_HEADER_SETTING)
    request_id_property_name = getattr(settings, REQUEST_ID_PROPERTY_NAME_SETTING, DEFAULT_REQUEST_ID_PROPERTY_NAME)
    self.headers[header_property] = local.__dict__.get(request_id_property_name,'none')
```

License
-------

Copyright © 2012-2018, DabApps.

All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
