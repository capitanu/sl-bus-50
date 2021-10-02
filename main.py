import query


def main():
    api_key_file = open("api_key", 'r')
    api_key = api_key_file.readlines()[0]
    returned_data = query.get_data(api_key, 60)
    parsed_data = query.query_parser(returned_data)
    print(parsed_data)
main()
