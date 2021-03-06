# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		unity-lens-music
Version:	6.8.1daily13.04.18~13.04
Release:	1%{?dist}
Summary:	Unity music lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-music
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity-lens-music_%{version}.orig.tar.gz
Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-unity-lens-music.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(oauth)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(unity)

%description
This package contains the music lens which can be used to browse media files.


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

%find_lang unity-lens-music


%files -f unity-lens-music.lang
%doc AUTHORS
%dir %{_libexecdir}/unity-lens-music/
%{_libexecdir}/unity-lens-music/music-preview-player
%{_libexecdir}/unity-lens-music/unity-music-daemon
%{_libexecdir}/unity-lens-music/unity-musicstore-daemon
%{_datadir}/dbus-1/services/music-preview-player.service
%{_datadir}/dbus-1/services/musicstore-scope.service
%{_datadir}/dbus-1/services/unity-lens-music.service
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/music/
%{_datadir}/unity/lenses/music/music.lens
%{_datadir}/unity/lenses/music/musicstore.scope


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.1daily13.04.18~13.04-1
- Version 6.8.1daily13.04.18~13.04

* Fri Feb 01 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.1daily13.01.11-1
- Version 6.8.1daily13.01.11
- Build dep on GStreamer 1.0

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.1-1
- Version 6.8.1

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.8.0-1
- Version 6.8.0

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.6.0-1
- Version 6.6.0

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1
- Version 6.2.0

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.0.0-1
- Version 6.0.0

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.12.0-1
- Initial release
- Version 5.12.0
