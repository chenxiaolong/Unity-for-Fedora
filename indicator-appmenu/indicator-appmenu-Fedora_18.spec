# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		indicator-appmenu
Version:	13.01.0daily13.03.28
Release:	1%{?dist}
Summary:	Indicator to host the menus from an application

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-appmenu
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-appmenu_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-appmenu.tar.gz

Patch0:		0001_Fix_dbusmenu-dumper_path.patch
Patch1:		revert_r229.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(dbusmenu-jsonloader-0.4)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libbamf3)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sqlite3)

BuildRequires:	readline-devel

%description
This package contains an indicator to host the menus from an application.


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

gtkdocize
autoreconf -vfi
intltoolize -f


%build
CFLAGS="$RPM_OPT_FLAGS"

# Disable -Werror
CFLAGS="${CFLAGS} -Wno-error"

# Cannot find gio/gdesktopappinfo.h
CFLAGS="${CFLAGS} $(pkg-config --cflags --libs gio-unix-2.0)"

%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang %{name}


%postun
if [ ${1} -eq 0 ] ; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libappmenu.so
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.appmenu.gschema.xml


%files tools
%doc AUTHORS ChangeLog
%{_libexecdir}/current-menu
%{_libexecdir}/current-menu-dump
%{_libexecdir}/menu-pusher
%{_libexecdir}/mock-json-app


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 13.01.0daily13.03.28-1
- Version 13.01.0daily13.03.28

* Mon Jan 28 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.4daily13.01.25-1
- Version 12.10.4daily13.01.25

* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.4daily12.11.23-1
- Version 12.10.4
- Ubuntu daily build from 2012-11-23

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3-1.0ubuntu2
- Version 12.10.3
- Ubuntu release 0ubuntu2

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.3-1
- Version 12.10.3

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0
- Drop GTK 2 subpackage: no longer maintained upstream

* Wed Jul 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.97-1
- Initial release
- Version 0.3.97
