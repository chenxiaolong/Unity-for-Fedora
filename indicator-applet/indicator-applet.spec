# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		indicator-applet
Version:	0.5.0
Release:	1%{?dist}
Summary:	Small applet for GNOME panel to display appindicators

Group:		User Interface/Desktops
License:	GPLv3 and LGPLv2 and LGPLv3
URL:		https://launchpad.net/indicator-applet
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-applet_%{version}.orig.tar.gz

BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	hicolor-icon-theme
BuildRequires:	intltool
BuildRequires:	libtool

BuildRequires:	gnome-panel-devel
BuildRequires:	gtk3-devel
BuildRequires:	libindicator-gtk3-devel
BuildRequires:	libX11-devel
BuildRequires:	libxml2-devel

%description
This package contains an applet for the GNOME panel to display Ayatana
appindicators.


%prep
%setup -q

# Build fix with newer GLib versions
sed -i '/#include <glib\/gtypes\.h>/d' src/tomboykeybinder.h


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libexecdir}/indicator-applet
%{_libexecdir}/indicator-applet-appmenu
%{_libexecdir}/indicator-applet-complete
%{_libexecdir}/indicator-applet-session
%{_datadir}/dbus-1/services/org.gnome.panel.applet.FastUserSwitchAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.IndicatorAppletAppmenuFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.IndicatorAppletCompleteFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.IndicatorAppletFactory.service
%{_datadir}/gnome-panel/4.0/applets/org.ayatana.panel.FastUserSwitchApplet.panel-applet
%{_datadir}/gnome-panel/4.0/applets/org.ayatana.panel.IndicatorApplet.panel-applet
%{_datadir}/gnome-panel/4.0/applets/org.ayatana.panel.IndicatorAppletAppmenu.panel-applet
%{_datadir}/gnome-panel/4.0/applets/org.ayatana.panel.IndicatorAppletComplete.panel-applet
%{_datadir}/icons/hicolor/scalable/apps/indicator-applet.svg


%changelog
* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
