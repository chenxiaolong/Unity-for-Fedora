# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Why are there three names?
# - gnome-control-center-signon (Ubuntu's packaging)
# - credentials-control-center (Source tarball)
# - online-accounts-gnome-control-center (Website)

# We'll use the same package names as Ubuntu (gnome-control-center-signon)

Name:		gnome-control-center-signon
Version:	0.1.2bzr12.12.05
Release:	1%{?dist}
Summary:	GNOME Control Center extension for single signon

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/online-accounts-gnome-control-center
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/gnome-control-center-signon_%{version}.orig.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools
BuildRequires:	yelp-tools

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(libgnome-control-center)
BuildRequires:	pkgconfig(libsignon-glib)
BuildRequires:	pkgconfig(signond)

%description
This package contains a GNOME Control Center extension for Single Sign On.


%package -n libaccount-plugin
Summary:	GNOME Control Center Library for libaccounts-glib
Group:		System Environment/Libraries
License:	LGPLv3

%description -n libaccount-plugin
This package contains the GNOME Control Center Library for libaccounts-glib.


%package -n libaccount-plugin-devel
Summary:	Development files for libaccount-plugin
Group:		Development/Libraries
License:	LGPLv3

Requires:	libaccount-plugin%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(gtk+-3.0)
Requires:	pkgconfig(libsignon-glib)

%description -n libaccount-plugin-devel
This package contains the development files for the account-plugin library.


%package -n libaccount-plugin-docs
Summary:	Documentation for libaccount-plugin
Group:		Documentation

BuildArch:	noarch

%description -n libaccount-plugin-docs
This package contains the documentation for the account-plugin library.


%prep
%setup -q

aclocal -I m4 --install --force
gtkdocize
autoreconf -vfi
intltoolize -f


%build
%configure --enable-gtk-doc
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Validate desktop files
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/gnome-credentials-panel.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/update-accounts.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang web-credentials --with-gnome --without-mo


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%post -n libaccount-plugin -p /sbin/ldconfig

%postun -n libaccount-plugin -p /sbin/ldconfig


%files -f web-credentials.lang
%doc AUTHORS
%{_libdir}/control-center-1/panels/libcredentials.so
%{_libexecdir}/update-accounts
%{_datadir}/applications/gnome-credentials-panel.desktop
%{_datadir}/applications/update-accounts.desktop
%{_datadir}/dbus-1/services/com.canonical.webcredentials.capture.service
%{_datadir}/icons/hicolor/*/apps/*.png


%files -n libaccount-plugin
%{_libdir}/libaccount-plugin-1.0.so.*
%{_libdir}/girepository-1.0/AccountPlugin-1.0.typelib


%files -n libaccount-plugin-devel
%dir %{_includedir}/libaccount-plugin/
%{_includedir}/libaccount-plugin/*.h
%{_libdir}/libaccount-plugin-1.0.so
%{_libdir}/pkgconfig/account-plugin.pc
%{_datadir}/gir-1.0/AccountPlugin-1.0.gir
%{_datadir}/vala/vapi/AccountPlugin.vapi


%files -n libaccount-plugin-docs
%doc %{_datadir}/gtk-doc/html/account-plugin/


%changelog
* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.2bzr12.12.05-1
- Version 0.1.2bzr12.12.05

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.1-1
- Version 0.1.1

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.18-1
- Version 0.0.18

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.17-1
- Version 0.0.17

* Fri Sep 14 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.15-1
- Version 0.0.15

* Tue Sep 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.0.13-1
- Initial release
- Version 0.0.13
