# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		unity-lens-video
Version:	0.3.14daily13.04.15
Release:	1%{?dist}
Summary:	Unity video lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-videos
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity-lens-video_%{version}.orig.tar.gz
Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-unity-lens-video.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-common
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(zeitgeist-1.0)

# CheckRequires
BuildRequires:	xorg-x11-server-Xvfb

Requires:	unity-lens-music
Requires:	gvfs


%description
This package contains the video lens which can be used for searching videos in
the dash of the Unity shell.


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
%configure --enable-headless-tests


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT

#sed -i \
#  -e '/Encoding/d' \
#  -e '/Categories/ s/$/;/' \
#  $RPM_BUILD_ROOT%{_datadir}/applications/unity-lens-video.desktop
#desktop-file-validate \
#  $RPM_BUILD_ROOT%{_datadir}/applications/unity-lens-video.desktop

%find_lang unity-lens-video


%files -f unity-lens-video.lang
%doc COPYING
%{_libexecdir}/unity-lens-video/
%{_datadir}/dbus-1/services/unity-lens-video.service
%{_datadir}/dbus-1/services/unity-scope-video-remote.service
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%{_datadir}/unity/lenses/video/


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.14daily13.04.15-1
- Version 0.3.14daily13.04.15

* Fri Feb 01 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.14daily12.12.05-1
- Version 0.3.14daily12.12.05

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.14-1
- Version 0.3.14

* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.12-1
- Version 0.3.12

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.10-1
- Version 0.3.10

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.9-1
- Version 0.3.9

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-3
- Fix directory ownership

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-2
- Video lens didn't get installed
- Install daemon to libexec

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.6-1
- Initial release
- Version 0.3.6
