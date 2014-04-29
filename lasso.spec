#
# TODO
# - fix tests (some linkage errors)

# Conditional build:
%bcond_with	wsd		# wsd
%bcond_with	tests		# build tests
%bcond_without	java		# Java bindings
%bcond_without	php		# PHP bindings
%bcond_without	perl		# Perl bindings
%bcond_without	python		# Python 2.x bindings

Summary:	Liberty Alliance Single Sign On
Name:		lasso
Version:	2.4.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://dev.entrouvert.org/lasso/%{name}-%{version}.tar.gz
# Source0-md5:	3d04aaff37c816aa16f2d1bcc2639f27
Patch1:		0001-Fix-java-version-detection.patch
Patch2:		0001-Fix-generators-for-parsing-of-integer-values.patch
Patch3:		0002-xml-xml.c-fix-liberal-use-of-casting-for-the-SNIPPET.patch
URL:		http://lasso.entrouvert.org/
%{?with_wsf:BuildRequires: cyrus-sasl-devel}
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	swig
BuildRequires:	xmlsec1-devel
BuildRequires:	xmlsec1-openssl-devel
%if %{with php}
BuildRequires:	expat-devel
BuildRequires:	php-devel
BuildRequires:	python
%endif
%if %{with perl}
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
%endif
%if %{with java}
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-lxml
BuildRequires:	rpm-pythonprov
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to
handle the whole life-cycle of SAML based Federations, and provides
bindings for multiple languages.

%package devel
Summary:	Lasso development headers and documentation
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and
development documentation for Lasso.

%package -n perl-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Perl bindings
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
Perl language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%package -n java-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Java bindings
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils
Requires:	jre

%description -n java-%{name}
Java language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%package -n php-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) PHP bindings
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n php-%{name}
PHP language bindings for the lasso (Liberty Alliance Single Sign On)
library.

%package -n python-%{name}
Summary:	Liberty Alliance Single Sign On (lasso) Python bindings
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign
On) library.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i -e '
	s/OPTIMIZE="-g"/CC="%{__cc}" OPTIMIZE="%{rpmcflags}" INSTALLDIRS=vendor/
' bindings/perl/Makefile.am

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--disable-silent-rules \
	%{!?with_tests:--disable-tests} \
	%{!?with_java:--disable-java} \
	%{!?with_python:--disable-python} \
	%{!?with_perl:--disable-perl} \
%if %{with php}
	--enable-php5=yes \
	--with-php5-config-dir=%{php_sysconfdir}/conf.d \
%else
	--enable-php5=no \
%endif
%if %{with wsf}
	--enable-wsf \
	--with-sasl2=%{_prefix}/sasl2 \
%endif

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -v

# Perl subpackage
%if %{with perl}
rm $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Lasso/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Lasso/Lasso.bs
%endif

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

# Remove bogus doc files
rm -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/liblasso.so.*.*.*
%ghost %{_libdir}/liblasso.so.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblasso.so
%{_pkgconfigdir}/lasso.pc
%{_includedir}/lasso

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
%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/lasso.ini
%attr(755,root,root) %{php_extensiondir}/lasso.so
%{php_data_dir}/lasso.php
%endif

%if %{with python}
%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/lasso.py[co]
%attr(755,root,root) %{py_sitedir}/_lasso.so
%endif
