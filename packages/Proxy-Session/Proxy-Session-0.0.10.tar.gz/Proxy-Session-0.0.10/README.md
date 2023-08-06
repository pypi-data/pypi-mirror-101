# Proxy-Session

**Proxy-Session** is a python module, helps to make a reliable proxy request to a HTTP server.

## Version

The current version is `0.0.10`.

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
            the proxy url.
            On Failure after maximum attempts, it will return a Response object, having
            status_code -1 with empty content. The proxy url will be null in this case.
        '''
        ...
        ...
    ...
    ...
```

>> Later a better reference manual will be provided.

## Usage

```python
from proxy_session import ProxySession
from proxy_session import ProxySessionTimeout

if __name__ == '__main__':
    with ProxySession() as ps:
        response, proxy_addr = ps.make_request('https://httpbin.org/ip', timeout=ProxySessionTimeout.LONG_TIMEOUT, log=True)
        if response.status_code == 200:
            print(f'Response Content:\n{response.text}')
            print(f'Proxy URL: {proxy_addr}')
        else:
            print("Some error occurred")
            if response.status_code == -1:
                print("Could not find any better proxy server")
        
```

The above code generated the below output, when I tested it.

```output
Trying Proxy[https]: http://51.89.4.140:8118
Trying Proxy[https]: http://118.140.151.98:3128
Trying Proxy[https]: http://15.185.193.6:3128
Response Content:
{
  "origin": "15.185.193.6"
}

Proxy URL: http://15.185.193.6:3128
```

## License

Python module **Proxy-Session** comes with [MIT License](https://github.com/antaripchatterjee/Proxy-Session/blob/master/UNLICENSE).
