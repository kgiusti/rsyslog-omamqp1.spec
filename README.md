$ builddir=`pwd`
$ mkdir -p rsyslog_build
$ wget http://vault.centos.org/centos/7/os/Source/SPackages/rsyslog-7.4.7-12.el7.src.rpm
$ rpm --define "_topdir $builddir/rsyslog_build" -i rsyslog-7.4.7-12.el7.src.rpm
$ rpmbuild --define "_topdir $builddir/rsyslog_build" -bp rsyslog_build/SPECS/rsyslog.spec
$ pushd rsyslog_build/BUILD
$ tar -cvzf ../../rsyslog-7.4.7-12.tar.gz rsyslog-7.4.7
$ popd

$ mkdir -p proton_build
$ wget https://dl.fedoraproject.org/pub/epel/7/SRPMS/q/qpid-proton-0.10-2.el7.src.rpm
$ rpm --define "_topdir $builddir/proton_build" -i qpid-proton-0.10-2.el7.src.rpm
$ rpmbuild --define "_topdir $builddir/proton_build" -bp proton_build/SPECS/qpid-proton.spec
$ pushd proton_build/BUILD
$ tar -cvzf ../../qpid-proton-0.10-2.tar.gz qpid-proton-0.10
$ popd

$ rpmbuild --define '_topdir .' --define '_sourcedir .' --define 'dist .el7' -bs rsyslog-omamqp1.spec
