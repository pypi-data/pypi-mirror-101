Installation
============

This command should install :mod:`islpy`::

    pip install islpy

You may need to run this with :command:`sudo`.
If you don't already have `pip <https://pypi.python.org/pypi/pip>`_,
run this beforehand::

    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    python get-pip.py

For a more manual installation, `download the source
<http://pypi.python.org/pypi/islpy>`_, unpack it, and say::

    python setup.py install

You may also clone its git repository::

    git clone --recursive http://git.tiker.net/trees/islpy.git
    git clone --recursive git://github.com/inducer/islpy

Wiki and FAQ
============

A `wiki page <http://wiki.tiker.net/IslPy>`_ is also available, where install
instructions and an FAQ will grow over time.

For a mailing list, please consider using the `isl list
<http://groups.google.com/group/isl-development>`_ until they tell us to get
lost.

License
=======

islpy is licensed to you under the MIT/X Consortium license:

Copyright (c) 2011 Andreas Klöckner and Contributors.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

.. note::

    * isl and imath, which islpy depends on, are also licensed under the `MIT
      license <http://repo.or.cz/w/isl.git/blob/HEAD:/LICENSE>`_.

    * GMP, which used to be a dependency of isl and thus islpy, is no longer
      required. (but building against it can optionally be requested)

Relation with isl's C interface
===============================

Nearly all of the bindings to isl are auto-generated, using the following
rules:

* Follow :pep:`8`.
* Expose the underlying object-oriented structure.
* Remove the `isl_` and `ISL_` prefixes from data types, macros and
  function names, replace them with Python namespaces.
* A method `isl_printer_print_set` would thus become
  :meth:`islpy.Printer.print_set`.

See also :ref:`gen-remarks`.

User-visible Changes
====================

Version 2016.2
--------------
.. note::

    This version is currently in development and can be obtained from
    islpy's version control.

* Update for isl 0.17
* Add :func:`islpy.make_zero_and_vars`

Version 2016.1.1
----------------

* Add :func:`islpy.make_zero_and_vars`
* Do not turn on small-integer optimization by default
  (to avoid build trouble on old compilers)

Version 2016.1
--------------

* Update for isl 0.16

Version 2014.2.1
----------------

* :mod:`islpy` now avoids using 2to3 for Python 3 compatibility.

Version 2014.2
--------------

* A large number of previously unavailable functions are now exposed.

* Sebastian Pop's `imath <https://github.com/creachadair/imath>`__ support has
  been merged into the version of isl that ships with :mod:`islpy`. This means
  that unless a user specifically requests a build against GMP, :mod:`islpy`
  is (a) entirely self-contained and depends only on a C++ compiler and
  (b) is entirely MIT-licensed by default.

Version 2014.1
--------------

* Many classes are now picklable.

* isl's handling of integer's has changed, forcing islpy to make
  incompatible changes as well.

  Now :class:`islpy.Val` is used to represent all numbers going
  into and out of :mod:`islpy`. ``gmpy`` is no longer a dependency
  of :mod:`islpy`. The following rules apply for this interface change:

  * You can pass (up to ``long int``-sized) integers to methods of
    isl objects without manual conversion to :class:`islpy.Val`.
    For larger numbers, you need to convert manually for now.

  * All numbers returned from :mod:`islpy` will be of type :class:`islpy.Val`.
    If they are integers, they can be converted

  * Since upstream made the decision to make ``isl_XXX_do_something_val``
    not always semantically equivalent to ``isl_XXX_do_something``, the
    old functions were removed.

    One example of this is ``isl_aff_get_constant``, which returned just
    the constant, and ``isl_aff_get_constant_val``, which returns the
    constant divided by the :class:`islpy.Aff`'s denominator as a rational
    value.

Version 2011.3
--------------

* Add :meth:`islpy.Set.project_out_except` and friends.
* Add ``islpy.Set.remove_divs_of_dim_type`` and friends.
* ``islpy.Dim`` was renamed to :class:`islpy.Space` in isl.
* ``islpy.Div`` was removed and replaced by :class:`islpy.Aff`
  wherever it was used previously.
* ``islpy.BasicSet.as_set`
  and
  ``islpy.BasicMap.as_map``
  were removed.
* :ref:`automatic-casts` were added.
* Support for more Python :class:`set`-like behavior was added. In particular,
  the operators `|`, `&', '-', `<`, `<=`, `>`, `>=`, `==`, `!=` work as expected.
