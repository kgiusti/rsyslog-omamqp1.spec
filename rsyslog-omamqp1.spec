%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/%{name}-%{version}
%if 0%{?rhel} >= 7
%global want_hiredis 0
%global want_mongodb 0
%else
%global want_hiredis 1
%global want_mongodb 1
%endif

%define PROTON_VERSION 0.10
%define PROTON_RELEASE 2
%define RSYSLOG_VERSION 8.15.0
%define RSYSLOG_RELEASE 1

# we provide these libraries privately, for use by the omamqp1 module, so
# don't want the automatic dependency generator creating a runtime dependency
# on the qpid-proton-c package, or advertising that this package provides
# qpid proton
%define __requires_exclude ^libqpid.*$
%define __provides_exclude ^libqpid.*$

Summary: Rsyslog AMQP v1 output module
Name: rsyslog-omamqp1
Version: %{RSYSLOG_VERSION}.%{RSYSLOG_RELEASE}.%{PROTON_VERSION}.%{PROTON_RELEASE}
Release: 1%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: qpid-proton-%{PROTON_VERSION}-%{PROTON_RELEASE}.tar.gz
Source1: rsyslog-%{RSYSLOG_VERSION}-%{RSYSLOG_RELEASE}.tar.gz

Patch0: 0001-Output-Module-for-AMQP-1.0-compliant-brokers.patch
Patch1: 0002-Fix-clang-compilation-warnings.patch

%description
rsyslog-omamqp1 provides the omamqp1 Rsyslog output module.  This
module sends log messages to an AMQP 1.0-compliant messaging bus.

#
# rsyslog requirements
#

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: dos2unix
BuildRequires: flex
BuildRequires: libtool
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libee-devel
BuildRequires: json-c-devel
BuildRequires: curl-devel
BuildRequires: libgt-devel
BuildRequires: python-docutils
BuildRequires: liblogging-stdlog-devel
%if 0%{?fedora}%{?rhel}>= 7
# make sure systemd is in a version that isn't affected by rhbz#974132
BuildRequires: systemd-devel >= 204-8
%endif
BuildRequires: zlib-devel
BuildRequires: qpid-proton-c-devel

Requires: libgt
Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: syslog
Obsoletes: sysklogd < 1.5-11

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql-devel >= 4.0

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.1.1
BuildRequires: librelp-devel >= 1.1.1
BuildRequires: libgcrypt-devel

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel

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

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

%package mmfields
Summary: mmfields support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

%package pmaixforwardedfrom
Summary: pmaixforwardedfrom support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmanon
Summary: mmanon support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmutf8fix
Summary: Fix invalid UTF-8 sequences in messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package ommail
Summary: Mail support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package pmciscoios
Summary: pmciscoios support
Group: System Environment/Daemons
Requires: %name = %version-%release

%if 0%{?fedora}0%{?rhel}>= 6
%package rsgtutil
Summary: RSyslog rsgtutil support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: %{name}-ksi = %version-%release

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libuuid-devel
BuildRequires: libcurl-devel

%if %{want_mongodb}
%package mongodb
Summary: MongoDB output support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package kafka
Summary: Kafka output support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: adiscon-librdkafka-devel

%package ksi
Summary: KSI signature support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: libksi <= 3.4.0.0
BuildRequires: libksi-devel

%package mmgrok
Summary: Grok pattern filtering support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: grok
BuildRequires: json-c-devel glib2-devel grok grok-devel tokyocabinet-devel
%endif

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libgcrypt-devel

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

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

%description mmjsonparse
This module provides support for parsing structured log messages that follow
the CEE/lumberjack specification.

%description mmnormalize
The rsyslog-mmnormalize package provides log normalization by using the
liblognorm and its Rulebase format.

%description mmfields
Parse all fields of the message into structured data inside the JSON tree.

%description pmaixforwardedfrom
This module cleans up messages forwarded from AIX.
Instead of actually parsing the message, this modifies the message and then
falls through to allow a later parser to handle the now modified message.

%description mmanon
IP Address Anonimization Module (mmanon).
It is a message modification module that actually changes the IP address
inside the message, so after calling mmanon, the original message can
no longer be obtained. Note that anonymization will break digital
signatures on the message, if they exist.

%description mmutf8fix
This module provides support for fixing invalid UTF-8 sequences. Most often,
such invalid sequences result from syslog sources sending in non-UTF character
sets, e.g. ISO 8859. As syslog does not have a way to convey the character
set information, these sequences are not properly handled.

%description pmciscoios
Parser module which supports various Cisco IOS formats.

%description ommail
Mail Output Module.
This module supports sending syslog messages via mail. Each syslog message
is sent via its own mail. The ommail plugin is primarily meant for alerting users.
As such, it is assume that mails will only be sent in an extremely
limited number of cases.

%description rsgtutil
Adds rsyslog utility used for GT and KSI signature verification and more.
For more information see the rsgtutil manual.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
ElasticSearch.

%if %{want_mongodb}
%description mongodb
MongoDB output plugin for rsyslog. This plugin allows rsyslog to write
the syslog messages to MongoDB, a scalable, high-performance,
open source NoSQL database.
%endif

%description kafka
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support. It was designed with message delivery
reliability and high performance in mind, current figures exceed 800000 msgs/second
for the producer and 3 million msgs/second for the consumer.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description ksi
The KSI signature plugin provides access to the Keyless Signature Infrastructure
globally distributed by Guardtime.

%description mmgrok
This module provides filtering based on grok patterns.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.


######################
# proton requirements
######################

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
autoreconf -iv
popd


%build

###############
# PROTON BUILD 
###############

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
make V=1
popd


###############################
# RSYSLOG OMAMQP1 MODULE BUILD 
###############################

pushd rsyslog-%{RSYSLOG_VERSION}

%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DSYSLOGD_PIDNAME=\\\"/var/run/syslogd.pid\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"/var/run/syslogd.pid\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS="-L%{_libdir} -lhiredis"
%endif
%configure \
        --prefix=/usr \
        --enable-generate-man-pages \
        --disable-static \
        --disable-testbench \
        --enable-uuid \
        --enable-elasticsearch \
%if %{want_mongodb}
        --enable-ommongodb \
%endif
        --enable-omkafka \
        --enable-usertools \
        --enable-gt-ksi \
        --enable-imjournal \
        --enable-omjournal \
        --enable-gnutls \
        --enable-imfile \
        --enable-impstats \
        --enable-imptcp \
        --enable-libdbi \
        --enable-mail \
        --enable-mysql \
        --enable-omprog \
        --enable-omudpspoof \
        --enable-omuxsock \
        --enable-pgsql \
        --enable-pmlastmsg \
        --enable-relp \
        --enable-snmp \
        --enable-unlimited-select \
        --enable-mmjsonparse \
        --enable-mmnormalize \
        --enable-mmanon \
        --enable-mmutf8fix \
        --enable-mail \
        --enable-mmfields \
        --enable-mmpstrucdata \
        --enable-mmsequence \
        --enable-pmaixforwardedfrom \
        --enable-pmciscoios \
        --enable-guardtime \
        --enable-mmgrok \
        --enable-gssapi-krb5 \
        --enable-mmaudit \
        --enable-mmcount \
        --enable-mmsnmptrapd \
%if %{want_hiredis}
        --enable-omhiredis \
%endif
        --enable-omrabbitmq \
        --enable-omstdout \
        --enable-pmcisconames \
        --enable-pmsnare \
        --enable-omamqp1

not-done-yet

./config.status --file=contrib/omamqp1/Makefile
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
