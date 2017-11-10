---
layout: post
title: Introduction to CMSSW Part I - The compiling environment and Hello world
description: Getting comfortable with writing and compiling code in CMSSW
tags: [c++, cmssw, analysis]
modified: 2016-08-14
image:
  feature: code_head_1.png
  credit: ensc
---


Let's begin with the simplest of examples for any programming language, how to write a hello world program. The example files used in this page could be found [here](https://drive.google.com/file/d/0Bw8_U9a0g9nHTHhjSlNiamQ5RWc/view?usp=sharing), and extract the file to the `CMSSW_X_X_X/src` directory with the command:

```bash
tar -zxvf HelloWorld.tar.gz
```
Remember each time you entry this directory, you should load the CMSSW environment with the command

```bash
cmsenv
```

If you wish to follow the build the sample up yourself, I will also be listing the directory structure used below

## Writing a main function and a first look at `BuildFiles`

### Writing a working version
Writing a main function is simple, but you will need to structure your file in the specific structure to properly expose the file containing the main function to the `CMSSW` compiling environment. For the simplest example of just one file containing a main function, you will need to construct the following structure below the `CMSSW_X_X_X/src` directory:

```
CMSSW_X_X_X/src
└── <HelloWorld>
    └── <Example1>
        └── bin
            ├── BuildFile.xml
            └── <main>.cc

```

where all of the files and directory could be named whatever you want with a few exceptions:

  * your `<main>.cc` file must end with with a valid C++ extension: `.cc`, `.cpp`, `.cxx` and such.
  * The `BuildFile.xml` must be named exactly as indicated.

Write your `main.cc` how ever you like, and add in the `BuildFile.xml` the file below.

```html
<bin name="HelloWorld" file="main.cc"/>
```

Be careful to change the entry after `file` to be whatever you have called your C++ file. Now you can call the `CMSSW` compile command in any working directory above `HelloWorld/Example1`.

```bash
scram b
```

After the command has finished (and no compile errors are produced), you should now have a new command available, type `HelloWorld` ( or whatever you have added in the `name` entry in the `BuildFile.xml` ) into your command line and see the result of your main file!

```bash
[user@machine Example1] HelloWorld
Hello World!
```

### Simple explanation of The `BuildeFile.xml`
The `BuildFile.xml` replaces the `makefile` file to tell the compiler what to compile; in our case, the contents for our file `BuidlFile.xml` is rather simple, you could read as:

> request to build a `bin`ary file to be called `HelloWorld` using the main function found in the C++ file `main.cc`.

The binary file that is created would be stored under the `CMSSW_X_X_X/bin/`. The first thing that you could try out is that the you could write multiple main function files in the `Example1/bin` directory provided that the final executable are named differently! Just remember for each new `.cc` you write to add an entry in the `BuildFile.xml`.

