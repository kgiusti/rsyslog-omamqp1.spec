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
Release: 4%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: qpid-proton-%{PROTON_VERSION}-%{PROTON_RELEASE}.tar.gz
Source1: rsyslog-%{RSYSLOG_VERSION}-%{RSYSLOG_RELEASE}.tar.gz

Patch0: 0001-Output-Module-for-AMQP-1.0-compliant-brokers.patch
Patch1: 0002-Fix-clang-compilation-warnings.patch

# directory structure under BUILD/
%define proton_build %{_builddir}/rsyslog-omamqp1/qpid-proton-%{PROTON_VERSION}
%define rsyslog_build %{_builddir}/rsyslog-omamqp1/rsyslog-%{RSYSLOG_VERSION}


%description
rsyslog-omamqp1 provides the omamqp1 Rsyslog output module.  This
module sends log messages to an AMQP 1.0-compliant messaging bus.

Requires: rsyslog-%{RSYSLOG_VERSION}-%{RSYSLOG_RELEASE}

######################
# rsyslog requirements
######################

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

Requires: libgt
Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

#Provides: syslog
#Obsoletes: sysklogd < 1.5-11

#%package libdbi
#Summary: Libdbi database support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: libdbi-devel

#%package mysql
#Summary: MySQL support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: mysql-devel >= 4.0

#%package pgsql
#Summary: PostgresSQL support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: postgresql-devel

#%package gssapi
#Summary: GSSAPI authentication and encryption support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: krb5-devel

#%package relp
#Summary: RELP protocol support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
Requires: librelp >= 1.1.1
BuildRequires: librelp-devel >= 1.1.1
BuildRequires: libgcrypt-devel

#%package gnutls
#Summary: TLS protocol support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel

#%package snmp
#Summary: SNMP protocol support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: net-snmp-devel

#%package udpspoof
#Summary: Provides the omudpspoof module
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: libnet-devel

#%package mmjsonparse
#Summary: JSON enhanced logging support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

#%package mmnormalize
#Summary: Log normalization support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

#%package mmfields
#Summary: mmfields support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: liblognorm-devel >= 1.1.2

#%package pmaixforwardedfrom
#Summary: pmaixforwardedfrom support
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package mmanon
#Summary: mmanon support
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package mmutf8fix
#Summary: Fix invalid UTF-8 sequences in messages
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package ommail
#Summary: Mail support
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package pmciscoios
#Summary: pmciscoios support
#Group: System Environment/Daemons
# Requires: %name = %version-%release

%if 0%{?fedora}0%{?rhel}>= 6
#%package rsgtutil
#Summary: RSyslog rsgtutil support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
Requires: %{name}-ksi = %version-%release

#%package elasticsearch
#Summary: ElasticSearch output module for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: libuuid-devel
BuildRequires: libcurl-devel

%if %{want_mongodb}
#%package mongodb
#Summary: MongoDB output support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

#%package kafka
#Summary: Kafka output support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: adiscon-librdkafka-devel

#%package ksi
#Summary: KSI signature support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
Requires: libksi <= 3.4.0.0
BuildRequires: libksi-devel

#%package mmgrok
#Summary: Grok pattern filtering support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
Requires: grok
BuildRequires: json-c-devel glib2-devel grok grok-devel tokyocabinet-devel
%endif

%if %{want_hiredis}
#%package hiredis
#Summary: Redis support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

#%package mmaudit
#Summary: Message modification module supporting Linux audit format
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package mmsnmptrapd
#Summary: Message modification module for snmptrapd generated messages
#Group: System Environment/Daemons
# Requires: %name = %version-%release

#%package rabbitmq
#Summary: RabbitMQ support for rsyslog
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2

#%package crypto
#Summary: Encryption support
#Group: System Environment/Daemons
# Requires: %name = %version-%release
BuildRequires: libgcrypt-devel



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
%setup -q -c -n rsyslog-omamqp1 -T -a 0 -a 1
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

# Let configure know where the bundled proton includes and libs are
#
export PROTON_CFLAGS="-I%{proton_build}/proton-c/include"
export PROTON_LIBS="-L%{proton_build}/proton-c -lqpid-proton"

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

LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C contrib/omamqp1


%install
pushd rsyslog-%{RSYSLOG_VERSION}
LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C contrib/omamqp1 DESTDIR=%{buildroot} install

# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# install private version of libqpid-proton
install -d -m 755 %{buildroot}%{_libdir}/rsyslog/qpid-proton-c
install -p -m 755 %{proton_build}/proton-c/libqpid-proton.so* %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/
rm -f %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/*.so

%files
%defattr(-,root,root,-)
# plugins
%{_libdir}/rsyslog/omamqp1.so
%{_libdir}/rsyslog/qpid-proton-c

%changelog
* Tue Mar 01 2016 Kenneth Giusti - 8.15.0.1.0.10.2-4
- Remove qpid-proton-c-devel BuildRequires.  Not needed as the proton sources
  are included in the package

* Mon Feb 22 2016 Kenneth Giusti - 8.15.0.1.0.10.2-3
- Remove rsyslog subpackage info

* Sun Feb 21 2016 Kenneth Giusti - 8.15.0.1.0.10.2-2
- Shamelessly stolen from Rich's original work.  Modified to build a private
  copy of the proton library.

* Mon Feb  1 2016 Rich Megginson <rmeggins@redhat.com> 7.4.7-12
- initial commit - hacked rsyslog.spec
