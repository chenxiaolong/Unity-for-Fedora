# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Do not provide the Python 2 binding library
%filter_provides_in %{python_sitearch}/_geis_bindings\.so$
%filter_setup

Name:		utouch-geis
Version:	2.2.10
Release:	1%{?dist}
Summary:	An implementation of the GEIS interface

Group:		System Environment/Libraries
License:	GPLv2 and LGPLv3
URL:		https://launchpad.net/utouch-geis
Source0:	https://launchpad.net/utouch-geis/trunk/utouch-geis-%{version}/+download/utouch-geis-%{version}.tar.xz

Patch0:		0001_evemu.patch

BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	libxcb-devel
BuildRequires:	libXi-devel
BuildRequires:	python2-devel
BuildRequires:	evemu-devel
BuildRequires:	utouch-grail-devel
BuildRequires:	xcb-proto
BuildRequires:	xorg-x11-server-devel
BuildRequires:	xmlto

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel
%endif

%description
GEIS is a library for applications and toolkit programmers which provides a
consistent platform independent interface for any system-wide input gesture
recognition mechanism.


%package devel
Summary:	Development files for the utouch-geis library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the utouch-geis library.


%package -n python-utouch-geis
Summary:	Python 2 bindings for the utouch-geis library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-utouch-geis
This package contains the Python 2 bindings for the utouch-geis library.


%package docs
Summary:	Documentation for the utouch-geis library
Group:		Documentation

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description docs
This package contains the documentation for the utouch-geis library.


%package tools
Summary:	Gesture Recognition And Instantiation Library - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python-utouch-geis%{?_isa} = %{version}-%{release}

%description tools
This package contains the testing tools for the utouch-geis library.


%prep
%setup -q

%patch0 -p1 -b .evemu

autoreconf -vfi

# Fix Python architecture-dependant site-packages directory
sed -i '/am_cv_python_pythondir=/ s/lib/%{_lib}/g' aclocal.m4


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
mv $RPM_BUILD_ROOT%{_docdir}/utouch-geis/ \
   $RPM_BUILD_ROOT%{_docdir}/utouch-geis-docs-%{version}/

# Avoid rpmlint non-executable-script error
sed -i '/^#[ \t]*\!/d' $RPM_BUILD_ROOT%{python_sitearch}/geisview/__init__.py

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog NEWS README
%{_libdir}/libutouch-geis.so.1
%{_libdir}/libutouch-geis.so.1.3.0


%files devel
%doc ChangeLog NEWS README
%{_includedir}/geis/geis.h
%{_includedir}/geis/geisimpl.h
%{_libdir}/libutouch-geis.so
%{_libdir}/pkgconfig/libutouch-geis.pc


%files -n python-utouch-geis
%doc ChangeLog NEWS README
%{python_sitearch}/geis/__init__.py*
%{python_sitearch}/geis/geis_v2.py*
%{python_sitearch}/geisview/__init__.py*
%{python_sitearch}/geisview/classview.py*
%{python_sitearch}/geisview/defaults.py*
%{python_sitearch}/geisview/deviceview.py*
%{python_sitearch}/geisview/filter_definition.py*
%{python_sitearch}/geisview/filter_list.py*
%{python_sitearch}/_geis_bindings.so


%files docs
%{_docdir}/utouch-geis-docs-%{version}/Doxyfile
%{_docdir}/utouch-geis-docs-%{version}/geisspec-1.0.asc
%{_docdir}/utouch-geis-docs-%{version}/geisspec-docbook.xml
%{_docdir}/utouch-geis-docs-%{version}/html/*.css
%{_docdir}/utouch-geis-docs-%{version}/html/*.html
%{_docdir}/utouch-geis-docs-%{version}/html/*.js
%{_docdir}/utouch-geis-docs-%{version}/html/*.png
%{_docdir}/utouch-geis-docs-%{version}/html/search/*.css
%{_docdir}/utouch-geis-docs-%{version}/html/search/*.html
%{_docdir}/utouch-geis-docs-%{version}/html/search/*.js
%{_docdir}/utouch-geis-docs-%{version}/html/search/*.png


%files tools
%{_bindir}/geis-server
%{_bindir}/geistest
%{_bindir}/geisview
%{_bindir}/pygeis
%{_datadir}/applications/geisview.desktop
%{_datadir}/geisview/filter_definition.ui
%{_datadir}/geisview/filter_list.ui
%{_datadir}/geisview/geisview.ui
%{_mandir}/man1/geistest.1.gz
%{_datadir}/pixmaps/geisview32x32.xpm


%changelog
* Fri Jun 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.2.10-1
- Initial release
- Version 2.2.10
