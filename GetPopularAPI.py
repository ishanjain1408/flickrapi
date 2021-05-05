import requests
import json
import jsonschema

#apikey = 13552988ea3e15aefe8b12c3caefab72
#secretkey = 8c74187139654cc2

base_url = 'https://www.flickr.com/services/rest/?format=json&nojsoncallback=1'
method = 'method=flickr.photos.getPopular'
api_key = 'api_key=13552988ea3e15aefe8b12c3caefab72'
user_id = 'user_id=125877475@N06'

test_url = base_url+"&"+method+"&"+api_key+"&"+user_id

response = requests.get(test_url)
if(response.status_code != 200):
    print("Status not OK")
else:
    print("Status OK")
    j = response.json()
    json_response = json.dumps(j)
    validschema = {
                "type": "object",
                "required": ["photos","stat"],
                "properties": {
                    "photos": {
                        "type": "object",
                        "required": ["page", "pages", "perpage", "total", "photo"],
                        "properties": {
                            "page": {"type": "integer"},
                            "pages": {"type": "integer"},
                            "perpage": {"type": "integer"},
                            "total": {"type": "integer"},
                            "photo": {"type": "array",
                                "items": {"anyOf": [{
                                    "type": "object",
                                    "required": ["id","owner","secret","server","farm","title","ispublic","isfriend","isfamily"],
                                            "properties": {
                                                "id": {"type": "string"},
                                                "owner": {"type": "string"},
                                                "secret": {"type": "string"},
                                                "server": {"type": "string"},
                                                "farm": {"type": "integer"},
                                                "title": {"type": "string"},
                                                "ispublic": {"type": "integer"},
                                                "isfriend": {"type": "integer"},
                                                "isfamily": {"type": "integer"}
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "stat": {"const": "ok"}
                }
            }

    def validateJson(Data):
        try:
            jsonschema.validate(instance=Data, schema=validschema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    jsonData = json.loads(json_response)
    isValid = validateJson(jsonData)
    if isValid:
        print("Given JSON data is Valid")
        print(jsonData)    
    else:
        print("Given JSON data is Invalid")