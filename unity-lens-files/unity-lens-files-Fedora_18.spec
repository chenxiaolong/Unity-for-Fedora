# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

Name:		unity-lens-files
Version:	7.0~daily13.04.15
Release:	1%{?dist}
Summary:	Unity files lens

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-files
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/unity-lens-files_%{version}.orig.tar.gz
Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-unity-lens-files.tar.gz

Patch0:		0001_unity-protocol-private.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	pkgconfig
BuildRequires:	vala-tools

BuildRequires:	pkgconfig(dee-1.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gee-1.0)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(unity-protocol-private)
BuildRequires:	pkgconfig(zeitgeist-1.0)

%description
This package contains the files lens which can be used to browse recent
documents and other files.


%prep
%setup -q

%patch0 -p1 -b unity-protocol-private

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


%postun
if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%dir %{_libexecdir}/unity-lens-files/
%{_libexecdir}/unity-lens-files/unity-files-daemon
%{_datadir}/dbus-1/services/unity-lens-files.service
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.FilesLens.gschema.xml
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/files/
%dir %{_datadir}/unity/themes/
%{_datadir}/unity/lenses/files/files.lens
%{_datadir}/unity/themes/files.png


%changelog
* Sat May 04 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 7.0~daily13.04.15-1
- Version 7.0~daily13.04.15

* Fri Feb 01 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.6.0daily12.12.05-1
- Version 6.6.0daily12.12.05

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.6.0-1
- Version 6.6.0

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.4.0-1
- Version 6.4.0

* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-2
- Fix directory ownership
- Use pkgconfig for dependencies

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 6.2.0-1
- Version 6.2.0

* Fri Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 5.10.0-1
- Initial release
- Version 5.10.0
