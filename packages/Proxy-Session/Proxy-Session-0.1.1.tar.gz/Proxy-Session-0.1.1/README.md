# Proxy-Session

**Proxy-Session** is a python module, helps to make a reliable proxy request to a HTTP server.

## Version

The current version is `0.1.1`.

## Installation

### Using git

```bash
git clone https://github.com/antaripchatterjee/Proxy-Session
cd Proxy-Session
python setup.py install
```

### Using pip

```bash
pip install Proxy-Session
```

## Uninstallation

```bash
pip uninstall proxy_session
```

## Platform Support

This is a cross-platform python module, provided the version of the python interpreter should be 3.6+.

## API Reference

```python
import requests
...
...

class ProxySession(requests.Session):
    def __init__(self, user_=None, pass_=None, socks=False):
        '''
        @param user_: str[None] -> Username for proxy authentication
        @param pass_: str[None] -> Password for proxy authentication
        @param socks: bool[False] -> If True, it will perform a socks5
                authentication, given the user_ and pass_ has been
                provided. If False, it will perform a basic authent-
                ication will be performed, provided the value of
                user_ and pass_.
        '''
        super(ProxySession, self).__init__()
        ...
        ...
    ...
    ...
    def make_request(self, url, method='GET', timeout=ProxySessionTimeout.SHORT_TIMEOUT, log = True, max_attempt = 100, **kwargv):
        '''
        @param url: str -> The target URL
        @param method: str[GET] -> The HTTP method to be called
        @param timeout: int[5] -> The timeout value, for the proxy request
        @param log: bool[True] -> It will log the necessary information
        @param max_attempt: int[100] -> Maximum number of attempt to reach the target URL,
                must be a positve integer
        @param **kwargv -> Other keyword arguments, which will be passed to requests.request
                method
        
        @return -> It will always return the tuple of two element, response and proxy_url
                On success, it will return the reponse object, returned by the method call and
                the proxy url. If the random proxy selection is made, it will return the proxy
                url as a string, otherwise it will be same as keyword argument "proxies". 
                On Failure after maximum attempts, it will return a Response object, having
                status_code -1 with empty content. The proxy url will be null in this case.
        '''
        ...
        ...
    ...
    ...
```

Find the full source code from [GitHub](https://github.com/antaripchatterjee/Proxy-Session/blob/master/proxy_session/session.py).

If you need to make a request using `socks` proxy, make sure you install [PySocks](https://pypi.org/project/PySocks/). Alternatively just run the below command.

```python
pip install requests[socks]
```

If you pass keyword argument `proxies` to the `ProxySession.make_request` method(like `requests.request(...)`), it will prevent any random proxy selection.

The random proxies are scrapped from [Free Proxy List - Just Checked Proxy List](https://free-proxy-list.net/). This module provides a reliable way to find a free and live proxy server, however, it does not evaluate any security of the proxy server, so it does not guarantee you about your personal and/or confidential data. It is always better to use a paid proxy, instead of a free proxy.

## Usage

```python
from sys import stderr
from proxy_session import ProxySession
from proxy_session import ProxySessionTimeout

if __name__ == '__main__':
    with ProxySession() as ps:
        error_ = ps.error
        if error_:
            print('Error Status: ', error_[0], file=stderr)
            print('Error:\n' + error_[1], file=stderr)
        response, proxy_addr = ps.make_request('https://httpbin.org/ip', timeout=ProxySessionTimeout.LONG_TIMEOUT, log=True)
        if response.status_code == 200:
            print(f'Response Content:\n{response.text}')
            print(f'Proxy URL: {proxy_addr}')
        else:
            print(f'{response}')
              
```

The above code generated the below output, when I tested it.

```output
Trying random free proxy[https]: http://103.109.58.102:46523
Trying random free proxy[https]: http://157.230.103.189:36366
Trying random free proxy[https]: http://85.15.152.39:3128
Response Content:
{
  "origin": "85.15.152.39"
}

Proxy URL: http://85.15.152.39:3128
```

## License

Python module **Proxy-Session** comes with [MIT License](https://github.com/antaripchatterjee/Proxy-Session/blob/master/LICENSE).
