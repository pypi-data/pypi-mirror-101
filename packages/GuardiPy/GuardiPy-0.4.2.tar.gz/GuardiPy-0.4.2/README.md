# GuardiPy

GuardiPy is a Guardicore Centra™ API client
    
    currently under development,
    written around api v3.0,
    under release 35.x,
    static-declared,
    for Python 3.6+,
    type-hinted.

# Howto

GuardiPy can be install by running the following command:
```
pip install GuardiPy
```

You can find examples as the library is developed in (the commit history of?) `./scratch_testing.py`.
There are two parts of the library you will primarily use:

- `GuardiPy.Centra` is the connection/session object. Start here.
    - Call `.execute()` on this to perform actions against the API.
      - Results from `.execute()` are returned as a list of objects.
      - Objects can be converted to native Python dictionaries using the `.convert_to_dictionary()` method.
    - Call `.export_to_csv()` on this to fetch CSV data from the API.
      - The optional `filename` parameter may be used to have the CSV data written to the provided `filename`
  
- `GuardiPy.CentraObject` is the directory of objects you can interact with.
    - Such as `.Incident`, `.Asset`, `.VM`, etc.
    - Within `CentraObject` there are (static) methods for performing API actions. Such as `.list()` to perform basic searching.
    - A `CentraObject` is initialized by the `.execute()` method, containing fields of that item. Such as the time of an incident.
    
- `GuardiPy.CentraObject.auxiliary_types` contains type definitions that the API documentation did not give a specific section to; and thus are considered not-very-(important/complex).

## Authentication

Authentication takes a hostname, username, and password.

First, create your client object, `gc` for example.

```python
from GuardiPy import Centra
gc = Centra(username="me", hostname="server", password="secret")
```

## Usage

To interact with the API, explore the Centra entities, such as `CentraObject.Incident`.

- When static (ie, `Incident`), these entities will contain methods (ie, `.list()` to search) meant to be passed to `Centra.execute()`.
  - Specifically, these return a `CentraApiPayload` or `CentraApiExportable` object.
    - The returned objects are meant to be fed directly to `Centra.execute()`.
    - `CentraApiExportable` objects may also be fed directly to `Centra.export_to_csv()` to generate a CSV file/string.
    - Generally, you don't have to deal with the payload helper object; it's for purposes internal to the library: describing the HTTP request to make, for your given query (ie: list), of a given object type (ie: Incidents).
    - However, it can be modified on the fly if you for some reason need to do so.

- When `Centra.execute()` makes your API call, it will return a list of objects from your search. These objects are instances of the class (ie, `Incident()`). The attributes (name, IP, timestamps, etc) are assigned to these objects.
  - This provides type hinting/autocompletion, so as you use this library, you will know what attributes are available to you**.
  - In some instances, this is undesirable. IE, if you need the JSON that makes up an object, nested entities (such as `Incident.affected_assets`) will return a brief description as text; instead of the JSON that makes up the affected assets in full...
  - To work around this, pass the `Incident` through `Centra.convert_to_dictionary`.
  - It, and all of it's children, will be serialized into a native Python dictionary (which can be modified if needed) before being passed to `JSON.dumps()`.
  
- When `Centra.export_to_csv()` makes your API call, it will return a string representation of the CSV file containing the results of your search.
  - If a `filename` argument is used when `.export_to_csv()` is called, the results of the search will also be written to the specified file.
  

```python
# [ continued from above ]

from GuardiPy import CentraObject

incident_query = CentraObject.Asset.list(
    asset_id="some-uu1d-g03s-her3",  # Most can either be a string,
    label_id=["required", "labels"],  # Or list of many strings.
)

assets = gc.execute(incident_query)
print(assets)

# Soon™:
# for asset in assets:
#     asset.do_something_to_it() ...?
```

