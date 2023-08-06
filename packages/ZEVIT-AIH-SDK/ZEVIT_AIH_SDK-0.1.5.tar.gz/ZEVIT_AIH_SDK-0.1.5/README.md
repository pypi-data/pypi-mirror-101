# Introduction 
This project makes it possible to easily interact with the objects in AIH's Asset Integrity Hub.

Project is divided structured as follows:

```
AIH_SDK
├── AIHClient
├── v1
│   ├── Annotation
│   ├── Assessment
│   ├── Deviation
│   ├── Media
│   ├── MediaReference
│   ├── PanoramaImage
│   ├── PanoramicTour
│   └── WorkorderItem
├── v2
│   ├── DataProcessing
│   │   ├── Job
│   │   └── JobConfiguration
│   └── Assets
│   │   ├── Equipment
│   │   └── MainSystem

```

# Getting Started
1.	Install by: pip install ZEVIT-AIH-SDK
2.	Initialize AIHClient by: AIH_SDK.AIHClient.AIHClient(environment_to_connect_to, client_id, client_secret)
3.	Get objects from v1 and v2 APIs. Example of getting a main system: mainsystem = AIH_SDK.v2.MainSystem.MainSystem().get(guid)
4.	objects supports CRUD operation in form of get, post, put, and delete.

# Object design
Objects store the information fetch from the APIs in the self.value

self.value can either be a dict containing one instance or be a list containing multiple dicts, representing multiple objects

Objects all contain following methods:
* get()
* put()
* post()
* delete()
* get_value()
* update_values()
* to_dataframe()
* from_dataframe()
* inner_join()