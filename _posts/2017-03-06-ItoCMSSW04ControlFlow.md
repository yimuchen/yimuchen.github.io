---
layout: post
title: Introduction to CMSSW part IV - Tools for high level control flow
description: Better tools for high level control flow in using the CMSSW framework
tags: [c++,python,cmssw]  
modified: 2017-03-06
image:
  feature: code_head_1.png
  credit: ensc
---

All the code could be found here

## C++ plugin and python configuration interface

As we have seen the `EDProducer` plugin class is initialized with a `const edm::ParameterSet&` argument. This object is passed down from the python configuration file used to declare the plugin the python configuration file. What the `edm::ParameterSet` is is sort of a associate array with string as indexes to access various data types. In the C++ file, the contents in a `edm::ParameterSet` is access like:

```cpp
PSetTest::PSetTest( const edm::ParameterSet& iConfig )
{
  cout << iConfig.getParameter<int>("myint") << endl;
  cout << iConfig.getParameter<std::string>("mystring") << endl;

  for( const auto& mydouble : iConfig.getParameter<std::vector<double>>("myintlist") ){
    cout << mydouble << " ";
  } cout << endl;
}
```

In the instance of the python file, to defined the `edm::ParameterSet` to be read:

```python
process.psettest = cms.EDProducer(
  # First string used to determine which plugin to use.
  "PSetTest",

  # All other are made into the edm::Parameter instance to be used in the c++ file
  myint = cms.int32( 100 ),
  myintlist = cms.vint32( 3.1415926 ),
  mystring = cms.string( "test string" ),

)
```

A complete list of data types supported by the `edm::ParameterSet` with the python corresponding object could be found [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Parameters). One of the most import objects that is supported is that of `edm::ParameterSet` itself and its vector variant. This gives every plugin the potential to load arbitrarily complicated initialization conditions while still keeping the code readable.

## Python output configuration
