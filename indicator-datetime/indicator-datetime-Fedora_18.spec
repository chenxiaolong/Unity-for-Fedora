# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		indicator-datetime
Version:	12.10.3daily13.03.26
Release:	1%{?dist}
Summary:	Indicator for displaying the date and time

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-datetime
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-datetime_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-datetime.tar.gz

Patch1:		0001_Port_to_systemd_timedated.patch
Patch2:		0002_Remove_timezone_functionality.patch
Patch3:		0003_Link_pthread.patch
Patch4:		revert_r201.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(evolution-data-server-1.2)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(geoclue)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libgnome-control-center)
BuildRequires:	pkgconfig(libical)
BuildRequires:	pkgconfig(libido3-0.1)
BuildRequires:	pkgconfig(polkit-gobject-1)

Requires:	control-center-ubuntu

%description
This package contains an indicator for displaying the date and time in the
panel.


%prep
%setup -q

# Port to systemd's timedated
%patch1 -p1 -b .systemd

# Removes all timezone functionality from the indicator.
# - Removes indicator-datetime's own timezone settings. They do not work with
#   systemd and requires much work to be ported when GNOME's own timezone
#   settings can be used instead.
# - Removes dependencies on libtimezonemap and geoclue
# - Removes ability to disable multiple timezones
# - Removes ability to changes timezone based on physical location
%patch2 -p1 -b .timezone

# Tests need to link against pthread
%patch3 -p1 -b .pthread

%patch4 -p0

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
%configure --disable-static
make -j1


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate \
 $RPM_BUILD_ROOT%{_datadir}/applications/indicator-datetime-preferences.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang %{name}


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libdir}/control-center-1/panels/libindicator-datetime.so
%{_libdir}/indicators3/7/libdatetime.so
%{_libexecdir}/indicator-datetime-service
%{_datadir}/applications/indicator-datetime-preferences.desktop
%{_datadir}/dbus-1/services/indicator-datetime.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.datetime.gschema.xml
%dir %{_datadir}/indicator-datetime/
%{_datadir}/indicator-datetime/datetime-dialog.ui


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3daily13.03.26-1
- Version 12.10.3daily13.03.26

* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3daily13.01.25-1
- Version 12.10.3daily13.01.25

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2
- Add patches:
  - 0001_Port_to_systemd_timedated.patch
    - Read timezone from the timedated daemon
  - 0002_Remove_timezone_functionality.patch
    - Remove any timezone related features as they don't work with
      systemd's timedated

* Tue Oct 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-2
- Add patch to get timezone from systemd's timedated daemon

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: deprecated
- Add patch: Revert evolution-data-server 3.6 API

* Mon Jul 16 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-2
- Read timezone from /etc/sysconfig/clock

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.94-1
- Initial release
- Version 0.3.94
