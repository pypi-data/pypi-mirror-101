from json import dumps

json_content_array = ['https://cloud.kili-technology.com/api/label/v2/files?id=5b24cc51-8b50-4949-b3c3-08e02e285573', 'https://cloud.kili-technology.com/api/label/v2/files?id=fccaf568-f3f9-4a73-bac5-3ac02c9558be']

formatted_json_content_array = list(map(lambda json_content: dumps(
                dict(zip(range(len(json_content)), json_content))), json_content_array))

print(formatted_json_content_array)