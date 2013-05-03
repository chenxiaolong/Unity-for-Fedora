# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130419

Name:		indicator-messages
Version:	12.10.6daily13.04.09
Release:	1%{?dist}
Summary:	Indicator for collecting messages that need a response

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-messages
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-messages_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-messages.tar.gz

Patch0:		revert_r335.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
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


%prep
%setup -q

%patch0 -p0

mkdir po_new
tar zxvf '%{SOURCE98}' -C po_new
rm -f po/LINGUAS po/*.pot
mv po_new/po/*.pot po/
for i in po_new/po/*.po; do
  FILE=$(sed -n "s|.*/%{name}-||p" <<< ${i})
  mv ${i} po/${FILE}
  echo ${FILE%.*} >> po/LINGUAS
done

gtkdocize
autoreconf -vfi
intltoolize


%build
%configure --disable-static --enable-gtk-doc
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang indicator-messages


%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
/sbin/ldconfig
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files -f indicator-messages.lang
%doc AUTHORS ChangeLog
%{_libdir}/girepository-1.0/MessagingMenu-1.0.typelib
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libmessaging.so
%{_libdir}/libmessaging-menu.so.0
%{_libdir}/libmessaging-menu.so.0.0.0
%{_libexecdir}/indicator-messages-service
%{_datadir}/dbus-1/services/indicator-messages.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.messages.gschema.xml
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg


%files devel
%doc AUTHORS ChangeLog
%doc %{_datadir}/gtk-doc/html/messaging-menu/
%dir %{_includedir}/messaging-menu/
%{_includedir}/messaging-menu/messaging-menu.h
%{_libdir}/libmessaging-menu.so
%{_libdir}/pkgconfig/messaging-menu.pc
%{_datadir}/gir-1.0/MessagingMenu-1.0.gir


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily13.04.09-1
- Version 12.10.6daily13.04.09
- Add translations

* Sun Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily13.01.25-1
- Version 12.10.6daily13.01.25

* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.6daily12.11.22-1
- Version 12.10.6
- Ubuntu daily build from 2012-11-22

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.5-1
- Version 12.10.5

* Tue Oct 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.4-1
- Version 12.10.4

* Fri Sep 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3-1
- Version 12.10.3
- Drop GTK 2 subpackage

* Mon Aug 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Sat Jul 07 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.6.0-1
- Initial release
- Version 0.6.0
