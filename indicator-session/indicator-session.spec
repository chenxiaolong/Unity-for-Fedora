# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-session
Version:	0.3.96
Release:	2%{?dist}
Summary:	Indicator for session management and status information

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-session
Source0:	https://launchpad.net/indicator-session/0.4/%{version}/+download/indicator-session-%{version}.tar.gz

# Use gnome-packagekit instead of Ubuntu's update-manager
Patch0:		0001_Use_gnome-packagekit.patch

BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool

BuildRequires:	dbus-glib-devel
BuildRequires:	GConf2-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtk3-devel
BuildRequires:	libgudev1-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel
BuildRequires:	libindicator-devel
BuildRequires:	libindicator-gtk3-devel
#BuildRequires:	PackageKit-backend-devel
BuildRequires:	PackageKit-glib-devel
BuildRequires:	polkit-devel

Requires:	gnome-packagekit

# From Ubuntu packaging
Requires:	gnome-settings-daemon
Requires:	upower

# Satisfy OBS conflict on what provides PackageKit-backend
BuildRequires:	PackageKit-yum

# OBS dependency solver fix: dependencies use gtk3-ubuntu, so don't install gtk3
#!BuildIgnore:  gtk3
#!BuildIgnore:  gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

# Satisfy OBS conflict on libXfixes
BuildRequires:	libXfixes
BuildRequires:	libXfixes-devel

%description
Quick! Change your status. Switch users. Close your session. All provided by the
The Session Menu these tasks are conveniently placed in the upper-right corner
of the desktop to make them available and easy to use.


%package gtk2
Summary:	Indicator for session management and status information - GTK 2
Group:		User Interface/Desktops

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk2
This package contains the GTK 2 version of the session indicator.


%prep
%setup -q

%patch0 -p1 -b .packagekit


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

%find_lang %{name}


%postun
if [ ${1} -eq 0; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libdir}/indicators3/7/libsession.so
%{_libexecdir}/gtk-logout-helper
%{_libexecdir}/indicator-session-service
%{_datadir}/GConf/gsettings/indicator-session.convert
%{_datadir}/dbus-1/services/indicator-session.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.session.gschema.xml
%{_datadir}/indicators/session/applications/classic-desktop.desktop
%{_datadir}/indicators/session/applications/classic-desktop.sh
%{_datadir}/libindicator/icons/hicolor/16x16/actions/system-log-out.png
%{_datadir}/libindicator/icons/hicolor/16x16/actions/system-restart.png
%{_datadir}/libindicator/icons/hicolor/16x16/actions/system-shutdown-panel.png
%{_datadir}/libindicator/icons/hicolor/16x16/actions/system-shutdown.png
%{_datadir}/libindicator/icons/hicolor/16x16/status/account-logged-in.png
%{_datadir}/libindicator/icons/hicolor/22x22/actions/system-log-out.png
%{_datadir}/libindicator/icons/hicolor/22x22/actions/system-restart.png
%{_datadir}/libindicator/icons/hicolor/22x22/actions/system-shutdown-panel.png
%{_datadir}/libindicator/icons/hicolor/22x22/actions/system-shutdown.png
%{_datadir}/libindicator/icons/hicolor/22x22/status/account-logged-in.png
%{_datadir}/libindicator/icons/hicolor/24x24/actions/system-log-out.png
%{_datadir}/libindicator/icons/hicolor/24x24/actions/system-restart.png
%{_datadir}/libindicator/icons/hicolor/24x24/actions/system-shutdown-panel.png
%{_datadir}/libindicator/icons/hicolor/24x24/actions/system-shutdown.png
%{_datadir}/libindicator/icons/hicolor/24x24/status/account-logged-in.png
%{_datadir}/libindicator/icons/hicolor/32x32/actions/system-log-out.png
%{_datadir}/libindicator/icons/hicolor/32x32/actions/system-restart.png
%{_datadir}/libindicator/icons/hicolor/32x32/status/account-logged-in.png
%{_datadir}/libindicator/icons/hicolor/scalable/actions/system-log-out.svg
%{_datadir}/libindicator/icons/hicolor/scalable/actions/system-restart.svg
%{_datadir}/libindicator/icons/hicolor/scalable/actions/system-shutdown-panel.svg
%{_datadir}/libindicator/icons/hicolor/scalable/actions/system-shutdown.svg
%{_datadir}/libindicator/icons/hicolor/scalable/status/account-logged-in.svg


%files gtk2
%doc AUTHORS ChangeLog
%{_libdir}/indicators/7/libsession.so


%changelog
* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-2
- Use gpk-update-viewer to show updates

* Sat Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-1
- Initial release
- Version 0.3.96
