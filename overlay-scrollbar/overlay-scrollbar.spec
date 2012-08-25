# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _bzr_rev 353
%define _ubuntu_rel 0ubuntu2

# Workaround: the overlay-scrollbar needs to be noarch, but the subpackages
# need to be arch-dependent. RPM doesn't support this.
Name:		abcdefghijklmnopqrstuvwxyz
Version:	0.2.16
Release:	1.bzr%{_bzr_rev}.%{_ubuntu_rel}%{?dist}
Summary:	Overlayed scrollbar widget for GTK

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://launchpad.net/ayatana-scrollbar
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/overlay-scrollbar_%{version}+r%{_bzr_rev}-%{_ubuntu_rel}.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(glib-2.0)
# Ubuntu's patched gtk required
BuildRequires:	gtk2-ubuntu-devel
BuildRequires:	gtk3-ubuntu-devel

%description
Ayatana Scrollbars use an overlay to ensure that scrollbars take up no active
screen real-estate. A thumb appears magically when the pointer is in proximity
to the scrollbar, for easy desktop-style paging and dragging.


%package -n overlay-scrollbar
Summary:	Overlayed scrollbar widget for GTK

Requires:	overlay-scrollbar-gtk2 = %{version}-%{release}
Requires:	overlay-scrollbar-gtk3 = %{version}-%{release}
Requires:	xorg-x11-xinit

BuildArch:	noarch

%description -n overlay-scrollbar
Ayatana Scrollbars use an overlay to ensure that scrollbars take up no active
screen real-estate. A thumb appears magically when the pointer is in proximity
to the scrollbar, for easy desktop-style paging and dragging.


%package -n overlay-scrollbar-gtk2
Summary:	GTK 2 overlayed scrollbar widget
Group:		System Environment/Libraries

Requires:	gtk2-ubuntu

Obsoletes:	overlay-scrollbar-gtk2-devel

%description -n overlay-scrollbar-gtk2
This package contains a GTK 2 widget allowing for a overlayed scrollbar.


%package -n overlay-scrollbar-gtk3
Summary:	GTK 3 overlayed scrollbar widget
Group:		System Environment/Libraries

Requires:	gtk3-ubuntu

Obsoletes:	overlay-scrollbar-gtk3-devel

%description -n overlay-scrollbar-gtk3
This package contains a GTK 3 widget allowing for a overlayed scrollbar.


%prep
%setup -q -n overlay-scrollbar-%{version}+r%{_bzr_rev}

autoreconf -vfi


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

# Put X11 startup script in correct directory
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xsession.d/81overlay-scrollbar \
  $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/


%postun -n overlay-scrollbar
if [ $1 -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n overlay-scrollbar
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -n overlay-scrollbar
%doc AUTHORS NEWS
%{_sysconfdir}/X11/xinit/xinitrc.d/81overlay-scrollbar
%{_datadir}/glib-2.0/schemas/com.canonical.desktop.interface.enums.xml
%{_datadir}/glib-2.0/schemas/com.canonical.desktop.interface.gschema.xml


%files -n overlay-scrollbar-gtk2
%doc AUTHORS NEWS
%{_libdir}/gtk-2.0/modules/liboverlay-scrollbar.so


%files -n overlay-scrollbar-gtk3
%doc AUTHORS NEWS
%{_libdir}/gtk-3.0/modules/liboverlay-scrollbar.so


%changelog
* Fri Aug 24 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.16-1.bzr353.0ubuntu2
- Version 0.2.16
- BZR revision 353
- Ubuntu release 0ubuntu2

* Sat Jul 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.2.16-1
- Initial release
- Version 0.2.16
