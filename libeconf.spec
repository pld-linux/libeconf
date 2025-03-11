#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	python		# Python (3.x) binding
%bcond_without	static_libs	# static libraries
%bcond_without	tests
#
Summary:	Highly flexible library to manage key=value configuration files
Summary(pl.UTF-8):	Elastyczna biblioteka do zarządzania plikami konfiguracyjnymi klucz=wartość
Name:		libeconf
Version:	0.6.2
Release:	3
License:	MIT
Group:		Libraries
Source0:	https://github.com/openSUSE/libeconf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cd90a83892540594b5785546984d5a1a
URL:		https://github.com/openSUSE/libeconf
BuildRequires:	doxygen
BuildRequires:	meson >= 0.49
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
%if %{with python}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:61
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libeconf is a highly flexible and configurable library to parse and
manage key=value configuration files. It reads configuration file
snippets from different directories and builds the final configuration
file for the application from it.

%description -l pl.UTF-8
libeconf to bardzo elastyczna i konfigurowalna biblioteka do analizy i
zarządzania plikami konfiguracyjnymi klucz=wartość. Wczytuje kawałki
plików konfiguracyjnych z różnych katalogów i buduje z nich ostateczny
plik konfiguracyjny dla aplikacji.

%package devel
Summary:	Header files for libeconf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libeconf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libeconf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libeconf.

%package static
Summary:	Static libeconf library
Summary(pl.UTF-8):	Statyczna biblioteka libeconf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libeconf library.

%description static -l pl.UTF-8
Statyczna biblioteka libeconf.

%package apidocs
Summary:	API documentation for libeconf library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libeconf
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libeconf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libeconf.

%package -n python3-libeconf
Summary:	Python 3 bindings for libeconf
Summary(pl.UTF-8):	Wiązania Pythona 3 do libeconf
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n python3-libeconf
Python 3 bindings for libeconf.

%description -n python3-libeconf -l pl.UTF-8
Wiązania Pythona 3 do libeconf.

%prep
%setup -q

cat >bindings/python3/setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%meson build

%ninja_build -C build

%if %{with python}
cd bindings/python3
%py3_build
cd ../..
%endif

%if %{with tests}
%ninja_test -C build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with python}
cd bindings/python3
%py3_install

cp -p docs/python-libeconf.3 $RPM_BUILD_ROOT%{_mandir}/man3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README.md TODO.md
%attr(755,root,root) %{_bindir}/econftool
%attr(755,root,root) %{_libdir}/libeconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeconf.so.0
%{_mandir}/man8/econftool.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeconf.so
%{_includedir}/libeconf.h
%{_includedir}/libeconf_ext.h
%{_pkgconfigdir}/libeconf.pc
%{_mandir}/man3/libeconf.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeconf.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif

%if %{with python}
%files -n python3-libeconf
%defattr(644,root,root,755)
%{py3_sitescriptdir}/econf.py
%{py3_sitescriptdir}/__pycache__/econf.cpython-*.py[co]
%{py3_sitescriptdir}/python_libeconf-0.6.0-py*.egg-info
%{_mandir}/man3/python-libeconf.3*
%endif
