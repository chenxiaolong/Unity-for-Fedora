# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		unity-lens-applications
Version:	6.10.0daily13.04.18~13.04
Release:	1%{?dist}
Summary:	Unity Applications Lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-applications
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity-lens-applications_%{version}.orig.tar.gz
Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-unity-lens-applications.tar.gz

Patch0:		10-no-db51.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcolumbus0)
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(unity-protocol-private)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zeitgeist-1.0)

BuildRequires:	libdb-devel
BuildRequires:	xapian-core-devel

%description
This package contains the applications lens which can be used to launch
applications for the Unity shell.


%prep
%setup -q

%patch0 -p1 -b .dbversion

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

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}


%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%config %{_sysconfdir}/xdg/menus/unity-lens-applications.menu
%dir %{_libexecdir}/unity-lens-applications/
%{_libexecdir}/unity-lens-applications/unity-applications-daemon
%{_datadir}/dbus-1/services/unity-lens-applications.service
%{_datadir}/desktop-directories/X-Unity-All-Applications.directory
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.AppsLens.gschema.xml
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/applications/
%dir %{_datadir}/unity/lenses/commands/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/lenses/applications/applications.lens
%{_datadir}/unity/lenses/commands/commands.lens
%{_datadir}/unity/themes/applications.png


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.10.0daily13.04.18~13.04-1
- Version 6.10.0daily13.04.18~13.04

* Fri Feb 01 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.10.0daily12.12.05-1
- Version 6.10.0daily12.12.05
- Build dep on pkgconfig(libgnome-menu-3.0)

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.10.0-1
- Version 6.10.0

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.0-1
- Version 6.8.0

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.6.0-1
- Version 6.6.0

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-1
- Version 6.4.0

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-2
- Fix directory ownership
- Use pkgconfig for dependencies
- Remove unneeded build dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1
- Version 6.2.0

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1
- Initial release
- Version 5.12.0
