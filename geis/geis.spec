# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Do not provide the Python 2 binding library
%filter_provides_in %{python_sitearch}/_geis_bindings\.so$
%filter_setup

Name:		geis
Version:	2.2.12
Release:	1%{?dist}
Summary:	An implementation of the GEIS interface

Group:		System Environment/Libraries
License:	GPLv2 and LGPLv3
URL:		https://launchpad.net/geis
Source0:	https://launchpad.net/geis/trunk/%{version}/+download/geis-%{version}.tar.xz

BuildRequires:	asciidoc
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	xmlto

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(evemu)
BuildRequires:	pkgconfig(grail)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xorg-server)

%description
GEIS is a library for applications and toolkit programmers which provides a
consistent platform independent interface for any system-wide input gesture
recognition mechanism.


%package devel
Summary:	Development files for the geis library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the geis library.


%package -n python-geis
Summary:	Python 2 bindings for the geis library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-geis
This package contains the Python 2 bindings for the geis library.


%package docs
Summary:	Documentation for the geis library
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the geis library.


%package tools
Summary:	Gesture Recognition And Instantiation Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python-geis%{?_isa} = %{version}-%{release}

%description tools
This package contains the testing tools for the geis library.


%prep
%setup -q

# Fix Python architecture-dependant site-packages directory
#sed -i '/am_cv_python_pythondir=/ s/lib/%{_lib}/g' aclocal.m4


%build
%configure --disable-static --with-evemu
make %{?_smp_mflags}

# Build HTML documentation
make -C doc doc-html


%install
make install DESTDIR=$RPM_BUILD_ROOT pythondir=%{python_sitearch}

# Install HTML documentation
make -C doc install-html

# Verify desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/geisview.desktop

# Put documentation in correct directory
mv $RPM_BUILD_ROOT%{_docdir}/geis/ \
   $RPM_BUILD_ROOT%{_docdir}/geis-docs-%{version}/

# Avoid rpmlint non-executable-script error
sed -i '/^#[ \t]*\!/d' $RPM_BUILD_ROOT%{python_sitearch}/geisview/__init__.py

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog NEWS README
%{_libdir}/libgeis.so.*


%files devel
%doc ChangeLog NEWS README
%dir %{_includedir}/geis/
%{_includedir}/geis/geis.h
%{_includedir}/geis/geisimpl.h
%{_libdir}/libgeis.so
%{_libdir}/pkgconfig/libgeis.pc


%files -n python-geis
%doc ChangeLog NEWS README
%dir %{python_sitearch}/geis/
%{python_sitearch}/geis/__init__.py*
%{python_sitearch}/geis/geis_v2.py*
%dir %{python_sitearch}/geisview/
%{python_sitearch}/geisview/__init__.py*
%{python_sitearch}/geisview/classview.py*
%{python_sitearch}/geisview/defaults.py*
%{python_sitearch}/geisview/deviceview.py*
%{python_sitearch}/geisview/filter_definition.py*
%{python_sitearch}/geisview/filter_list.py*
%{python_sitearch}/_geis_bindings.so


%files docs
%doc %{_docdir}/geis-docs-%{version}/


%files tools
%{_bindir}/geis-server
%{_bindir}/geistest
%{_bindir}/geisview
%{_bindir}/pygeis
%{_datadir}/applications/geisview.desktop
%dir %{_datadir}/geisview/
%{_datadir}/geisview/filter_definition.ui
%{_datadir}/geisview/filter_list.ui
%{_datadir}/geisview/geisview.ui
%{_mandir}/man1/geistest.1.gz
%{_datadir}/pixmaps/geisview32x32.xpm


%changelog
* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.12-1
- Version 2.2.12

* Fri Jul 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.11-1
- Version 2.2.11
- Upstream renamed from utouch-geis to geis

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.10-1
- Initial release
- Version 2.2.10
