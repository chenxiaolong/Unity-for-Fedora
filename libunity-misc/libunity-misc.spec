# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu2

Name:		libunity-misc
Version:	4.0.4
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Differently licensed stuff for Unity

Group:		System Environment/Libraries
# GPLv3:
# - unity-misc/unity-misc.h
# GPLv2:
# - unity-misc/unity-tray-manager.h
# - shell-embedded-window-private.h
# - unity-tray-manager.c
# - shell-embedded-window.c
# - shell-gtk-embed.h
# - shell-gtk-embed.c
# - shell-embedded-window.h
# LGPLv2
# - All other files
License:	GPLv2 and GPLv3 and LGPLv2
URL:		https://launchpad.net/libunity-misc
Source0:	https://launchpad.net/libunity-misc/trunk/%{version}/+download/libunity-misc-%{version}.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/libunity-misc_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(x11)

%description
libunity-misc is a shared library that provides miscellaneous functions for
Unity.


%package devel
Summary:	Development files for libunity-misc
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)

%description devel
This package contains the development files for the unity-misc library.


%package docs
Summary:	Documentation for libunity-misc
Group:		Documentation

BuildArch:	noarch

%description docs
This package contains the documentation for the unity-misc library.


%prep
%setup -q

# Apply Ubuntu's patches
# - update-notifier systray icons showed and the wrong place and size
#   (LP: #856125)
zcat '%{SOURCE99}' | patch -Np1


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libunity-misc.so.*


%files devel
%doc AUTHORS
%dir %{_includedir}/unity-misc/
%dir %{_includedir}/unity-misc/unity-misc/
%{_includedir}/unity-misc/unity-misc/*.h
%{_libdir}/libunity-misc.so
%{_libdir}/pkgconfig/unity-misc.pc


%files docs
%dir %{_datadir}/gtk-doc/html/libunity-misc/


%changelog
* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.0.4-2.0ubuntu2
- Clean up spec file
- Use pkgconfig for dependencies
- Fix directory ownership

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.0.4-1.0ubuntu2
- Initial release
- Version 4.0.4
- Ubuntu release 0ubuntu2
