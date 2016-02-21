An RPM spec file for the AMQP 1.0 rsyslog output module.

This spec file builds the omamqp1 output module and installs it into
the rsyslog module library directory.  It also builds and installs a
private copy of the QPID Proton AMQP 1.0 protocol library into the
same rsyslog library directory.  This library is required by the
omamqp1 module.

First, the SRPM file should be created using the following recipe:

$ # pull down the source rpm for the target rsyslog package
$ # this will be used to build the omamqp1 module
$ builddir=`pwd`
$ mkdir -p rsyslog_build
$ wget https://copr-be.cloud.fedoraproject.org/results/portante/rsyslog-v8.15/epel-7-x86_64/00149031-rsyslog/rsyslog-8.15.0-1.el7.centos.src.rpm
$ rpm --define "_topdir $builddir/rsyslog_build" -i rsyslog-8.15.0-1.el7.centos.src.rpm
$ rpmbuild --define "_topdir $builddir/rsyslog_build" -bp rsyslog_build/SPECS/rsyslog.spec
$ pushd rsyslog_build/BUILD
$ tar -cvzf ../../rsyslog-8.15.0-1.tar.gz rsyslog-8.15.0
$ popd

$ # now pull down the source rpm for the QPID Proton library
$ mkdir -p proton_build
$ wget https://dl.fedoraproject.org/pub/epel/7/SRPMS/q/qpid-proton-0.10-2.el7.src.rpm
$ rpm --define "_topdir $builddir/proton_build" -i qpid-proton-0.10-2.el7.src.rpm
$ rpmbuild --define "_topdir $builddir/proton_build" -bp proton_build/SPECS/qpid-proton.spec
$ pushd proton_build/BUILD
$ tar -cvzf ../../qpid-proton-0.10-2.tar.gz qpid-proton-0.10
$ popd

Once these steps have been completed, build the source rpm for the
module in the local directory:

$ rpmbuild --define '_topdir .' --define '_sourcedir .' --define 'dist .el7' -bs rsyslog-omamqp1.spec

This source rpm can then be used to build the binary rpm on the target system.

Note about versioning:

The version number is a bit crazy.  It is an attempt to clearly
indicate the version of rsyslog and qpid-proton that this module is
compatible with.  The first 4 numbers are the version and release of
rsyslog used to build the module.  The next 4 numbers are the version
and release of the qpid-proton library used to build the module.

For example:

   rsyslog-omamqp1-8.15.0.1.0.10.2-1

Contains the omamqp1 output module for the rsyslog-8.15.0-1 package,
built with the qpid-proton-c-0.10-2 library.
