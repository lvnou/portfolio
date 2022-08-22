import jstyleson
from pathlib import Path
import io
import pandas as pd

################################################################
# Base class

class BaseClass:
    def _parse_json(self, json_file_path):
        try:
            setts = jstyleson.load(open(json_file_path,"r"))
        except Exception as ex:
            print("Error while parsing {}:".format(json_file_path))
            print(ex)
            print(open(json_file_path,"r").read())
            raise ex
            
        return setts 
        
   
    def _parse_df_from_text(self,text, cols = dict(), numeric_cols = []):
        
        buf = io.StringIO(text)
        df = pd.read_csv(buf, delimiter = "|", header = 0, comment = "#", dtype="str") #,skiprows=[1])
        
        df = df.dropna(how="all",axis=1)
        df = df.dropna(how="any",axis=0)

        for c in df.columns.values:
            cnew = c.strip()
            if cnew in cols: cnew = cols[cnew]
            df[cnew] = df[c].str.strip()
            if cnew != c:
                del df[c]
        
        df.reset_index(drop=True, inplace=True)
        
        def parse_numeric(x):
            if "%" in x:
                x=float(x.replace("%",""))/100.
            return float(x)
        for c in numeric_cols:
            df[c] = pd.to_numeric(df[c].apply(parse_numeric), downcast = "float")
                
        
        return df
        
          
class SettedBaseclass(BaseClass):
    _default_setts = dict()

    def __init__(self, json_file_path = None, setts = None):
        self._json_path = None
        if json_file_path is not None:
            self._json_path = Path(json_file_path)
            
        if setts is None:
            if json_file_path is not None:
                setts = self._parse_json(json_file_path)

        if setts is not None:
            setts_with_default = self._default_setts.copy()
            setts_with_default.update(setts)
            self._parse_setts(setts_with_default)

        return super(SettedBaseclass, self).__init__()

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
        _type = setts[self._type_field]
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
        
        if json_file_path is not None:
            setts = self._parse_json(json_file_path)
            for k, v in setts.items():
                self[k] = self._type(setts = v).get(json_file_path = json_file_path, setts = v)


################################################################