* Support direct construction from string for objects that have a `read_from_str`
  method.
* The constant in a :class:`islpy.Constraint` is now set as the '1'
  key in a coefficient dictionary in
  :meth:`islpy.Constraint.eq_from_names`,
  :meth:`islpy.Constraint.ineq_from_names`, and
  :meth:`islpy.Constraint.set_coefficients_by_name`.

Version 2011.2
--------------

* Switch to copy-by-default semantics.
* A few changes in Python-side functionality.
* Automatic type promotion in 'self' argument.

Version 2011.1
--------------

* Initial release.

Documentation Cross-References
------------------------------

.. class:: unsigned

    See :class:`int`.

.. class:: long

    See :class:`int`.

.. class:: size_t

    See :class:`int`.

.. class:: double

    See :class:`float`.
Bundled dependencies in the wheel
gmp is bundled with this wheel
Source code can be found at: https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2
gmp license
===================
Copyright 1991, 1996, 1999, 2000, 2007 Free Software Foundation, Inc.

This file is part of the GNU MP Library.

The GNU MP Library is free software; you can redistribute it and/or modify
it under the terms of either:

  * the GNU Lesser General Public License as published by the Free
    Software Foundation; either version 3 of the License, or (at your
    option) any later version.

or

  * the GNU General Public License as published by the Free Software
    Foundation; either version 2 of the License, or (at your option) any
    later version.

or both in parallel, as here.

The GNU MP Library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received copies of the GNU General Public License and the
GNU Lesser General Public License along with the GNU MP Library.  If not,
see https://www.gnu.org/licenses/.






			THE GNU MP LIBRARY


GNU MP is a library for arbitrary precision arithmetic, operating on signed
integers, rational numbers, and floating point numbers.  It has a rich set of
functions, and the functions have a regular interface.

GNU MP is designed to be as fast as possible, both for small operands and huge
operands.  The speed is achieved by using fullwords as the basic arithmetic
type, by using fast algorithms, with carefully optimized assembly code for the
most common inner loops for lots of CPUs, and by a general emphasis on speed
(instead of simplicity or elegance).

GNU MP is believed to be faster than any other similar library.  Its advantage
increases with operand sizes for certain operations, since GNU MP in many
cases has asymptotically faster algorithms.

GNU MP is free software and may be freely copied on the terms contained in the
files COPYING* (see the manual for information on which license(s) applies to
which components of GNU MP).



			OVERVIEW OF GNU MP

There are four classes of functions in GNU MP.

 1. Signed integer arithmetic functions (mpz).  These functions are intended
    to be easy to use, with their regular interface.  The associated type is
    `mpz_t'.

 2. Rational arithmetic functions (mpq).  For now, just a small set of
    functions necessary for basic rational arithmetics.  The associated type
    is `mpq_t'.

 3. Floating-point arithmetic functions (mpf).  If the C type `double'
    doesn't give enough precision for your application, declare your
    variables as `mpf_t' instead, set the precision to any number desired,
    and call the functions in the mpf class for the arithmetic operations.

 4. Positive-integer, hard-to-use, very low overhead functions are in the
    mpn class.  No memory management is performed.  The caller must ensure
    enough space is available for the results.  The set of functions is not
    regular, nor is the calling interface.  These functions accept input
    arguments in the form of pairs consisting of a pointer to the least
    significant word, and an integral size telling how many limbs (= words)
    the pointer points to.

    Almost all calculations, in the entire package, are made by calling these
    low-level functions.

For more information on how to use GNU MP, please refer to the documentation.
It is composed from the file doc/gmp.texi, and can be displayed on the screen
or printed.  How to do that, as well how to build the library, is described in
the INSTALL file in this directory.



			REPORTING BUGS

If you find a bug in the library, please make sure to tell us about it!

You should first check the GNU MP web pages at https://gmplib.org/, under
"Status of the current release".  There will be patches for all known serious
bugs there.

Report bugs to gmp-bugs@gmplib.org.  What information is needed in a useful bug
report is described in the manual.  The same address can be used for suggesting
modifications and enhancements.




----------------
Local variables:
mode: text
fill-column: 78
End:
		   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions. 

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version. 

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.

isl is bundled with this wheel
Source code can be found at: http://isl.gforge.inria.fr/isl-0.22.1.tar.gz
isl license
===================
MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