# Output example
*[ Note: as of v0.1a, return types are implemented only for the `Incident` type (and it's children). For other types that are developed, there is a method available for converting API results to a dictionary, for easy JSON serialization. ]*

<details>
<summary>Example of returned Asset object</summary>

```python
{
    '_id': 'uuid obfuscated from here!',
    'active': True,
    'asset_id': 'uuid obfuscated from here!',
    'bios_uuid': 'uuid obfuscated from here!',
    'comments': '',
    'file_detection_rules': [],
    'first_seen': 1589471530555,
    'full_name': 'Network\\USER-NAME',
    'host_id': 'uuid obfuscated from here!',
    'host_orchestration_id': 'host-261',
    'id': 'uuid obfuscated from here!',
    'ip_addresses': ['10.1.2.3'],
    'is_on': True,
    'label_groups': [],
    'labels': [{'color_index': -1,
                'id': 'uuid obfuscated from here!',
                'key': 'vCenter host',
                'name': 'vCenter host: demo-esx2.company.local',
                'value': 'demo-esx2.company.local'},
               {'color_index': 1,
                'id': 'uuid obfuscated from here!',
                'key': 'Network',
                'name': 'Network: IT_Staff',
                'value': 'IT_Staff'},
               {'color_index': 0,
                'id': 'uuid obfuscated from here!',
                'key': 'Environment',
                'name': 'Environment: CompanyDemo',
                'value': 'CompanyDemo'},
               {'color_index': 1,
                'id': 'uuid obfuscated from here!',
                'key': 'Network',
                'name': 'Network: Vendor',
                'value': 'Vendor'},
               {'color_index': -1,
                'id': 'uuid obfuscated from here!',
                'key': 'vCenter folder',
                'name': 'vCenter folder: Something',
                'value': 'Network'}],
    'last_seen': 1601684867986,
    'mac_addresses': ['01:20:55:aa:aa:aa', 'aa:bb:cc:dd:ee:00'],
    'metadata': {'vSphere': {'host': 'demo-esx2.company.local',
                             'power_state': 'poweredOn',
                             'tools_running_status': 'guestToolsRunning',
                             'tools_version_status': 'guestToolsUnmanaged'}},
    'name': 'obfuscated string!',
    'nics': [{'cloud_network': None,
              'ip_addresses': ['10.1.5.200'],
              'is_cloud_public': False,
              'mac_address': 'aa:bb:cc:dd:ee:ff',
              'network_id': 'DemoLAN',
              'network_name': 'DemoLAN',
              'switch_id': 'vSwitch5',
              'vif_id': '0',
              'vlan_id': 0},
             {'cloud_network': None,
              'ip_addresses': [],
              'is_cloud_public': False,
              'mac_address': '11:22:33:44:55:66',
              'network_id': 'DemoLAN',
              'network_name': 'DemoLAN',
              'switch_id': 'vSwitch2',
              'vif_id': '1',
              'vlan_id': 0}],
    'orchestration_details': [{'orchestration_id': 'uuid obfuscated from here!',
                               'orchestration_name': 'DELETED',
                               'orchestration_obj_id': 'vm-12345',
                               'orchestration_type': 'vSphere',
                               'revision_id': 200609150340},
                              {'orchestration_id': 'uuid obfuscated from here!',
                               'orchestration_name': 'company demo',
                               'orchestration_obj_id': 'vm-54321',
                               'orchestration_type': 'vSphere',
                               'revision_id': 201003002040}],
    'orchestration_labels': [['vCenter host',
                              'demo-esx2.company.local'],
                             ['vCenter folder', 'Network']],
    'orchestration_labels_dict': {'vCenter folder': ['Network'],
                                  'vCenter host': ['demo-esx2.company.local']},
    'recent_domains': None,
    'replicated_labels': ['uuid obfuscated from here!',
                          'uuid obfuscated from here!',
                          'uuid obfuscated from here!'],
    'status': 'on',
    'tenant_name': 'Network',
    'vm': {'name': 'some name?',
           'orchestration_details': [{'orchestration_id': 'uuid obfuscated from here!',
                                      'orchestration_name': 'DELETED',
                                      'orchestration_obj_id': 'vm-20202020',
                                      'orchestration_type': 'vSphere',
                                      'revision_id': 200609150340},
                                     {'orchestration_id': 'uuid obfuscated from here!',
                                      'orchestration_name': 'company something',
                                      'orchestration_obj_id': 'vm-12345',
                                      'orchestration_type': 'vSphere',
                                      'revision_id': 201003002040}],
           'tenant_name': 'Network',
           'vm_id': 'uuid obfuscated from here!'},
    'vm_id': 'uuid obfuscated from here!',
    'vm_name': 'device name?'
}
```

</details>

## Type-flexible shortcutting

GuardiPy aims for type friendliness where possible.

Most filters that take a single string are also capable of taking a list of multiple strings - such as UUIDs or IP addresses to include in a given search.

Some methods use filters where a value can be implied through many different types. Such as searching for `CentraObject.Incident.list()`, you are required to specify a range of time to search (from, to).

The Centra API uses Unix Epoch (in milliseconds) for date-time values. To exemplify this type flexibility, where you want/need to specify a datetime value to the API, you can provide...
- Absolutely nothing: a default parameter is often assigned.
    - Such as searching "up until" the current UTC time:
```python
to_time: Union[datetime, timedelta, int, str] = datetime.utcnow()
#                                             ^ default parameter value.
```
- `int` (and `str`) will be assumed to be readily-formatted values in Epoch Milliseconds.
    - Such as taking a value from an API result and passing it right into another query.
    - TODO possibility: string parsing to determine such?

```python
Incident.list(from_time=1601090930584)
#                       ^ int example.
```
- `datetime.timedelta` will be **ADDED** to the current UTC time.
    - Literally, a timedelta object is added to "right now" at runtime.
    - That is to say: *"right now, plus timedelta of negative seven days, will equal 1 week ago."*
    - Remember: specify negative values or you will be looking into the future!
    - This allows you to lazily search for a range, such as querying "up to 3.5 days ago":

```python
Incident.list(to_time=datetime.timedelta(days=-3, hours=-12)
```
- Finally, a `datetime` native object...

```python
import dateutil.parser  # v  from RFC3339 datetime string.

some_time = dateutil.parser.isoparse('2008-09-03T20:56:35.450686Z')
Incident.list(to_time=some_time)
```

