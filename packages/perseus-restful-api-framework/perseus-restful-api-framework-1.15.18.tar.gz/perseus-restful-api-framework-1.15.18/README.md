# Perseus: RESTful API Server Framework

Perseus is a Python framework for quickly building RESTful API servers with minimal effort.

Perseus provides an initial set of core services that supports the following features:

- Client application registration with API keys generation
- Client application access control with RESTful request signature
- Client application and RESTful API server version compatibility check
- User authentication and session management
- Team/group management
- RESTful request logging with data sensitiveness support
- RESTful service automatic discovery
- HTTP request query parameters & body JSON message automatically parsing (depending on the HTTP method used) with data type check and conversion

Perseus is based on [Tornado](https://www.tornadoweb.org/) for handling client network connection.

## RESTful API Request Handler

```python
from majormode.perseus.service.base_http_handler import HttpRequest
from majormode.perseus.service.base_http_handler import HttpRequestHandler
from majormode.perseus.service.base_http_handler import http_request

import AttendantService


class AttendantServiceHttpRequestHandler(HttpRequestHandler):
    @http_request(r'^/attendant/session$',
                  http_method=HttpRequest.HttpMethod.POST,
                  authentication_required=False,
                  sensitive_data=True,
                  signature_required=False)
    def sign_in(self, request):
        email_address = request.get_argument(
            'email_address',
            data_type=HttpRequest.ArgumentDataType.email_address,
            is_required=True)

        password = request.get_argument(
            'password',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        return AttendantService().sign_in(request.app_id, email_address, password)
```

## Run the RESTful API Server Process

```bash
$ fab configure && fab start
```

Hashtags/Topics: `#perseus` `#restful` `#api` `#server` `#framework` `#python`
