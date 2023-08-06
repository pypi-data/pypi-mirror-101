# Python wrapper for the mobilitylabs API
This repo contains a Python library with some classes to easily access the [mobilitylabs API](https://apidocs.emtmadrid.es/) which allows the access to the **BusEMTMad**, **BiciMAD Go** and **ParkingEMTMad** services among others. These services are part of the [MobilityLabs Madrid](https://mobilitylabs.emtmadrid.es/en) open and interoperable platform.

In addition to the Python wrapper **some test applications are included**; this will help to let you know how everything works and, on top of that, you can use it to interact with the service once you get your own credencials and store them in the `credentials.ini` file.

The following are the requirements needed to make it work:

- **Python 3** (3.7.3+)
- A **XClientID** and **passkey** in order to use the services; you can get your own XClientID and passkey by following the steps outlined in [Create an application in the EMTing portal](https://mobilitylabs.emtmadrid.es/en/doc/new-app), which is reduced down to:
  1. Creating your own **developer account**
  2. Creating an **EMTing Application**

This Python library has been successfully tested with [OSBDET S21R1](https://github.com/raulmarinperez/osbdet/tree/vs21r1) on a Debian 10 x64 host.

Remember to add the library to the **PYTHONPATH environment variable** if you want to use it from your code or if you want to run the tests Python scripts; you can do so by running the following line within the folder where the repo was cloned:

```
$ export PYTHONPATH=$PYTHONPATH:`pwd`
```
If you want to persist this environment variable, **add it to your user's profile** and it'll be created everytime you log into your computer.

## BusEMTMad
The `BusEMTMad` class allows you to leverage information about buses in the great city of Madrid, which is provided by the EMT (Empresa Municipal de Transportes); this class wrapps the [Block 3 TRANSPORT BUSEMTMAD](https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD) section in the official documentation, although not all the functions/webmethods are wrapped.

The following are the functions/webmethods wrapped at the moment:

- **info_lines(date_ref) -** It returns the list of active bus lines in the reference date.
- **info_line(line_id, date_ref) -** It returns detailed info of a specific bus line in the reference date.
- **info_stops() -** It returns the list of active bus stops and information about them.
- **info_stop(stop_id) -** It returns detailed info of a specific bus stop.
- **line_stops(line_id,direction) -** It returns the list of bus stops of a bus line keeping in mind the direction (1 - start to end, 2 - end to start)
- **issues(line_id) -** It returns details about incidents or issues identified and impacting bus lines.
- **buses_arrivals(stop_id, line_id="") -** It returns the real time estimation of how far the buses are from the stop and how much time will take them to get to the bus stop. Only buses from the line specified will be considered (*lineId is optional*).

`test_busemtmad.py` let you test this service easily; before you can use it, get your own XClientID and passkey and store them into the `credentials.ini` file. `test_busemtmad.py -h` will give you all the details on how to run it:

```
$ tests/test_busemtmad.py -h
usage: test_busemtmad.py [-h] [-lid LINEID] [-sid STOPID] [-dir {1,2}]
                         {info_lines,info_line,info_stops,info_stop,line_stops,issues,buses_arrivals} credentials_file

positional arguments:
  {info_lines,info_line,info_stops,info_stop,line_stops,issues,buses_arrivals}
                        what is going to be requested to the BusEMTMad service
  credentials_file       path to the file with info to access the service

optional arguments:
  -h, --help            show this help message and exit
  -lid LINEID, --line_id LINEID
                        bus line identifier for actions 'info_line', 'line_stops' and 'issues'; this argument is optional
                        for action 'buses_arrivals'
  -sid STOPID, --stop_id STOPID
                        stop identifier for action 'info_stop' and 'buses_arrivals'
  -dir {1,2}, --direction {1,2}
                        direction to be considered to analyze line info for action 'line_stops'; 1 for start to end, 2
                        for end to start
```


## BiciMAD Go
The `BiciMad` class allows you to leverage information about bikes and bike stations in the great city of Madrid, which is provided by the BiciMAD GO service; this class wrapps the [Block 4 TRANSPORT BICIMAD](https://apidocs.emtmadrid.es/#api-Block_4_TRANSPORT_BICIMAD) section in the official documentation, although not all the functions/webmethods are wrapped.

The following are the functions/webmethods wrapped at the moment:

- **info_bike_stations() -** It returns the details of Madrid BiciMad Stations.
- **info_bike_station(bike_station_id) -** It returns the details of a specific Madrid BiciMad Station.
- **info_bikes() -** It returns the details of Madrid BiciMad bikes.
- **info_bike(bike_id): -** It returns the details of a specific bike from the Madrid BiciMad service.

`test_bicimad.py` let you test this service easily; before you can use it, get your own XClientID and passkey and store them into the `credentials.ini` file. `test_bicimad.py -h` will give you all the details on how to run it:

```
$ tests/test_bicimad.py -h
usage: test_bicimad.py [-h] [-sid BIKESTATIONID] [-bid BIKEID]
                       {info_bike_stations,info_bike_station,info_bikes,info_bike} credentials_file

positional arguments:
  {info_bike_stations,info_bike_station,info_bikes,info_bike}
                        what is going to be requested to the BiciMAD GO service
  credentialsFile       path to the file with info to access the service

optional arguments:
  -h, --help            show this help message and exit
  -sid BIKESTATIONID, --bike_station_id BIKESTATIONID
                        bike station identifier for action 'info_bike_station'
  -bid BIKEID, --bike_id BIKEID
                        bike identifier for action 'info_bike'
```

## ParkingEMTMad
The `ParkingEMTMad` class allows you to leverage information about parking areas in the great city of Madrid, which is provided by the EMT (Empresa Municipal de Transportes); this class wrapps the [Block 5 PARKINGS](https://apidocs.emtmadrid.es/#api-Block_5_PARKINGS) section in the official documentation, although not all the functions/webmethods are wrapped.

The following are the functions/webmethods wrapped at the moment:

- **info_parkings() -** It returns the list of active parking areas operated by the EMT.
- **info_parking(parking_id) -** It returns the details of a specific parking area.
- **availability() -** It returns availability for those parking areas publishing this information. Not all of them make this information public.

`test_parkings.py` let you test this service easily; before you can use it, get your own XClientID and passkey and store them into the `credentials.ini` file. `test_parkings.py -h` will give you all the details on how to run it:

```
$ tests/test_parkings.py -h
usage: test_parkings.py [-h] [-id PARKINGID] {info_parkings,info_parking,availability} credentials_file

positional arguments:
  {info_parkings,info_parking,availability}
                        what is going to be requested to the ParkingEMTMad service
  credentialsFile       path to the file with info to access the service

optional arguments:
  -h, --help            show this help message and exit
  -id PARKINGID, --parking_id PARKINGID
                        parking area identifier for action 'info_parking'
```

## Changelog
- **v0.1 (20210410) -** initial release.
