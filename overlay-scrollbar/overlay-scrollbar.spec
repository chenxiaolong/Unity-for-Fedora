# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		overlay-scrollbar
Version:	0.2.16
Release:	1%{?dist}
Summary:	Overlayed scrollbar widget for GTK

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://launchpad.net/ayatana-scrollbar
Source0:	https://launchpad.net/ayatana-scrollbar/0.2/%{version}/+download/overlay-scrollbar-%{version}.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake

BuildRequires:	cairo-devel
BuildRequires:	glib2-devel
# Ubuntu's patched gtk required
BuildRequires:	gtk2-ubuntu-devel
BuildRequires:	gtk3-ubuntu-devel

%if 0%{?opensuse_bs}
# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel
%endif

%description
(contains no files)


%package gtk2
Summary:	GTK 2 overlayed scrollbar widget
Group:		System Environment/Libraries

Requires:	gtk2-ubuntu

%description gtk2
This package contains a GTK 2 widget allowing for a overlayed scrollbar.


%package gtk2-devel
Summary:	Development files for overlay-scrollbar-gtk2
Group:		Development/Libraries

Requires:	%{name}-gtk2%{?_isa} = %{version}-%{release}
Requires:	cairo-devel
Requires:	glib2-devel

%description gtk2-devel
This package contains the development files for the GTK 2 overlayed scollbar
widget.


%package gtk3
Summary:	GTK 3 overlayed scrollbar widget
Group:		System Environment/Libraries

Requires:	gtk3-ubuntu

%description gtk3
This package contains a GTK 3 widget allowing for a overlayed scrollbar.


%package gtk3-devel
Summary:	Development files for overlay-scrollbar-gtk3
Group:		Development/Libraries

Requires:	%{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:	cairo-devel
Requires:	glib2-devel

%description gtk3-devel
This package contains the development files for the GTK 3 overlayed scrollbar
widget.


%prep
%setup -q


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Remove X11 startup script (not needed)
rm $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xsession.d/81overlay-scrollbar


%post gtk2 -p /sbin/ldconfig

%postun gtk2 -p /sbin/ldconfig


%post gtk3 -p /sbin/ldconfig

%postun gtk3 -p /sbin/ldconfig


%files gtk2
%doc AUTHORS NEWS
%{_libdir}/liboverlay-scrollbar-0.2.so.0
%{_libdir}/liboverlay-scrollbar-0.2.so.0.0.16


%files gtk2-devel
%doc AUTHORS NEWS
%dir %{_includedir}/overlay-scrollbar-0.2/
%dir %{_includedir}/overlay-scrollbar-0.2/os/
%{_includedir}/overlay-scrollbar-0.2/os/os-scrollbar.h
%{_includedir}/overlay-scrollbar-0.2/os/os-utils.h
%{_includedir}/overlay-scrollbar-0.2/os/os-version.h
%{_includedir}/overlay-scrollbar-0.2/os/os.h
%{_libdir}/liboverlay-scrollbar-0.2.so
%{_libdir}/pkgconfig/overlay-scrollbar-0.2.pc


%files gtk3
%doc AUTHORS NEWS
%{_libdir}/liboverlay-scrollbar3-0.2.so.0
%{_libdir}/liboverlay-scrollbar3-0.2.so.0.0.16


%files gtk3-devel
%doc AUTHORS NEWS
%dir %{_includedir}/overlay-scrollbar3-0.2/
%dir %{_includedir}/overlay-scrollbar3-0.2/os/
%{_includedir}/overlay-scrollbar3-0.2/os/os-scrollbar.h
%{_includedir}/overlay-scrollbar3-0.2/os/os-utils.h
%{_includedir}/overlay-scrollbar3-0.2/os/os-version.h
%{_includedir}/overlay-scrollbar3-0.2/os/os.h
%{_libdir}/liboverlay-scrollbar3-0.2.so
%{_libdir}/pkgconfig/overlay-scrollbar3-0.2.pc


%changelog
* Sat Jul 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.16-1
- Initial release
- Version 0.2.16
