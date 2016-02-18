$ wget http://vault.centos.org/centos/7/os/Source/SPackages/rsyslog-7.4.7-12.el7.src.rpm
$ rpm -i rsyslog-7.4.7-12.el7.src.rpm
$ rpmbuild -bp ~/rpmbuild/SPECS/rsyslog.spec
$ tar -cvzf rsyslog-7.4.7-12.tar.gz ~/rpmbuild/BUILD/rsyslog-7.4.7

$ wget https://dl.fedoraproject.org/pub/epel/7/SRPMS/q/qpid-proton-0.10-2.el7.src.rpm
$ rpm -i qpid-proton-0.10-2.el7.src.rpm
$ rpmbuild -bp ~/rpmbuild/SPECS/qpid-proton.spec
$ tar -cvzf qpid-proton-0.10-2.tar.gz ~/rpmbuild/BUILD/qpid-proton-0.10
