---
layout: post
title: Introduction to CMSSW part III - First look at the CMSSW framework
description: A first look at altering main function control flows with python files
tags: [c++, python, CMSSW]
modified: 2016-08-29
image:
  feature: code_head_1.png
  credit: ensc
---

In this article we are going to explore the (supposed) rational behind why the CMSSW framework is designed as it it, as well as getting a first look at how one could easily alter the contents of a EDM file using this framework. As before all, the concrete code used in this article could be found [here](https://drive.google.com/open?id=0Bw8_U9a0g9nHSG5rMEJWazdLMjQ)

## Hiding the Loop
By now, you might have known that the core component of the main function for data processing would center around the  event-by-event for loop, a skeleton code for the main function might look something like:

```cpp
// code for opening file

for( run.toBegin() ; !run.atEnd() ; run++ ){
   // come per run calculations...
   for( lumi.toBegin() ; !lumi.atEnd() ; ++lumi ){
      // some per lumi calculations
      for( event.toBegin() ; ! event.atEnd() ; ++event() ){
         // some per-event calculations...
         // some other per-event calculations...
         //...
      }
   }
}
// Save calculations of files
```

Now are a few rationals why the framework might want to hide the main loop from the user:

* In mass data processing, the framework might not want to give the user freedom to manipulate the ordering of the for loop.  For example there might be specializations for multi-threading.
* The framework might what to optimization global object handling, such as the the pointer to handle the event contents.

When designing the framework, one will still need to give the user an interface to defined calculation flows. One way of doing so would be using the concept of [polymorphism](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)), which is implemented in C++ as the [virtual function](http://www.cplusplus.com/doc/tutorial/polymorphism/) syntax:

```cpp
class BaseCalculator {
   virtual void perrun_calc( run& )    {} ; // do nothing is not redefined by derived class
   virtual void perlumi_calc( lumi& )  {} ;
   virtual void perevent_calc( event& ){} ;
}

class MyCalc1 : public BaseCalculator {}; // implement one kind of calculation
class MyCalc2 : public BaseCalculator {}; // implement another kind of calculation
```

And the definition of the main functions would turn into something like this:

```cpp
// open file

vector<BaseCalculator*> processList ;

// Load the user defined calculation
processList.push_back( new MyCalc1 );
processList.push_back( new MyCalc2 );

for( run.toBegin() ; !run.atEnd() ; run++ ){
   for( auto& calc : processList ){
      calc->perrun_calc( run );
   }
   for( lumi.toBegin() ; !lumi.atEnd() ; ++lumi ){
      for( auto& calc : processList ){
         calc->perlumi_calc( lumi );
      }
      for( event.toBegin() ; ! event.atEnd() ; ++event() ){
         for( auto& calc : processList ){
            calc->perevent_calc( event );
         }
      }
   }
}

// Save  calculations of files
```

The merit of using this structure for the end user is that one could separate independent calculations from each other, so if we are only interested in altering one specific calculation, you could do so without having to comb through the entire high level control flow. Of course, there is the problem that calculations might dependent on the results of other user calculations. So how to define the control flow couldn't be as simple as above with a simple list of pointers. Luckily for use, the `CMSSW` framework as a set of very handy tools that could help us with the calculations. As will be demonstrate later.

After understanding the rational behind the why when interacting with the CMSSW framework, you won't be handling the high level control flows directly, we begin to get on the actual code for defining user calculations.


## A Look at one calculator class: `EDProducer`

### Structure overview
Let us look at the structure required for using a [`EDProducer`](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEDMTutorialProducer) derived class to define calculation. It follows the standard `Package/Subpackage` structure required by `CMSSW`, but this time the C++ code is written in the `plugins` directory, and also an extra `python` directory.

```
Package
└── MyReader
    ├── plugins
    │   ├── BuildFile.xml
    │   └── MyReader.cc
    └── python
        └── ConfFile_cfg.py
```

Let us look at the `MyReader.cc` file first, which should give you a rough idea of all the functions that are available in the calculator class. It does the same as the `FWLite` example given in the previous article, dumping the contents of the "Gaussian" variable stored in a EDM file, except using the C++ technology described above:

```cpp
#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

class MyReader : public edm::stream::EDProducer<>
{
public:
  explicit MyReader(const edm::ParameterSet&);
  ~MyReader();

private:
  virtual void beginStream(edm::StreamID) override;
  virtual void endStream() override;

  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  virtual void produce(edm::Event&, const edm::EventSetup&) override;
};
```

you could think of these private member functions corresponding to these execution points in the imaginary loop code:

```cpp
// <--- beginStream() called here
for( run.toBegin() ; !run.atEnd() ; run++ ){
   // <-- beginRun() called here
   for( lumi.toBegin() ; !lumi.atEnd() ; ++lumi ){
      // <--- beginLuminosityBlock() called here
      for( event.toBegin() ; ! event.atEnd() ; ++event() ){
         // <--- produce() called here
      }
      // <--- endLuminosityBlock() called here
   }
   // <---  endRun() called here
}
// <--- endStream() called here
```

But note that the file opening and saving process are not handled by the `beginStream`/`endStream` functions. We will get to that in a bit. Now for the part of actually writing the "calculation" part of the code in the the `produce` member function.


### Getting the Handle class

Since the `CMSSW` main framework is designed with fast computing in hand, so the `Handle` class while similar in usage to that we have seen previously, requires slightly different initialization.

The [`edm::EDGetToken` class](http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_8_0_26/doc/html/de/dba/classedm_1_1EDGetToken.html) is mandatory to be initialized during the constructor via a `consumes()` call, and this is used to get the `Handle` class we will be interested in.

```cpp
class MyReader : public edm::stream::EDProducer<>
{...
private:...
   const edm::EDGetToken _mytoken;
};

// Getting the token via the consumes call.
// The Input Tag format is identical to that of the fwlite.
MyReader::MyReader(const edm::ParameterSet& iConfig):
   _mytoken( consumes<double>( edm::InputTag("myprod","Gauss","Dummy")) )
{} // No other initialization for now

// Defining the calculation to be called per event
void MyReader::produce(edm::Event& iEvent, const edm::EventSetup&)
{
   edm::Handle<double> myHandle;
   // Note the big difference in the getByToken() call compared to fwlite!
   iEvent.getByToken( _mytoken, myHandle );
   // After a sucessful getByToken call
   // myHandle is essentially a double pointer
   std::cout << *myHandle << std::endl;
}
```

Take special note of the much more complex way of inserting the three magic strings to get the Handle object.. Also take note that the `Handle` and `Event` class are no longer using the one in the `fwlite` namespace, but the `edm` work space.


### Exposing the class as a plugin.

The control flow part should be rather straight forwards, but there are still a few magic lines of code required to let the `CMSSW` framework understand this class as a calculation class.
At the very end of the file, we need to call the MACROS function:

```cpp
DEFINE_FWK_MODULE(MyReader);
```

Be sure that the argument in the MACROS functions is the same as the name of your class. In the case that you have decided to split you calculator class across multiple `.cc` files, make sure that this MACROS function is called exactly once. Otherwise you will get repeated definition error during the compilation.

Now we look at the requires needed to add to the `BuildFile.xml` file in the `plugins` directory:

```html
<use name="FWCore/Framework"/>
<use name="FWCore/PluginManager"/>
<use name="FWCore/ParameterSet"/>
<flags EDM_PLUGIN="1"/>
```

Again, the `use` tag is used to list external libraries as dependencies. The minimal requirements for the "calculator" class are the three listed above. The last line is new! This time, instead of saying we are compiling to a external library, we are making a "plugin" for manipulating `EDM` files (again with the name left to be default by the `="1"` flag). Now we are ready to compile!

```
scram b
```

## A python configuration file for the main function

Next we would want to know how to run the main function, and how to alter its behaviour, such as:

* What input file to use.
* What output file (if any) to use
* What calculator classes to load

The main function containing the event loops is invoked via the `cmsRun` command provided by the `CMSSW` environment, but to alter the behaviour of this main function, you need to provided it with a configuration file read, which is a python file that should be intuitive to read, and later down the line, allows the configuration it self to be programable! But first, lets look at a minimal example the file in directory `MyReader/python/ConfFile_cfg.py`, where the file is basically a bunch of declaration for what the main function should use.

```py
# Getting the required python modules
import FWCore.ParameterSet.Config as cms

# Defining the process
# You can say that process will be the object what is converted to
# what the main function should do.
process = cms.Process("MyProcess")

# How many events before early exit (-1 for effectively every event)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# Define input, note that for local files, the prefix 'file:' is required
# so the below is referring to the local file ./edm_example.root
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        'file:edm_example.root'
    )
)

# Loading the producer, notice the string must the same as
# the argument you placed in the C++ MACROS function!
# but the name of the member in the process instance can be anything you want.
process.myProducer = cms.EDProducer(
    'MyReader'
)

# Defining sequence of producer instances you want to run.
# Again, the name of the member in the process instance could be anything you want.
process.mypath = cms.Path(process.myProducer)
```

A note to the folks that are not familiar with python syntax. The data members in a python class are completely dynamic, meaning you can [add data members](https://docs.python.org/3/tutorial/classes.html) at will. The python memory manager will also keep track of what type each variable is declared by. So what the main file will be translated to will be something like this:


```python
process = ReadFromConfig( "ConfFile_cfg.py" )

# Opening the file
open( process.source.fileName )

# Defining the calculation classes to load via cms.Path variables
calclist = []
for member  in  get_all_member( process ) :
  if get_type( member ) == get_type( cms.Path ):
    calclist.extend( member.content )

## main for loop
for evt  in opened_file :
  for calc in calclist :
    calc.produce( evt )
```

It must be stressed that this is a very rough "translation", and is definitely not what is actually implemented in the `CMSSW` framework. The core concept of what to take away from this translation is that ultimately what matters in the configuration file would be the final data members in the `cms.Process` instance.

Having written you configuration file, you could then run the following command:

```
cmsRun ConfFile_cfg.py
```

And you should get the output that looks something like:

```
29-Aug-2016 20:53:16 CST  Initiating request to open file file://edm_example.root
29-Aug-2016 20:53:17 CST  Successfully opened file file://edm_example.root
Begin processing the 1st record. Run 1, Event 383601, LumiSection 1919 at 29-Aug-2016 20:53:18.320 CST
2.9968
Begin processing the 2nd record. Run 1, Event 383602, LumiSection 1919 at 29-Aug-2016 20:53:18.321 CST
2.34539
...
Begin processing the 10th record. Run 1, Event 383610, LumiSection 1919 at 29-Aug-2016 20:53:18.322 CST
6.78134
29-Aug-2016 20:53:18 CST  Closed file file://edm_example.root

=============================================

MessageLogger Summary

 type     category        sev    module        subroutine        count    total
 ---- -------------------- -- ---------------- ----------------  -----    -----
    1 fileAction           -s file_close                             1        1
    2 fileAction           -s file_open                              2        2

 type    category    Examples: run/evt        run/evt          run/evt
 ---- -------------------- ---------------- ---------------- ----------------
    1 fileAction           PostEndRun                        
    2 fileAction           pre-events       pre-events       

Severity    # Occurrences   Total Occurrences
--------    -------------   -----------------
System                  3                   3

```

Congratulations! You have complete the event loop using the full CMSSW framework! Notice that what you actually calculate and defined to be outputted is in between the messages pre-defined by the CMSSW framework for loop.

## Making the producer produce something
As suggested by the name, the `EDProducer` this isn't just a calculator class. The `EDProducer` class has functionalities that actually produces something that could be placed into an output `EDM`. Suppose I want to compute the square of all the `Gauss` variables and store them in the event. We would need to alter the constructor:

```cpp
MyProducer::MyProducer(const edm::ParameterSet& iConfig):
   _mytoken( consumes<double>(edm::InputTag("myprod","Gauss","Dummy")))
{
   produces<double>("GaussSquare");
}
```

which tell the main function that we want to produce a `double` collection, called `GaussSquare`. Next we need to define how the `GaussSquare` variable should be calculated.

```cpp
void MyProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<double> myHandle;
   iEvent.getByToken( _mytoken, myHandle );

   std::auto_ptr<double> myptr( new double );
   *myptr = (*myHandle) * (*myHandle);
   iEvent.put( myptr, "GaussSquare" );
}
```

The three new lines creates a new pointer to a double, store the results that we want, and associate the double with the `GaussSquare` name. (If you are wondering what an [`auto_ptr`](http://en.cppreference.com/w/cpp/memory/auto_ptr) is, it is essentially the same as the pointer, except it automatically deletes at the end of the scope it is declared in. The use of this STL class (or its successor class [`std::unique_ptr`](http://en.cppreference.com/w/cpp/memory/unique_ptr) to call the `put` member function is mandatory).

Next we need to add the following lines to the python configuration file:

```py
# Same as before, but with the MyProducer instance instead
process.myProducerInstance = cms.EDProducer(
    'MyProducer'
)
process.p = cms.Path(process.myProducerInstance)

# We wish to output a EDM files containing all the stuff produced in this process
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myoutput.root'),
)

# Marking the process as a EndPath (to be ran after everything else)
process.e = cms.EndPath( process.out )
```

Next you could run the command

```
cmsRun python/Conf1.py
```

You should see a new file called `myoutput.root`, and if you dump the contents of this file you should see:

```
Type                    Module                 Label           Process           
---------------------------------------------------------------------------------
double                  "myprod"               "Gauss"         "Dummy"           
int                     "myprod"               "Poisson"       "Dummy"           
double                  "myProducerInstance"   "GaussSquare"   "ProduceProcess"   
```

You now have a new collection! You could also being to see where the three magic strings used to get objects in the `EDM` files are coming from:

  * The module name is the name you defined for the `cms.EDProducer` instance **in the python file**
  * the process name is the name you gave the `cms.Process` instatnce **in the python file**.
  * The Label name is defined in the `C++` file on the `produces` call in the producer constructor. A common practice in the standard CMS data files is for each producer to produce only one variable for one type type. In which case you cad leave the entry in the `produces` call empty.

It is worth noting that most of the standard "analysis recipes" in CMS revolves around using `EDProducers` to add more objects into a EDM file during runtime. For instance we make a joint configuration to first product the "GaussSquare" variable before passing the calculation results to our `MyReader` class. In the next section, we will be introducing tool for better high level control flow in the python file, as well as a better look at the interface between the python and c++ interface.

## Comparison between `FWLite` and the full framework
As you have probably seen, a CMSSW framework is aimed for event looping and event looping only. If you want to combine various `EDM` files with different weight associated with each file, it is doable, but very hard. The `CMSSW` full framework is meant to dealing with bulk calculations across a large number of files. The reason for using plugins and such C++ technologies is used so that the full framework could also multi-threaded with minimal amount of additional user coding. The full framework should be used to reduce the bulky, general purpose files into a handful of variable/objects that are interesting to an analysis, and then a more flexible `fwlite` framework could be used to read the output and produce the final calculation.