It is also worth noting that `xml` is the fully named the [*extensible markup language*](https://en.wikipedia.org/wiki/XML), which is used for storing information in a document in a specific way so that is should be both human and machine readable. Though commonly seen in web application (alongside his famous cousin [`html`](https://en.wikipedia.org/wiki/HTML)), the usage of `xml` files are not limit to such applications only.

Writing a main function is only the first step. If you are the kind of guy that writes analysis code in a single file consisting of a few thousand lines of code, then I can guarantee you that after three weeks without looking at it, the code would become unintelligible, even by the writer. How you write you own libraries and split subroutines into multiple files is on big step for making you code readable. This ties in with the next part we will be looking at, about directories other than `bin` and how to write their corresponding `BuildFile.xml`

## The CMSSW BuildFile structure

Here we take a look at a more complicated structure. One what that might commonly occur:

 * We want a to create a library `ExampleLib` containing the complete implementation of a class and relate function.
 * We want some additional wrapper function to help interface the classes to the main function
 * The main function to actually execute the code.

The structure we would want to create would be something like this:

```
CMSSW_X_X_X/src
└── HelloWorld
    ├── Example2
    │   ├── bin
    │   │   ├── BuildFile.xml
    │   │   └── main.cc
    │   ├── interface
    │   │   └── funclib.hpp
    │   └── src
    │       ├── BuildFile.xml
    │       └── funclib.cc
    └── ExampleLib
        ├── interface
        │   └── MyClass.hpp
        └── src
            ├── BuildFile.xml
            ├── MyClass.cc
            └── MyClass_Say.cc
```

### Exposing a library and understanding the include path
Inside The directory `HelloWorld/ExampleLib` is a class declaration and implementation

```cpp
// in MyClass.hpp
#ifndef HELLOWORLD_MYCLASS
#define HELLOWORLD_MYCLASS
#include <string>
class MyClass {
public:
   MyClass( const std::string& );
   virtual ~MyClass ();
   void Say( const std::string& );
private:
   const std::string _name;
};
#endif

//-------------------------
// in MyClass.cc
#include "HelloWorld/ExampleLib/interface/MyClass.hpp"
MyClass::MyClass( const std::string& x ) : _name(x) {}
MyClass::~MyClass(){}

//-------------------------
// in MyClass_Say.cc
#include "HelloWorld/ExampleLib/interface/MyClass.hpp"
#include <iostream>
void MyClass::Say( const std::string& x ){
   std::cout << this->_name << " says: " << x << std::endl ;
}
```

Looking at how the various `.cc` file include the common header, you can see that the CMSSW compile environment adds a new include path in the compilation flags, which is the `CMSSW_X_Y_Z/src` directory! To tell the compiler that the contents of this folder is meant for a shared library, you must include this line in the `BuildFile.xml` file:

```html
<export><lib name="1"/></export>
```

Again the meaning of this file is meant to be human readable:

> Export **every** c++ file in the `HelloWorld/ExampleLib/src` directory as a single shared object file, with the the library name left automatic (1).

You can see this in action by checking the content in `CMSSWW_X_Y_Z/lib` directory.

All this instruction is well, but a shared library isn't much use without a executable file.


### Using shared libraries.

We first use an example of a library using another library. In the directory `HelloWorld/Example2`, we could see in the `interface/funclib.hpp` and `src/funclib.cc` file that this library provides one function, which depends on the example just given:

```cpp
#include "HelloWorld/ExampleLib/interface/MyClass.hpp"
#include <iostream>
int myfunction()
{
   static MyClass myinst("hello"); myinst.Say("World");
   std::cout <<  "Hello World from my function!" << std::endl;
   return 0;
}
```

Again, note how the external header file is included. Now for the building of this library we need to link it with the functions found in `HelloWorld/ExampleLib`, so the `BuildFile.xml` in `HelloWorld/Example2/src` need two have one more line:

```html
<use name="HelloWorld/ExampleLib"/>
<export><lib name="1"/></export>
```

The second line is already exampled with the `HelloWorld/ExampleLib` build file. The first line list the dependency of this library. Notice to list a library withing CMSSW as a dependency, you just need to use the `use` tag, with the `name` field being the directory of the dependency from within the `CMSSW_X_Y_Z/src` directory!

Finally for the for the `BuildFile.xml` in the `bin` directory, where the main function file requires the use of both of these external libraries, the `BuildFile.xml` there would read something like:

```html
<use name="HelloWorld/ExampleLib"/>
<use name="HelloWorld/Example2"/>
<bin name="HelloWorld2" file="main.cc"/>
```

Go and give the code a run and add your own tweaks, this should give you an idea of how to write your own libraries in the `CMSSW` compiling environment.


## More details about the `BuildFile.xml`.

As we have previously states, the `BuildFile.xml` is designed to reduce the verbosity of writing `MakeFile` like compiling control flows. This simplification is based on the fact that code structure of the `CMSSW` compiling environment is very strict. With all the `BuildFile.xml` required to be located under a  `CMSSW_X_X_X/src/Package/Subpackage/<dir>` path, where `<dir>` could only be named as a directory that the compile environment recognizes. What `<dir>` could be will be picked up as we go along.

### Official packages that you can add to `use`
When you first initiate your `CMSSW` environment, the `src` directory might looks empty. The the whole arsenal of packages and subpackages in the official `CMSSW` repository would be pre-compiled and at your disposal. Which is a good thing, because the whole CMSSW code would take approximately 20 hours to compile at the very least. For example, you package could have C++ codel that reads:

```cpp
// In a c++ file
#include "DataFormats/FWLite/interace/Event.hpp"
```

together with the `BuildFile.xml` with contents

```html
<!--- In a BuildFile.xml  --->
<use name="DataFormats/FWLite"/>
```

would be totally legal. For a list of all the packages you could use, see the [official github page](https://github.com/cms-sw/cmssw)). Some of these offical `CMSSW` packages are highly specialized packages for specific use cases within the operator of CMS operation, data collecting and processing, while other packages are core framework packages that will be used by nearly everyone who needs information from the data collected at CMS. The core packages will be what we mainly focus on for these tutorials.


### External libraries to be added to use.
What about packages outside of `CMSSW`? Unfortunately, there is no easy way of including them. But there are special libraries that are commonly used in the field of experimental high energy physics that could be used without hassle. These libraries include:

 * [ROOT](https://root.cern.ch/): `<use name="root"/>`
 * [ROOT](https://root.cern.ch/) plotting libraries and [RooFit](https://root.cern.ch/roofit): `<use name="roofit"/>`
 * The entire [boost](http://www.boost.org/) library: `<use name="boost"/>`
 * The [boost program options](http://www.boost.org/doc/libs/1_61_0/doc/html/program_options.html) libraries: `<use name="boost_program_options"/>`
 * The [boost python](http://www.boost.org/doc/libs/1_61_0/libs/python/doc/html/index.html) libraries: `<use name="boost_python"/>`

### Defining additional compile flags

If you wish to define additional compilation flags for specific optimization, debugging, declaring MACROS, and others, then you could do so for individual `BuildFile.xml` with lines such as

```html
<flag CXXFLAGS="-O1 -g"/>
<flag CPPDEFINE="DEBUG=1"/>
```


## Additional documentations and closing words

This is by no means an exhaustive list of all the structures and options allowed in `CMSSW`, for the official documentation, see [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBuildFile). We will be picking the ones we need up as we go along, but hopefully, with this knowledge it will become more easy for you to organize the code in you analysis into a more organized structure.
