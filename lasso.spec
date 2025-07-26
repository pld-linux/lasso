#
# TODO
# - fix tests (some linkage errors)
#
# Conditional build:
%bcond_with	wsf		# experimental ID-WSF support
%bcond_with	tests		# build tests
%bcond_with	java		# Java bindings
%bcond_with	php		# PHP 5 bindings (not ready for PHP 7)
%bcond_without	perl		# Perl bindings
%bcond_without	python		# Python 3.x bindings
%bcond_without	static_libs	# static library

%if "%{?php_suffix}" == ""
%define		php_suffix	55
%endif
%define		php_name	php%{?php_suffix}
Summary:	Liberty Alliance Single Sign On
Summary(pl.UTF-8):	Implementacja Liberty Alliance Single Sign On
Name:		lasso
Version:	2.8.2
Release:	7
License:	GPL v2+
Group:		Libraries
Source0:	https://dev.entrouvert.org/lasso/%{name}-%{version}.tar.gz
# Source0-md5:	ad2e167973cc1c21cd16329bfbcd3d16
Patch0:		git.patch
URL:		https://lasso.entrouvert.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.11
%{?with_tests:BuildRequires:	check-devel}
%{?with_wsf:BuildRequires: cyrus-sasl-devel >= 2}
BuildRequires:	glib2-devel >= 1:2.17.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	xmlsec1-devel >= 1.2.6
BuildRequires:	xmlsec1-openssl-devel >= 1.2.6
BuildRequires:	zlib-devel
%if %{with php}
BuildRequires:	expat-devel
BuildRequires:	%{php_name}-devel >= 5
BuildRequires:	python3
%endif
%if %{with perl}
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-Test-Simple
%endif
%if %{with java}
BuildRequires:	jdk >= 1.4
BuildRequires:	rpm-javaprov
%endif
%if %{with python}
BuildRequires:	python3-devel
BuildRequires:	python3-lxml
BuildRequires:	rpm-pythonprov
%endif
Requires:	glib2 >= 1:2.17.0
Requires:	xmlsec1 >= 1.2.6
Requires:	xmlsec1-openssl >= 1.2.6
%if %{without java}
Obsoletes:	java-lasso < %{version}-%{release}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to
handle the whole life-cycle of SAML based Federations, and provides
bindings for multiple languages.

%description -l pl.UTF-8
Lasso to biblioteka implementująca standardy Liberty Alliance Single
Sign On, w tym specyfikacje SAML i SAML2. Pozwala obsłużyć cały cykl
życia "Federacji" opartych na SAML, zapewnia wiązania dla wielu
języków.

%package devel
Summary:	Lasso development headers
Summary(pl.UTF-8):	Pliki nagłówkowe Lasso
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.17.0
Requires:	libxml2-devel >= 2.0
Requires:	libxslt-devel
Requires:	xmlsec1-devel >= 1.2.6

%description devel
This package contains the header files for Lasso.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe Lasso.

%package static
Summary:	Static lasso library
Summary(pl.UTF-8):	Statyczna biblioteka lasso
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lasso library.

%description static -l pl.UTF-8
Statyczna biblioteka lasso.

%package -n perl-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Perl bindings
Summary(pl.UTF-8):	Wiązania Perla do Liberty Alliance Single Sign On (lasso)
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%description -n perl-%{name} -l pl.UTF-8
Wiązania Perla do biblioteki lasso (Liberty Alliance Single Sign On).

%package -n java-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Java bindings
Summary(pl.UTF-8):	Wiązania Javy do Liberty Alliance Single Sign On (lasso)
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils
Requires:	jre

%description -n java-%{name}
Java language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%description -n java-%{name} -l pl.UTF-8
Wiązania Javy do biblioteki lasso (Liberty Alliance Single Sign On).

%package -n %{php_name}-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) PHP bindings
Summary(pl.UTF-8):	Wiązania PHP do Liberty Alliance Single Sign On (lasso)
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-%{name}
PHP language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%description -n %{php_name}-%{name} -l pl.UTF-8
Wiązania PHP do biblioteki lasso (Liberty Alliance Single Sign On).

%package -n python3-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do Liberty Alliance Single Sign On (lasso)
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-lasso < 2.7

%description -n python3-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign
On) library.

%description -n python3-%{name} -l pl.UTF-8
Wiązania Pythona do biblioteki lasso (Liberty Alliance Single Sign
On).

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e 's|OPTIMIZE="-g"|CC="%{__cc}" OPTIMIZE="%{rpmcflags}" INSTALLDIRS=vendor|' \
	bindings/perl/Makefile.am

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_java:--disable-java} \
	%{!?with_perl:--disable-perl} \
%if %{with php}
	--enable-php5 \
	--with-php5-config-dir=%{php_sysconfdir}/conf.d \
%else
	--disable-php5 \
%endif
	%{!?with_python:--disable-python} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_tests:--disable-tests} \
%if %{with wsf}
	--enable-wsf \
	--with-sasl2 \
%endif
	--with-html-dir=%{_gtkdocdir}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.la' | xargs %{__rm} -v

%if %{with static_libs}
%{?with_java:%{__rm} $RPM_BUILD_ROOT%{_jnidir}/libjnilasso.a}
%{?with_php:%{__rm} $RPM_BUILD_ROOT%{php_extensiondir}/lasso.a}
%{?with_python:%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_lasso.a}
%endif

# Perl subpackage
%if %{with perl}
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Lasso/.packlist
%endif

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

# Remove bogus doc files
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/liblasso.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblasso.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblasso.so
%{_pkgconfigdir}/lasso.pc
%{_includedir}/lasso

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblasso.a
%endif

%if %{with perl}
%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Lasso.pm
%dir %{perl_vendorarch}/auto/Lasso
%attr(755,root,root) %{perl_vendorarch}/auto/Lasso/Lasso.so
%endif

%if %{with java}
%files -n java-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_jnidir}/libjnilasso.so
%{_javadir}/lasso.jar
%endif

%if %{with php}
%files -n %{php_name}-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/lasso.ini
%attr(755,root,root) %{php_extensiondir}/lasso.so
%{php_data_dir}/lasso.php
%endif

%if %{with python}
%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/__pycache__
%{py3_sitedir}/lasso.py
%attr(755,root,root) %{py3_sitedir}/_lasso.so
%endif
