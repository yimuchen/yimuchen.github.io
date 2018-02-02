---
layout: post
title: Experiences with Inheritance
description: Infuriating experiences with classes in C++
tags: [thoughts, computing, c++, recipe]
modified: 2016-06-08
image:
  feature: code_head_1.png
  credit: ensc
---

I have recently began to practice designing more general purpose classes for my analysis. Conceptualising the concept object itself is difficult enough: one needs to avoid both being specific and too general, but over these days of experience with C++'s more obscure syntax and quirks, I really began to see why some might not consider C++ a complete object oriented programming language.

## The Diamond Problem

One handy way of avoiding repeated code is by class inheritance, so when you want to merge the functionality of two classes `B` and `C`, one might build a inherited class `D` that inherits both `B` and `C`:

{% highlight c++ %}
class B {};
class C {};
class D : public B, public C{};
{% endhighlight %}

But now a problem arises if `B` and `C` has a common ancestor, say class `A`:

{% highlight c++ %}
class A { public: int x;};

class B : public A{};
class C : public A{};
class D : public B, public C{};
{% endhighlight %}

Because when we create an instance of object `D`, we create an instance of object `B` and `C`, which repectively creates and instance of object `A`. So when we write: `C.x`, are we refering to the instance `C::A::D.x` or `C::B::D.x`? Such is known as the [diamond problem](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem), or the [deadly diamond of death](http://objectmentor.com/resources/articles/javacpp.pdf)

<figure>
	<a href="https://en.wikipedia.org/wiki/Multiple_inheritance">
   <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Diamond_inheritance.svg/180px-Diamond_inheritance.svg.png" alt=""></a>
	<figcaption><a href="https://commons.wikimedia.org/w/index.php?curid=1015688">
      Dependency diagram of diamond problem - By RokerHRO</a>
   </figcaption>
</figure>

Each program has their own approach to solving this problem. In C++, we require that at least one of the intermediate classes to be "virtually inherited", so that extended classes `D` will only create one instance on grandparent class `A`:

{% highlight c++ %}
class A { public: int x;};

class B : virtual public A{};
class C : virtual public A{};
class D : public B, public C{};
{% endhighlight %}


In the cases that simple inheritance and virtual inheritance at mixed and matched, the non-virtually inherited instances create independent instances of base class `A`, and explict paths are used expressed access:

{% highlight c++ %}
class A { public: int x;};

class B : virtual public A{ public: int b; };
class C : virtual public A{ public: int c; };
class E : public A{ public:  int e ; };
class D : public B, public C, public E{};

D d;

d.x = d.b = d.c = d.e; // All Legal variables
d::B.x; // Equivalent to d.x
d::A.x; // Equivalent to d.x
d::E.x; // An Independent variable to the one above!

{% endhighlight %}

While this does give most of the flexibility to the user as to what variables are used in an extended inheritance class, this still poses some issues: Since a virtual instance of grandparent class exists, the grandchild class has to explicitly call grandparent constructor for initialisation ( unless a argument-less constructor exists ). While it seems like a minor feature, it still means that abstraction in not a "opaque" as it should be. For instance, Python tackles this problem by guessing the meaning of `d.x` by the inheritance order during the declaration `class D(B,C,E):`, with the rule of thumb being "First found in DSF searching" and allowing syntax for hierarchy shifting, which makes class design much more intuitive.


## The missing VTABLE error message
One of the most infuriating compile error messages in g++4.9.3 is:

```
In function <class>::<constructor>
undefined reference to vtable for <class>
```

as it is annoying uninformative as to what is missing. A simplified view of the `vtable` (or virtual table) is a table of virtual methods that the compiler generates for a class, which is then linked for each class in an inheritance hierarchy. Missing `vtable` may be cause by the following issues:

* The file containing the `vtable` was not included for linking.
* The `vtable` was not generated. For a `vtable` to be generated, the all instances of reimplemented virtual functions to exists.

Most of the time, when a method is missing, the following error message is much more informative:

```
Error: undefined reference to <class>::<method>(<arguments>)
```

But in the case of methods related to the `vtable` generation, the error messages for missing methods is all compacted into a `missing vtable` and send to look for bugs in the constructor. Not only are you not-told where you bug might be, but it actively tells you to look for somewhere where the bug isn't.

I know that the error messages have been greatly improved in g++6.1. But working in a collaboration, I don't have the luxury to choose which compiler version I get to use. This is a memo to help me remember what this error message means and how to avoid it in the future.
