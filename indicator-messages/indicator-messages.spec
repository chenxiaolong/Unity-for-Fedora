# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-messages
Version:	0.6.0
Release:	1%{?dist}
Summary:	Indicator for collecting messages that need a response

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-messages
Source0:	https://launchpad.net/indicator-messages/0.6/%{version}/+download/indicator-messages-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme

BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libindicate-devel
BuildRequires:	libindicate-gtk2-devel
BuildRequires:	libindicate-gtk3-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	telepathy-glib-devel

# OBS dependency solver fix: dependencies use gtk3-ubuntu, so don't install gtk3
#!BuildIgnore:  gtk3
#!BuildIgnore:  gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
A place on the user's desktop that collects messages that need a response. This
menu provides a condensed and collected view of all of those messages for quick
access, but without making them annoying in times that you want to ignore them.


%package devel
Summary:	Development files for indicator-messages
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files needed for creating status providers
for the messages indicator.


%package gtk2
Summary:	Indicator for collecting messages that need a response - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This package contains the GTK 2 version of the messages indicator.


%prep
%setup -q


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk=2 --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk=3 --disable-static

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog
%{_libdir}/indicators3/7/libmessaging.so
%{_libdir}/libindicator-messages-service.so.0
%{_libdir}/libindicator-messages-service.so.0.0.0
%{_libdir}/libindicator-messages-status-provider.so.1
%{_libdir}/libindicator-messages-status-provider.so.1.0.0
%{_libexecdir}/indicator-messages-service
%{_libexecdir}/status-providers/1/libemesene.so
%{_libexecdir}/status-providers/1/libmc5.so
%{_libexecdir}/status-providers/1/libpidgin.so
%{_libexecdir}/status-providers/1/libtelepathy.so
%{_datadir}/dbus-1/services/indicator-messages.service
%{_datadir}/libindicator/icons/hicolor/16x16/categories/applications-chat-panel.png
%{_datadir}/libindicator/icons/hicolor/16x16/categories/applications-email-panel.png
%{_datadir}/libindicator/icons/hicolor/16x16/categories/applications-microblogging-panel.png
%{_datadir}/libindicator/icons/hicolor/16x16/status/application-running.png
%{_datadir}/libindicator/icons/hicolor/16x16/status/indicator-messages-new.png
%{_datadir}/libindicator/icons/hicolor/16x16/status/indicator-messages.png
%{_datadir}/libindicator/icons/hicolor/22x22/categories/applications-email-panel.png
%{_datadir}/libindicator/icons/hicolor/22x22/status/indicator-messages-new.png
%{_datadir}/libindicator/icons/hicolor/22x22/status/indicator-messages.png
%{_datadir}/libindicator/icons/hicolor/24x24/status/application-running.png
%{_datadir}/libindicator/icons/hicolor/24x24/status/indicator-messages-new.png
%{_datadir}/libindicator/icons/hicolor/24x24/status/indicator-messages.png
%{_datadir}/libindicator/icons/hicolor/32x32/categories/applications-chat-panel.png
%{_datadir}/libindicator/icons/hicolor/32x32/categories/applications-email-panel.png
%{_datadir}/libindicator/icons/hicolor/32x32/status/application-running.png
%{_datadir}/libindicator/icons/hicolor/32x32/status/indicator-messages-new.png
%{_datadir}/libindicator/icons/hicolor/32x32/status/indicator-messages.png
%{_datadir}/libindicator/icons/hicolor/48x48/status/application-running.png
%{_datadir}/libindicator/icons/hicolor/48x48/status/indicator-messages-new.png
%{_datadir}/libindicator/icons/hicolor/48x48/status/indicator-messages.png
%{_datadir}/libindicator/icons/hicolor/scalable/categories/applications-chat-panel.svg
%{_datadir}/libindicator/icons/hicolor/scalable/categories/applications-email-panel.svg
%{_datadir}/libindicator/icons/hicolor/scalable/status/application-running.svg
%{_datadir}/libindicator/icons/hicolor/scalable/status/indicator-messages-new.svg
%{_datadir}/libindicator/icons/hicolor/scalable/status/indicator-messages.svg


%files devel
%doc AUTHORS ChangeLog
%{_includedir}/libindicator-messages-service/app-menu-item.h
%{_includedir}/libindicator-messages-service/dbus-data.h
%{_includedir}/libindicator-messages-service/default-applications.h
%{_includedir}/libindicator-messages-service/dirs.h
%{_includedir}/libindicator-messages-service/gen-messages-service.xml.h
%{_includedir}/libindicator-messages-service/im-menu-item.h
%{_includedir}/libindicator-messages-service/launcher-menu-item.h
%{_includedir}/libindicator-messages-service/messages-service-dbus.h
%{_includedir}/libindicator-messages-service/seen-db.h
%{_includedir}/libindicator-messages-service/status-items.h
%{_includedir}/libindicator-messages-status-provider-1/status-provider.h
%{_libdir}/libindicator-messages-service.so
%{_libdir}/libindicator-messages-status-provider.so
%{_libdir}/pkgconfig/indicator-messages-status-provider-0.5.pc


%files gtk2
%doc AUTHORS ChangeLog
%{_libdir}/indicators/7/libmessaging.so


%changelog
* Sat Jul 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.0-1
- Initial release
- Version 0.6.0
