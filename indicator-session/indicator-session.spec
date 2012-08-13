# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-session
Version:	12.10.0
Release:	1%{?dist}
Summary:	Indicator for session management and status information

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-session
Source0:	https://launchpad.net/indicator-session/12.10/%{version}/+download/indicator-session-%{version}.tar.gz

Patch0:		0001_Revert_new_glib_stuff.patch

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

%description
Quick! Change your status. Switch users. Close your session. All provided by the
The Session Menu these tasks are conveniently placed in the upper-right corner
of the desktop to make them available and easy to use.


%prep
%setup -q

%patch0 -p1 -b .newglibstuff


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang %{name}


%postun
if [ ${1} -eq 0 ]; then
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


%changelog
* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: deprecated

* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-2
- Use gpk-update-viewer to show updates

* Sat Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.96-1
- Initial release
- Version 0.3.96
