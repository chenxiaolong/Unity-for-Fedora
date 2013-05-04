# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130419

Name:		indicator-power
Version:	12.10.6daily13.03.07
Release:	1%{?dist}
Summary:	Indicator to show the battery status

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-power
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-power_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-power.tar.gz

Patch0:		0001_Disable_-Werror.patch
Patch1:		revert_r161.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	gnome-settings-daemon-devel
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(upower-glib)

# From Ubuntu packaging
Requires:	control-center
Requires:	gnome-settings-daemon
# gnome-power-statistics needed
Requires:	gnome-power-manager

%description
This package contains an indicator to show the battery status. It replaces the
gnome-power-manager icon in desktop environments where regular tray icons are
hidden.


%prep
%setup -q

%patch0 -p1
%patch1 -p0

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
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang indicator-power


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f indicator-power.lang
%doc NEWS
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libpower.so
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.power.gschema.xml


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily13.03.07-1
- Version 12.10.6daily13.03.07

* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily13.01.25-1
- Version 12.10.6daily13.01.25

* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily12.11.21.1-1
- Version 12.10.6
- Ubuntu daily build from 2012-11-21

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.5-1
- Version 12.10.5

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2

* Thu Aug 30 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.0-1
- Initial release
- Version 2.0
