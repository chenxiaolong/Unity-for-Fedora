# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-messages
Version:	0.6.0
Release:	2%{?dist}
Summary:	Indicator for collecting messages that need a response

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-messages
Source0:	https://launchpad.net/indicator-messages/0.6/%{version}/+download/indicator-messages-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(indicate-0.7)
BuildRequires:	pkgconfig(indicate-gtk-0.7)
BuildRequires:	pkgconfig(indicate-gtk3-0.7)
BuildRequires:	pkgconfig(indicator-0.4)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(telepathy-glib)

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
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libmessaging.so
%{_libdir}/libindicator-messages-service.so.*
%{_libdir}/libindicator-messages-status-provider.so.*
%{_libexecdir}/indicator-messages-service
%dir %{_libexecdir}/status-providers/
%dir %{_libexecdir}/status-providers/1/
%{_libexecdir}/status-providers/1/libemesene.so
%{_libexecdir}/status-providers/1/libmc5.so
%{_libexecdir}/status-providers/1/libpidgin.so
%{_libexecdir}/status-providers/1/libtelepathy.so
%{_datadir}/dbus-1/services/indicator-messages.service
%dir %{_datadir}/libindicator/
%{_datadir}/libindicator/icons/


%files devel
%doc AUTHORS ChangeLog
%dir %{_includedir}/libindicator-messages-service/
%dir %{_includedir}/libindicator-messages-status-provider-1/
%{_includedir}/libindicator-messages-service/*.h
%{_includedir}/libindicator-messages-status-provider-1/status-provider.h
%{_libdir}/libindicator-messages-service.so
%{_libdir}/libindicator-messages-status-provider.so
%{_libdir}/pkgconfig/indicator-messages-status-provider-0.5.pc


%files gtk2
%doc AUTHORS ChangeLog
%dir %{_libdir}/indicators/
%dir %{_libdir}/indicators/7/
%{_libdir}/indicators/7/libmessaging.so


%changelog
* Mon Aug 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Sat Jul 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.0-1
- Initial release
- Version 0.6.0
