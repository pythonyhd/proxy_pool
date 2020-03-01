# -*- coding: utf-8 -*-
import execjs


def run_decode_js(text):
    with open('./decodeip.js', 'r', encoding='utf-8') as f:
        source_js = f.read()
        js_parttern = execjs.compile(source_js)
        result = js_parttern.call('decode', text)
        return result


if __name__ == '__main__':
    conn = run_decode_js('ZwVlYwV0BF4lZmthZGZ4')
    print(conn)