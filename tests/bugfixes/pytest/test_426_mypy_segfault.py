import time
import requests
import json
import unittest
import re
import httpretty


class GenerateTests(type):

    def __init__(cls, name, bases, attrs):
        if name in ('GenerateTestMeta',):
            return

        count = getattr(cls, '__generate_count__', attrs.get('__generate_count__')) or 100
        generate_method = getattr(cls, '__generate_method__', attrs.get('__generate_method__'))

        if not generate_method:
            raise SyntaxError(f'Metaclass requires def `__generate_method__(test_name):` to be implemented')


        for x in range(count):
            test_name = "test_{}".format(x)
            def test_func(self, *args, **kwargs):
                run_test = generate_method(test_name)
                run_test(self, *args, **kwargs)

            test_func.__name__ = test_name
            attrs[test_name] = test_func
            setattr(cls, test_name, test_func)


class TestBug426MypySegfaultWithCallbackAndPayload(unittest.TestCase, metaclass=GenerateTests):
    __generate_count__ = 1000

    def __generate_method__(test_name):
        @httpretty.httprettified(allow_net_connect=False)
        def test_func(self):
            httpretty.register_uri(httpretty.GET, 'http://github.com', body=self.json_response_callback({"kind": "insecure"}))
            httpretty.register_uri(httpretty.GET, 'https://github.com', body=self.json_response_callback({"kind": "secure"}))
            httpretty.register_uri(httpretty.POST, re.compile('github.com/.*'), body=self.json_response_callback({"kind": "regex"}) )

            response = requests.post(
                'https://github.com/foo',
                headers={
                    "Content-Type": "application/json"
                },
                data=json.dumps({test_name: time.time()}))

            assert response.status_code == 200

            try:
                response = requests.get('https://gitlab.com')
                assert response.status_code == 200
            except Exception:
                pass

        return test_func

    def json_response_callback(self, data):

        payload = dict(data)
        payload.update({
            "time": time.time()
        })

        def request_callback(request, path, headers):
            return [200, headers, json.dumps(payload)]

        return request_callback

class TestBug426MypySegfaultWithEmptyMethod(unittest.TestCase, metaclass=GenerateTests):
    __generate_count__ = 1000

    def __generate_method__(test_name):
        @httpretty.httprettified(allow_net_connect=False)
        def test_func(self):
            pass

        return test_func
