
$ builddir=`pwd`
$ mkdir -p rsyslog_build
$ wget https://copr-be.cloud.fedoraproject.org/results/portante/rsyslog-v8.15/epel-7-x86_64/00149031-rsyslog/rsyslog-8.15.0-1.el7.centos.src.rpm
$ rpm --define "_topdir $builddir/rsyslog_build" -i rsyslog-8.15.0-1.el7.centos.src.rpm
$ rpmbuild --define "_topdir $builddir/rsyslog_build" -bp rsyslog_build/SPECS/rsyslog.spec
$ pushd rsyslog_build/BUILD
$ tar -cvzf ../../rsyslog-8.15.0-1.tar.gz rsyslog-8.15.0
$ popd

$ mkdir -p proton_build
$ wget https://dl.fedoraproject.org/pub/epel/7/SRPMS/q/qpid-proton-0.10-2.el7.src.rpm
$ rpm --define "_topdir $builddir/proton_build" -i qpid-proton-0.10-2.el7.src.rpm
$ rpmbuild --define "_topdir $builddir/proton_build" -bp proton_build/SPECS/qpid-proton.spec
$ pushd proton_build/BUILD
$ tar -cvzf ../../qpid-proton-0.10-2.tar.gz qpid-proton-0.10
$ popd

$ rpmbuild --define '_topdir .' --define '_sourcedir .' --define 'dist .el7' -bs rsyslog-omamqp1.spec
