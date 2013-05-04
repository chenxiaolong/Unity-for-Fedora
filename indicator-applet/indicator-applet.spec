# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		indicator-applet
Version:	12.10.2daily13.03.01
Release:	1%{?dist}
Summary:	Small applet for GNOME panel to display appindicators

Group:		User Interface/Desktops
License:	GPLv3 and LGPLv2 and LGPLv3
URL:		https://launchpad.net/indicator-applet
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-applet_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-applet.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	hicolor-icon-theme
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libpanelapplet-4.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(x11)

%description
This package contains an applet for the GNOME panel to display Ayatana
appindicators.


%prep
%setup -q

mkdir po_new
tar zxvf '%{SOURCE98}' -C po_new
rm -f po/LINGUAS po/*.pot
mv po_new/po/*.pot po/
for i in po_new/po/*.po; do
  FILE=$(sed -n "s|.*/%{name}-||p" <<< ${i})
  mv ${i} po/${FILE}
  echo ${FILE%.*} >> po/LINGUAS
done

autoreconf -vfi
intltoolize -f


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
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2daily13.03.01-1
- Version 12.10.2daily13.03.01

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.5.0-1
- Initial release
- Version 0.5.0
