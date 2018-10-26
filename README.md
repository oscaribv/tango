
# __TANGO__: Transit ANimation for General Orbits
#### Written by Oscar Barragán
##### email: oscaribv@gmail.com
##### Updated October 25, 2018


## __Introduction__

A clear night gives us an instantaneous snapshot of the Universe. At first sight celestial bodies seem immutable. Their apparent immutability disappears if we add an important ingredient: *time*.
The variability of their light – the so-called light curve – carries a wealth of precious information about the physical phenomena happening in faraway astronomical bodies.

Planets perform a gravitational *TANGO* around their parent stars which is called orbit.
If the orbit inclination is close to 90°, the presence of a planet orbiting its host star can be inferred by detecting the periodic drops of stellar flux caused by the planet partly occulting the stellar disk. This phenomenon is called __transit__.


## Dependencies

* numpy
* matplotlib
* seaborn (optional)
* [pyaneti](https://github.com/oscaribv/pyaneti) (optional, needed if you want to plot the models)


## Animate *K2* data of GJ 9827

The system GJ 9827 contains (at least) three transiting planets. They were discovered by *K2* on its Campaign 12 ( see [Niraula et al., 2017](http://iopscience.iop.org/article/10.3847/1538-3881/aa957c/meta), [Prieto-Arranz et al., 2018](https://www.aanda.org/articles/aa/abs/2018/10/aa32872-18/aa32872-18.html), and [Rodriguez et al., 2017](http://iopscience.iop.org/article/10.3847/1538-3881/aaa292/meta) for more details).
The brightness of this star combined with the exquisite photometry of *Kepler*, give us a marvelous light curve where the three transiting planets are visible. During February 12, 2017, planets b, c and d transited the star consecutively, and this was observed by *Kepler*. __We will animate this!__

First, just clone or download TANGO.

```
git clone https://github.com/oscaribv/tango
```

The advantage about cloning the repository is the possibility to follow the changes to this package easily with git pull (learn more about git
at [https://git-scm.com/](https://git-scm.com/)).

The next step is to enter the tango directory and see what we can find inside it

```
cd tango
ls
  gj9827  README.md  tango.py
```

You can see that there is a directory called gj9827. This directory contains the light curve and input file needed to create your animation. The file lc_gj9827.dat contains *K2* long cadence data collected between 2963.5 and 2964.3 (BJD - 2454833) days. In this window there are three consecutive transits of GJ 9827 b, c and d (I used the light curve provided by EVEREST to create this file).

So now we have the light curve that we want to animate. The next step is to create the input file which will be used to pass the orbit solutions to the code. If you open the input file you will see something like This


Now you are ready to run the code for the first time! Just type


```
./pyaneti.py test
```

or

```
python pyaneti.py test
```

The program will start. You will see something like:

```

```
If you see this output it means that pyaneti ended succesfully!

Now let us check the plots.

```
evince outpy/test_out/testb_tr.pdf outpy/test_out/testb_rv.pdf

```

You will see some nice plots that look like this


<img src="./src/images/testb_tr.png" style="width: 250px;"/>
<img src="./src/images/testb_rv.png" style="width: 250px;"/>

Let me explain you briefly what this test fit was about:
> If you were an advanced alien civilization with really high technology, and "lucky" enough to see an Earth-like planet crossing in front of a Sun-like star, **this is how the Earth would look like to you**.

Look at those well-known parameters:
* 1 Earth Mass
* 1 Earth radii
* Period of 365 days
* 1 AU semi-major axis
* Density of ~5.5 g/cm^2,
* Gravity of ~10 m/s^2.

Of course you would need a spectograph with a precision of a few cm/s and also a very nice photometer.

> If you are at this point, you learned two things. First, with good data you can obtain really nice planet parameters and second, you learned how to run pyaneti.


## Documentation

#### Play with _test_ - Joint radial velocity and transit light curve fitting.

* There is a directory called _inpy_, inside this folder you will find a second directory called _test_.

* This directory constains the input and data files to perform the test fit.

* You can create an input director inside _inpy_ for each of your systems!

* We encorauge you to start to play with the code.

Create your own test directory and copy all the files from _inpy/test_ folder.

```
mkdir inpy/my_test
cp inpy/test/* inpy/my_test
```

Now you are ready to run _my_test_

```
./pyaneti.py my_test
```

You will see an output similar to that the _test_ case.
Now the output files are inside _outpy/my_test_out_. You will notice that inside this
directory you will find a extra file with the posterior distribution and correlation plots of the fitted parameters.

Now open the file _inpy/my_test/input_fit.py_ and start to play with it. The file is comented.
Let us change the priors for some parameters. Uncomment lines 56, 91 and 92
to fit for the scaled semi-major axis and impact factor. Save the changes and
re-run the code.

```
./pyaneti.py my_test
```

Now you can see that the fitted parameters are different in comparison with
the values given by _test_.

If you have some RV and/or transit data you only have to put the name
of your data files, change the prior ranges, and start to fit your data!

#### Parallel run

Run the code in parallel is really easy.

Just compile the code in parallel (you need openMP installed).

```
make para
```

if you have all the libraries installed, the compilation should finish without any problem.
Now you only need to run the code.

```
./pyaneti.py test
```

This option will run the code with all the processors available in your computer.
If you want to specify the number of CPUs to be use by _pyaneti_, you have to run the
env OMP_NUM_THREADS=N option, where N is the number of CPUs.

```
env OMP_NUM_THREADS=2 ./pyaneti.py test
```


**More documentation will come soon!**


## Science  with pyaneti

* Prieto-Arranz et al., 2018, _Mass determination of the 1:3:5 near-resonant planets transiting GJ 9827 (K2-135)_,
[A&A, submitted](https://arxiv.org/abs/1802.09557)
* Barragán et al., 2018, _K2-141 b: A 5-M_Earth super-Earth transiting a K7 V star every 6.7 hours_
[A&A, 612, A95](http://adsabs.harvard.edu/abs/2017arXiv171102097B)
* Niraula et al., 2017, _Three Small Super-Earths Transiting the nearby star GJ 9827_, [AJ, in press.](http://adsabs.harvard.edu/abs/2017arXiv170901527N).
* Gandolfi et al., 2017, _The transiting multi-planet system HD3167: a 5.7 MEarth Super-Earth and a 8.3 MEarth mini-Neptune_,
[AJ, 154, 123.](http://adsabs.harvard.edu/abs/2017AJ....154..123G)
* Guenther et al., 2017, _K2-106, a system containing a metal rich planet and a planet of lower density_,
[A&A, in press.](https://arxiv.org/abs/1705.04163).
* Fridlund et al., 2017, _K2-111 b - A short period super-Earth transiting a metal poor, evolved old star_,
[A&A, 604, A16](http://adsabs.harvard.edu/abs/2017A%26A...604A..16F).
* Barragán et al., 2017, _K2-139 b: a low-mass warm Jupiter on a 29-day orbit transiting an active K0V star_,
[MNRAS, submitted](https://arxiv.org/abs/1702.00691).
* Nespral et al., 2017, _Mass determination of K2-19b and K2-19c from radial velocities and transit timing variations_,
[A&A, 601A, 128.](http://adsabs.harvard.edu/abs/2017A%26A...601A.128N).
* Barragán et al, 2016, _K2-98b: A 32-M⊕ Neptune-sized planet in a 10-day orbit transiting an F8 star_,
 [AJ, 152, 6](http://adsabs.harvard.edu/abs/2016AJ....152..193B).

**See the list of citations to the code [here](https://ui.adsabs.harvard.edu/#abs/2017ascl.soft08003B/citations)**

## Citing

If you use pyaneti in your research, please cite it as

```
Barragán, O., Gandolfi, D., & Antoniciello, G. 2018, ArXiv e-prints [arXiv:1809.04609]
```

you can use the bibTeX entry

```
@ARTICLE{pyaneti,
   author = {{Barrag{\'a}n}, O. and {Gandolfi}, D. and {Antoniciello}, G.
	},
    title = "{pyaneti: a fast and powerful software suite for multi-planet radial velocity and transit fitting}",
  journal = {\mnras},
archivePrefix = "arXiv",
   eprint = {1809.04609},
 primaryClass = "astro-ph.EP",
 keywords = {methods: numerical, planets and satellites: general, techniques: photometry, techniques: spectroscopy},
     year = 2018,
    month = sep,
      doi = {10.1093/mnras/sty2472},
   adsurl = {http://adsabs.harvard.edu/abs/2018MNRAS.tmp.2361B},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

## What will come next?

* Gaussian process.
* TTV.
* Multiband transit photometry fitting.
* Graphical User Interface.


**If you have any comments, requests, suggestions or just need any help, please don't think twice, just contact us!**

##

#### Warning: This code is under developement and it may contain bugs. If you find something please contact us at oscaribv@gmail.com

## Acknowledgements
* Hannu Parviainen, thank you for helping us to interpret the first result of the PDF of the MCMC chains. We learned a lot from you!
* Salvador Curiel, thank you for  suggestions to parallelize the code.
* Mabel Valerdi, thank you for being the first _pyaneti_ user, for spotting typos and errors in this document. And thank you much for the awesome idea for pyaneti's logo.
* Lauren Flor, thank you for testing the code before release.
* Jorge Prieto-Arranz, thank you for all the suggestions which have helped to improve the code.

**THANKS A LOT!**
