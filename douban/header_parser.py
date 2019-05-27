import json

def header_parser(basic_header):
    tmp_headers = {}
    tmp_cookies = {}
    for line in basic_header:
        item = line.split(':')
        if not 'Cookie' in line:
            # print(line.split(':'))
            tmp_headers[item[0]] = item[-1].strip()
        else:
            sub_item = item[-1].split(';')
            # print(sub_item)
            for sitem in sub_item:
                scookies = sitem.strip().split('=', maxsplit=1)
                tmp_cookies[scookies[0]] = scookies[-1]
    return tmp_cookies, tmp_headers


if __name__ == '__main__':
    # tmp_headers = {}
    # tmp_cookies = {}
    # with open('./tmp/header_2', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # print(lines)
    # for line in lines:
    #     item = line.split(':')
    #     if not 'Cookie' in line:
    #         print(line.split(':'))
    #         tmp_headers[item[0]] = item[-1].strip()
    #     else:
    #         sub_item = item[-1].split(';')
    #         print(sub_item)
    #         for sitem in sub_item:
    #             scookies = sitem.strip().split('=', maxsplit=1)
    #             tmp_cookies[scookies[0]] = scookies[-1]
    # print(json.dumps(tmp_headers, indent=4))
    # print(json.dumps(tmp_cookies, indent=4))
    pass