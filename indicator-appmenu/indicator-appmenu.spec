# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-appmenu
Version:	0.3.97
Release:	1%{?dist}
Summary:	Indicator to host the menus from an application

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-appmenu
Source0:	https://launchpad.net/indicator-appmenu/0.4/%{version}/+download/indicator-appmenu-%{version}.tar.gz

Patch0:		0001_Fix_dbusmenu-dumper_path.patch

BuildRequires:	gnome-doc-utils
BuildRequires:	intltool

BuildRequires:	bamf-devel
BuildRequires:	bamf3-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libappindicator-gtk3-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libdbusmenu-jsonloader-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	sqlite-devel
BuildRequires:	vala-tools

# OBS dependency solver fix: dependencies use gtk3-ubuntu, so don't install gtk3
#!BuildIgnore:	gtk3
#!BuildIgnore:	gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
This package contains an indicator to host the menus from an application.


%package gtk2
Summary:	Indicator to host the menus from an application - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This packages contains the GTK 2 version of the appmenu indicator.


%package tools
Summary: 	Indicator to host the menus from an application - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libdbusmenu-tools

%description tools
This package contains debugging tools for the appmenu indicator.


%prep
%setup -q

%patch0 -p1 -b .dbusmenu-dumper


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

CFLAGS="$RPM_OPT_FLAGS"

# Disable -Werror
CFLAGS="${CFLAGS} -Wno-error"

# Cannot find gio/gdesktopappinfo.h
CFLAGS="${CFLAGS} $(pkg-config --cflags --libs gio-unix-2.0)"

pushd build-gtk2
%configure --with-gtk=2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%postun
if [ ${1} -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS ChangeLog
%{_libdir}/indicators3/7/libappmenu.so
%{_libexecdir}/hud-service
%{_datadir}/dbus-1/services/com.canonical.hud.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.gschema.xml
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.hud.gschema.xml
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.hud.search.gschema.xml


%files gtk2
%doc AUTHORS ChangeLog
%{_libdir}/indicators/7/libappmenu.so


%files tools
%doc AUTHORS ChangeLog
%{_bindir}/hud-cli
%{_bindir}/hud-dump-application
%{_bindir}/hud-gtk
%{_bindir}/hud-list-applications
%{_bindir}/hud-verify-app-info
%{_libexecdir}/current-menu
%{_libexecdir}/current-menu-dump
%{_libexecdir}/menu-pusher
%{_libexecdir}/mock-json-app
%{_mandir}/man1/hud-cli.1.gz
%{_mandir}/man1/hud-dump-application.1.gz
%{_mandir}/man1/hud-list-applications.1.gz
%{_mandir}/man1/hud-verify-app-info.1.gz
%{_datadir}/hud-gtk/hud-gtk.ui


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.97-1
- Initial release
- Version 0.3.97
