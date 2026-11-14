---
source: https://ssp.imcce.fr/webservices/skybot/api/conesearch/
fetched: 2026-11-14
status: 200
---

SkyBoT - conesearch | LTE

SkyBoT
======

conesearch
----------

### Solar system objects identification

The method **`skybotconesearch`** is intended to people who need to
search for and identify Solar System objects (asteroids, planets, natural satellites and comets)
that are present in a field of view of given celestial coordinates and radius at a given epoch.

HTTP Request
------------

If you are a software/solutions developer, you might want to include the SkyBoT  **`skybotconesearch`**
service into your application. This can be done by using the [web service method](#webservice) or
by using the following HTTP request:

https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?[parameters]

where **[parameters]** is a list of parameters separated by the character `&`, which may be composed in two ways:

- standard Simple Cone Search [version 1.1](https://ivoa.net/documents/ConeSearch/20200828/) (SCS) interface
:   the parameters are encoded in the URL with standard keywords providing a J2000 right ascension and declination (in degrees)
    and the search radius (in degrees) of the requested field of view on the sky, as well as the epoch at which you are searching for
    solar system objects. These parameters are described in Table 1.

- non standard interface
:   the parameters are encoded in the URL with dedicated keywords providing the relevant information to search
    the solar system objects located in a given field of view. These parameters are described in Table 2.

If you choose to query SkyBoT using the SCS standard interface, you may also use the non standard keywords by adding
them before the standard ones.

Table 1: Simple Cone Search v1.1 interface

| Parameter | Definition | Unit | Limits |
| `TIME=<string>` | [Requested epoch](/webservices/skybot/howto/conesearch/#howto-epoch), expressed in Julian day or ISO dateTime | - | 2411320.0 .. 2473540.0 1889-11-13 12h .. 2060-03-21 12h |
| `RA=<double>` | J2000 Right ascension of the FOV center | degree | 0° .. 360° (decimal) |
| `DEC=<double>` | J2000 Declination of the FOV center | degree | -90° .. +90° (decimal) |
| `SR=<double>` | Radius of the FOV (\*) | degree | 0 .. 30° (decimal) |
| `MAXREC=<int>` | Maximum number of output results (\*). For unlimited output keep empty. | - | 0 .. n |
| `VERB=<int>` | Level of output parameters (optional) | - | 1, 2, 3 which correspond respectively to outputs `object, basic, all` |
| `RESPONSEFORMAT=<string>` | Mime type of the results | - | [votable](http://www.ivoa.net/Documents/latest/VOT.html) | html | text | json |

(\*) in accordance with protocol, if SR=0 or MAXREC=0 then only the
service metadata are returned (See [SCS doc](https://ivoa.net/documents/ConeSearch/20200828/)).

Table 2: Non standard interface

| Parameter | Definition | Unit | Limits |
| `-ep=<string>` | [Requested epoch](/webservices/skybot/howto/conesearch/#howto-epoch), expressed in Julian day or formatted as any [English textual datetime](http://php.net/manual/en/function.strtotime.php) | - | 2411320.0 .. 2473540.0 1889-11-13 12h .. 2060-03-21 12h |
| `-ra=<double>` | [Right ascension](/webservices/skybot/howto/conesearch/#howto-fovcenter) or ecliptic longitude of the FOV center | degree | 0° .. 360° (decimal) |
| `-dec=<double>` | [Declination](/webservices/skybot/howto/conesearch/#howto-fovcenter) or ecliptic latitude of the FOV center | degree | -90° .. +90° (decimal) |
| `-rs=<double> -rm=<double> -rd=<double>  -bs=<string> -bm=<string> -bd=<string>` | [Radius](/webservices/skybot/howto/conesearch/#howto-fovradius) of the FOV OR Size of the FOV as Δα x Δδ | arcsec arcmin degree  arcsec arcmin degree | 0 .. 36000 arcsec 0 .. 600 arcmin 0 .. 10 degrees  0 .. 72000 arcsec 0 .. 1200 arcmin 0 .. 20 degrees |
| `-mime=<string>` | Mime type of the results | - | [votable](http://www.ivoa.net/Documents/latest/VOT.html) | html | text | json |
| `-output=<string>` | Output parameters | - | object | basic | obs | all |
| `-observer=<string>` | [Observer's location](/webservices/skybot/howto/conesearch/#howto-observer) code | - | Optional parameter, default = 500 (geocenter) |
| `-filter=<double>` | Filter to retrieve only objects with a position error lesser than the given value. 0 implies no filter | arcsec | Optional parameter, default = 120 arcsec |
| `-objFilter=<string>` | [Code](/webservices/skybot/howto/conesearch/#howto-objFilter) to indicate which objects must be sought in the FOV | - | Optional parameter, default = 111 (all objects) |
| `-refsys=<string>` | Code to indicate the reference plane of coordinates | - | Optional parameter: EQJ2000 (default) | ECJ2000 |
| `-from=<string>` | Word which definite the name of the caller application, or which describes the request | - | Any short string (no space character) |

The output results are described in the following [section](#output-results), and are available
in [VOTable](https://www.ivoa.net/Documents/latest/VOT.html) (default), HTML, plain text format, and
[JSON](#json-format) object (cf. [examples](#examples)). Some arguments are optionnal and
their values can be omitted. In that case, the default values are used.

Web service
-----------

The SkyBoT Web service provides methods based on [SOAP](https://www.w3.org/TR/soap/) and
[HTTP POST](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5) verb which allow
one to interact between its own application and the SkyBoT service. Here is the useful information to
invoke the SkyBoT  **`skybotconesearch`** method:

Web Service URI:
:   [https://ssp.imcce.fr/webservices/skybot/skybot.php](/webservices/skybot/skybot.php)

Namespace:
:   https://ssp.imcce.fr/webservices/skybot

WSDL:
:   [https://ssp.imcce.fr/webservices/skybot/skybot.php?wsdl](/webservices/skybot/skybot.php?wsdl)

SOAP header:
:   name of the SOAP header element: `clientID`
:   SOAP header's content: `array('from' => 'YourName', 'hostip'=>'')`

Method:
:   skybotconesearch (inputArray)

The input parameter of the method is an array which must contained the following parameter:

| Variable | Type | Units | Limits or values | Default | Comment |
| --- | --- | --- | --- | --- | --- |
| `epoch` | string | - | 2411320.0 .. 2473540.0 1889-11-13 12h .. 2060-03-21 12h | none | [Requested epoch](/webservices/skybot/howto/conesearch/#howto-epoch), expressed in Julian day, ISO format or formatted as any [English textual datetime](http://php.net/manual/en/function.strtotime.php) |
| `alpha` | double | degree | 0° .. 360° (decimal) | none | [Right ascension](/webservices/skybot/howto/conesearch/#howto-fovcenter) or ecliptic longitude of the FOV center |
| `delta` | double | degree | -90° .. +90° (decimal) | none | [Declination](/webservices/skybot/howto/conesearch/#howto-fovcenter) or ecliptic latitude of the FOV center |
| `radius` | string | arcsec | 0 .. 108000 arcsec or 0 .. 216000 arcsec | none | [Radius](/webservices/skybot/howto/conesearch/#howto-fovradius) (single value) or sizes (<value> x <value>) of the FOV |
| `mime` | string | - | [votable](http://www.ivoa.net/Documents/latest/VOT.html) | html | text | json | votable | Mime type of the results |
| `output` | string | - | object | basic | obs | all | basic | Output parameters |
| `observer` | string | - | Code of observer's location | 500 | [IAU observatory](http://www.minorplanetcenter.net/iau/lists/ObsCodes.html) code or [observer's location](/webservices/skybot/howto/conesearch/#howto-observer) code |
| `filter` | double | arcsec | 0 implies no filter | 120 | Filter on the error of position: only targets with position error lesser that the given value are retrieved |
| `objFilter` | string | - | 100 | 010 | 001 | 110 | 101 | 011 | 111 | 111 | [Code](/webservices/skybot/howto/conesearch/#howto-objFilter) to indicate which objects must be sought in the FOV, respectively asteroids, planets and comets. |
| `refsys` | string | - | EQJ2000 | ECJ2000 | EQJ2000 | Code to indicate the reference plane of coordinates |

The output of the  `skybotconesearch` method is an object containing the following attributes:

'flag'
:   the status of the response: `flag=1` means ok; `flag=0` or `flag=-1` mean that an error occured

'status'
:   the HTTP status-code of the response (e.g. `400: bad request`, `422: Unprocessable Entity`, `500: internal error`)

'ticket'
:   the Unix timestamp of the response which can be useful to stamp the request

'result'
:   a string containing the ephemeris of the requested solar system body with the parameters described in
    the [output results](#output-results) section

Depending on the selected mime type, the output is formatted as:

votable
:   the data are written in the IVOA standard [VOTable](https://www.ivoa.net/Documents/latest/VOT.html) format

html
:   the data are transformed from VOTable to HTML by XSLT processing ([SkyBoT XSL style sheet](/webservices/skybot/skybot.xsl))

text
:   the data are returned in plain text where each value is separated by the pipe '|' character

json
:   the data are written in a [JSON](#json-format) object.

Query examples
--------------

Click on the following links to get the result for
`epoch=now, alpha=148.666, delta=16.3833, radius=1200, observer=500, filter=120, refsys=EQJ2000, objFilter=110` and:

* [`mime=text, output=object`](/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=text&-output=object&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc)
* [`mime=json, output=object`](/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=json&-output=basic&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc)
* [`mime=html, output=basic`](/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=html&-output=obs&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc)
* [`mime=votable, output=all`](/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=votable&-output=all&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc)

Output results
--------------

The output parameters of the method is a string which contains the following information:

| Field | Definition | Units | Output | | | |
| --- | --- | --- | --- | --- | --- | --- |
| object | basic | obs | all |
| 1 | Object number (blank if unnumbered) | - | x | x | x | x |
| 2 | Object name (official or preliminary designation) | - | x | x | x | x |
| 3–4 | Astrometric J2000 equatorial or ecliptic coordinates at the given epoch, relatively to the observer, sexagesimal format | α in hour, δ in deg  long and lat in deg | x | x | x | x |
| 5 | Class | - | x | x | x | x |
| 6 | Visual magnitude | mag | x | x | x | x |
| 7 | Error on the position | arcsec | x | x | x | x |
| 8–9 | Motion on the celestial sphere (Δα'cos(δ), Δδ) or (Δlon cos(lat), Δlat) | arcsec/h |  | x | x | x |
| 10 | Distance to observer | au |  | x | x | x |
| 11 | Heliocentric distance | au |  | x | x | x |
| 12 | Phase angle | degree |  |  | x | x |
| 13 | Solar elongation | degree |  |  | x | x |
| 14–19 | Mean J2000 heliocentric equatorial or ecliptic position and velocity vectors at epoch T0 | au and au/d |  |  |  | x |
| 20 | Reference epoch of the position vector | Julien Day |  |  |  | x |

Note:
:   The VOTable, whatever the output, contains three hidden fields mainly dedicated to Aladin software:
    namely the astrometric J200 right ascension and declination (fields `_raj2000` \
    and `_decj2000`), and an external link to hint the targets in SsoDNet (field `externallink`).

Structure of the output JSON object
-----------------------------------

When the output mime type is the [JSON](https://www.json.org/) data-interchange format,
the output of the  `skybotconesearch` method is encapsulated into a structure defined as
follows (case `output=all`):  

```
[
  { 
    "Num": {int | string}, 
    "Name": {string}, 
    "RA (hour)": {string}, 
    "DEC (deg)": {string}, 
    "Class": {string},
    "VMag (mag)": {float}, 
    "Err (arcsec)": {float}, 
    "dRA (arcsec\/h)": {float}, 
    "dDEC (arcsec\/h)": {float}, 
    "dg (ua)": {float}, 
    "dh (ua)": {float}, 
    "Phase (deg)": {float}, 
    "SunElong (deg)": {float}, 
    "position (au)": { "x": {float}, "y": {float}, "z": {float} },
    "velocity (au\/d)": { "x": {float}, "y": {float}, "z": {float} },
    "ref_epoch": {float},
    "ssodnet": { "quaero": {string}, "ssocard": {string} }
  } 
]
```

How to consume
--------------

You have two ways to use the SkyBoT web service: by writting a client to send requests to the SkyBoT server and
to receive and analyze the response, or by using a command line interface and a data transfert program such as
[`curl`](https://curl.haxx.se/) or [`wget`](https://www.gnu.org/software/wget/).
For that, just execute one of the following commands in a console:  

```
$> curl "<URL>"
```

or

```
$> wget "<URL>"
```

where `<URL>` is described in section [HTTP request](#http-request).

In order to help you to invoke the SkyBoT web service, we provide some [clients](/webservices/skybot/clients/)
written in differents languages. Here are some detailed explanations to write a client with PHP
and SOAP which invokes the  `skybotconesearch` method:

1/ Provide the input parameters which are mandatory for the service:

```
// Client's ID: provide the name of your project or organisation or yourself
$from = 'MyName';
// Input parameters
$param = array('epoch'     => 2453384.92153935181,
               'alpha'     => 148.67,
               'delta'     => 16.3838,
               'radius'    => "900",
               'mime'      => "votable",
               'output'    => "basic",
               'observer'  => "500",
               'filter'    => "120",
               'objFilter' => "111",
               'refsys'    => "EQJ2000");

```

2/ Define the SOAP options, the namespace and the WSDL URI of SkyBoT web service:

```
// Enables or disables the WSDL caching feature
ini_set('soap.wsdl_cache_enabled', 1);
// SkyBoT namespace
$namespace = 'https://ssp.imcce.fr/webservices/skybot';
// SkyBoT WSDL
$uriwsdl = $namespace.'/skybot.wsdl';

```

3/ Create a SoapClient object in WSDL mode, set the SOAP header, then call the method and catch exceptions:

```
try {
   // Constructs the client
   $client = new SoapClient($uriwsdl, array('exceptions'=>1));
   // SOAP header
   $header = array('from'=>$from, 'hostip'=>'', 'lang'=>'en');
   $client->__setSoapHeaders(array(new SOAPHeader($namespace, 'clientID', $header)));  
   // Call the conesearch method
   $response = $client->__soapCall(' skybotconesearch',$param);
   // Display the results
   if ($param['mime'] == 'text') {
      header("HTTP/1.0 200");
      header("Content-Type: text/plain");
      echo "# Flag: ".$response->flag.PHP_EOL;
      echo "# Ticket: ".$response->ticket.PHP_EOL;
      $res = explode(';', $response->result);
      $nbr = count($res);
      $newkey = array_keys($res);
      for ($i=0; $i<$nbr; $i++) { echo $res[$newkey[$i]].PHP_EOL; }
    } else if ($param['mime'] == 'json') {
      header("HTTP/1.0 200");
      header("Content-Type: application/json");
      echo $response->result;
   } else {
      header("HTTP/1.0 200");
      header("Content-Type: text/xml;content=x-votable");
      echo $response->result;
   }
} 
catch (SoapFault $fault) 
{
   trigger_error("SOAP Fault: {$fault->getTraceAsString()} (faultcode: {$fault->faultcode},
                               faultstring: {$fault->faultstring})", E_USER_ERROR);
}
```

## Links found on page

- http://php.net/manual/en/function.strtotime.php
- http://www.ivoa.net/Documents/latest/VOT.html
- http://www.minorplanetcenter.net/iau/lists/ObsCodes.html
- https://curl.haxx.se/
- https://ivoa.net/documents/ConeSearch/20200828/
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=html&-output=obs&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=json&-output=basic&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=text&-output=object&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=now&-ra=148.67&-dec=16.3838&-rs=1200&-mime=votable&-output=all&-observer=500&-filter=120&-objFilter=110&-refsys=EQJ2000&-from=SkybotDoc
- https://ssp.imcce.fr/webservices/skybot/clients/
- https://ssp.imcce.fr/webservices/skybot/howto/conesearch/#howto-epoch
- https://ssp.imcce.fr/webservices/skybot/howto/conesearch/#howto-fovcenter
- https://ssp.imcce.fr/webservices/skybot/howto/conesearch/#howto-fovradius
- https://ssp.imcce.fr/webservices/skybot/howto/conesearch/#howto-objFilter
- https://ssp.imcce.fr/webservices/skybot/howto/conesearch/#howto-observer
- https://ssp.imcce.fr/webservices/skybot/skybot.php
- https://ssp.imcce.fr/webservices/skybot/skybot.php?wsdl
- https://ssp.imcce.fr/webservices/skybot/skybot.xsl
- https://www.gnu.org/software/wget/
- https://www.ivoa.net/Documents/latest/VOT.html
- https://www.json.org/
- https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5
- https://www.w3.org/TR/soap/
