%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/%{name}-%{version}
%if 0%{?rhel} >= 7
%global want_hiredis 0
%global want_mongodb 0
%global want_rabbitmq 0
%else
%global want_hiredis 1
%global want_mongodb 1
%global want_rabbitmq 1
%endif

%define PROTON_VERSION 0.10
%define PROTON_RELEASE 2
%define RSYSLOG_VERSION 7.4.7
%define RSYSLOG_RELEASE 12

# we provide these libraries privately, for use by the omamqp1 module, so
# don't want the automatic dependency generator creating a runtime dependency
# on the qpid-proton-c package, or advertising that this package provides
# qpid proton
%define __requires_exclude ^libqpid.*$
%define __provides_exclude ^libqpid.*$

Summary: Rsyslog AMQP v1 output module
Name: rsyslog-omamqp1
Version: 7.4.7
Release: 12%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: qpid-proton-%{PROTON_VERSION}-%{PROTON_RELEASE}.tar.gz
Source1: rsyslog-%{RSYSLOG_VERSION}-%{RSYSLOG_RELEASE}.tar.gz

Patch0: 0001-omamqp1-it-compiles.patch
Patch1: 0002-Debug-stuff-trying-to-understand-the-reactor-api.patch
Patch2: 0003-Basic-functionality-done-mostly-stable.patch
Patch3: 0004-fix-configuration-add-readme-doc.patch
Patch4: 0005-fix-compilation-warnings-on-RHEL7.patch
Patch5: 0006-Fix-the-reference-counting-and-various-leaks.patch
Patch6: 0007-URL-support-added-old-SASL-PLAIN-config.patch
Patch7: 0008-Fixed-errors-when-handling-undeliverable-messages.-U.patch

#
# rsyslog requirements
#

BuildRequires: bison
BuildRequires: flex
BuildRequires: json-c-devel
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
# make sure systemd is in a version that isn't affected by rhbz#974132
BuildRequires: systemd-devel >= 204-8
BuildRequires: zlib-devel
# BuildRequires: qpid-proton-c-devel

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libgcrypt-devel

%package doc
Summary: HTML Documentation for rsyslog
Group: Documentation

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libee-devel liblognorm-devel

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql >= 4.0
BuildRequires: mysql-devel >= 4.0

%if %{want_mongodb}
%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%if %{want_rabbitmq}
%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2
%endif

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.0.3
BuildRequires: librelp-devel >= 1.0.3

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel



%description
Rsyslog-omamqp1 is an AMQP v1 output module for rsyslog that uses QPID Proton
as the implementation.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%description doc
This subpackage contains documentation for rsyslog.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%if %{want_mongodb}
%description mongodb
The rsyslog-mongodb package contains a dynamic shared object that will add
MongoDB database support to rsyslog.
%endif

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%if %{want_rabbitmq}
%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.
%endif

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

#
# proton requirements
#

BuildRequires:  cmake >= 2.6
BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  epydoc
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  cyrus-sasl-devel
Requires:       cyrus-sasl-lib
Requires:       openssl




%prep
%setup -c -n rsyslog-omamqp1 -T -a 0 -a 1
pushd rsyslog-%{RSYSLOG_VERSION}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
popd


%build

## PROTON BUILD ##
pushd qpid-proton-%{PROTON_VERSION}

# add for next rebase:
#    -DBUILD_CPP=OFF \
#    -DBUILD_GO=OFF \
%cmake \
    -DBUILD_JAVA=OFF \
    -DBUILD_JAVASCRIPT=OFF \
    -DBUILD_PERL=OFF \
    -DBUILD_PHP=OFF \
    -DBUILD_PYTHON=OFF \
    -DBUILD_RUBY=OFF \
    -DBUILD_TESTING=OFF \
    .
popd

## RSYSLOG OMAMQP1 MODULE BUILD ##

pushd rsyslog-%{RSYSLOG_VERSION}
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DSYSLOGD_PIDNAME=\\\"syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS=-L%{_libdir}
%endif
%configure \
	--prefix=/usr \
	--disable-static \
	--disable-testbench \
	--enable-elasticsearch \
	--enable-gnutls \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp \
	--enable-libdbi \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mysql \
%if %{want_hiredis}
	--enable-omhiredis \
%endif
	--enable-omjournal \
%if %{want_mongodb}
	--enable-ommongodb \
%endif
	--enable-omprog \
%if %{want_rabbitmq}
	--enable-omrabbitmq \
%endif
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmrfc3164sd \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \
        --enable-omamqp1

poopybum

./config.status --file=plugins/omamqp1/Makefile
PKG_CONFIG=${PKG_CONFIG:-pkg-config}
PROTON_CFLAGS=`$PKG_CONFIG --cflags "libqpid-proton >= 0.9" 2>/dev/null`
PROTON_LIBS=`$PKG_CONFIG --libs "libqpid-proton >= 0.9" 2>/dev/null`
sed -i -e "s/@PROTON_CFLAGS@/${PROTON_CFLAGS}/g" \
    -e "s/@PROTON_LIBS@/${PROTON_LIBS}/g" \
    plugins/omamqp1/Makefile
LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C plugins/omamqp1

%install
LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C plugins/omamqp1 DESTDIR=%{buildroot} install

# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# private version of qpid
install -d -m 755 %{buildroot}%{_libdir}/rsyslog/qpid-proton-c
install -p -m 755 %{_libdir}/libqpid* %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/
rm -f %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/*.so

%files
%defattr(-,root,root,-)
# plugins
%{_libdir}/rsyslog/omamqp1.so
%{_libdir}/rsyslog/qpid-proton-c

%changelog
* Mon Feb  1 2016 Rich Megginson <rmeggins@redhat.com> 7.4.7-12
- initial commit - hacked rsyslog.spec
