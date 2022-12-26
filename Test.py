import json
from collections import namedtuple
from collections import OrderedDict

GIF = namedtuple('GIF', 'Header LSD')
Header = namedtuple('Header', 'Version')
LSD = namedtuple('LSD', 'Width')

root = GIF()
t = Token('ABC', 'DEF', t2)

def namedtuple_asdict(obj):
  if hasattr(obj, "_asdict"): # detect namedtuple
    return OrderedDict(zip(obj._fields, (namedtuple_asdict(item) for item in obj)))
  elif isinstance(obj, str): # iterables - strings
     return obj
  elif hasattr(obj, "keys"): # iterables - mapping
     return OrderedDict(zip(obj.keys(), (namedtuple_asdict(item) for item in obj.values())))
  elif hasattr(obj, "__iter__"): # iterables - sequence
     return type(obj)((namedtuple_asdict(item) for item in obj))
  else: # non-iterable cannot contain namedtuples
    return obj

print(json.dumps(namedtuple_asdict(t)))
