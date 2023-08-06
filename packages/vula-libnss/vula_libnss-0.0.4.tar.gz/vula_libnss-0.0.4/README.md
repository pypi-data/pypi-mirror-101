This project provides a source package and also an architecture specific libnss
shared object file which are suitable for upload to pypi. We encourage users to
build a deb and it will put the required libnss shared object into
`/lib/libnss_vula.so.2`; users of the pip installed `vula_libnss` need to copy
the `libnss_vula.so.2` into the correct place and reconfigure `nsswitch.conf`
to use this new module.

If in doubt, build a Debian package and install it; if you're an advanced user,
you may pip install `vula_libnss` and manually configure it for use with
`vula`.

To build a Debian package:

```make deb```

For developers, we also provide some additional build targets.

To build a python source package and an arch specific wheel for the current
system architecture suitable for upload to pypi:

```make pypi-build```

To upload those files to pypi:

```make pypi-upload```

To clean up after the build:

```make clean```

