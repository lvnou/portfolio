import json
from pathlib import Path


################################################################
# Base class

class BaseClass:
    def _parse_json(self, json_file_path):
        try:
            setts = json.load(open(json_file_path,"r"))
        except Exception as ex:
            print("Error while parsing {}:".format(json_file_path))
            print(ex)
            raise ex
        return setts 
        
          
class SettedBaseclass(BaseClass):
    def __init__(self, json_file_path = None, setts = None):
        self._json_path = None
        if json_file_path is not None:
            setts = self._parse_json(json_file_path)
            self._json_path = Path(json_file_path)

        if setts is not None:
            self._parse_setts(setts)

    def _parse_var(self, var):
        if isinstance(var, str):
            if self._json_path is not None:
                var = var.replace("$json_dir$", str(self._json_path.parent))
        return var
        
    def _parse_setts(self, setts):
        """
        To overwrite
        """
        pass

################################################################

################################################################
# Base Handler        
        
class BaseHandler(BaseClass):
    _type_dict = dict()
    
    def __init__(self, requested_type):
        self._type = requested_type
        self._type_cls = self._type_dict[self._type]
        
    def get(self, *args, **kwargs):
        return self._type_cls(*args, **kwargs)
        
        
class SettedBaseHandler(BaseHandler):
    _type_field = "type"

    def __init__(self, json_file_path = None, setts = None):
        if json_file_path is not None:
            setts = self._parse_json(json_file_path)
            
        self._json = json_file_path
        _type = setts[ſelf._type_field]
        return super(SettedBaseHandler, self).__init__(_type)
    
    def get(self, *args, **kwargs):
        if isinstance(self._json, str):
            kwargs["json_file_path"] = self._json
        return super(SettedBaseHandler, self).get( *args, **kwargs)
        
################################################################
# Base Array

class BaseArray(BaseClass, dict):
    def __init__(self, array_type_handler):
        self._type = array_type_handler
        
class SettedBaseArray(BaseArray):
    def __init__(self, json_file_path, *args, **kwargs):
        super(SettedBaseArray,self).__init__(*args, **kwargs)
        
        setts = self._parse_json(json_file_path)
        for k, v in setts.items():
            self[k] = self._type(setts = v).get()


################################################################

