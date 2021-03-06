# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Do not provide the Python 3 binding library
%filter_provides_in %{python3_sitearch}/_geis_bindings\.so$
%filter_setup

Name:		geis
Version:	2.2.15daily13.04.03
Release:	1%{?dist}
Summary:	An implementation of the GEIS interface

Group:		System Environment/Libraries
License:	GPLv2 and LGPLv3
URL:		https://launchpad.net/geis
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/geis_%{version}.orig.tar.gz

BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	xmlto

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(evemu)
BuildRequires:	pkgconfig(grail)
BuildRequires:	pkgconfig(python3)
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
Summary:	Python 3 bindings for the geis library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-geis
This package contains the Python 3 bindings for the geis library.


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

autoreconf -vfi


%build
%configure --disable-static --with-evemu
make %{?_smp_mflags}

# Build HTML documentation
make -C doc doc-html


%install
make install DESTDIR=$RPM_BUILD_ROOT pythondir=%{python3_sitearch}

# Install HTML documentation
make -C doc install-html

# Verify desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/geisview.desktop

# Put documentation in correct directory
mv $RPM_BUILD_ROOT%{_docdir}/geis/ \
   $RPM_BUILD_ROOT%{_docdir}/geis-docs-%{version}/

# Avoid rpmlint non-executable-script error
sed -i '/^#[ \t]*\!/d' $RPM_BUILD_ROOT%{python3_sitearch}/geisview/__init__.py

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
%{python3_sitearch}/geis/
%{python3_sitearch}/geisview/
%{python3_sitearch}/_geis_bindings.so


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
%{_mandir}/man1/geisview.1.gz
%{_mandir}/man1/pygeis.1.gz
%{_datadir}/pixmaps/geisview32x32.xpm


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.15daily13.04.03-1
- Version 2.2.15daily13.04.03

* Tue Jan 29 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.15daily12.12.10-1
- Version 2.2.15daily12.12.10
- Add build dependency for Python 3

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.14-1.0ubuntu2
- Version 2.2.14
- Ubuntu release 0ubuntu2

* Sun Oct 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.12-1.0ubuntu2
- Ubuntu release 0ubuntu2
  - Fix Geisv1 gesture class IDs (LP: #1047596)

* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.12-1
- Version 2.2.12

* Fri Jul 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.11-1
- Version 2.2.11
- Upstream renamed from utouch-geis to geis

* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.10-1
- Initial release
- Version 2.2.10
