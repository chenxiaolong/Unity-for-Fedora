# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _translations 20130418

%define _ubuntu_rel 0ubuntu3

Name:		indicator-printers
Version:	0.1.6
Release:	2.%{_ubuntu_rel}%{?dist}
Summary:	Indicator showing active print jobs

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/indicator-printers
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-printers_%{version}.orig.tar.gz

Source98:	https://dl.dropboxusercontent.com/u/486665/Translations/translations-%{_translations}-indicator-printers.tar.gz
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/indicator-printers_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool

BuildRequires:	cups-devel

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(indicator3-0.4)

%description
This package contains an indicator that shows active print jobs in the panel.


%prep
%setup -q

# Apply Ubuntu's patches
cp src/indicator-printers-service.c{,.orig}
zcat '%{SOURCE99}' | patch -Np1
cp src/indicator-printers-service.c{.orig,}

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

pushd debian/local/
find . -type f -exec install -Dm644 {} $RPM_BUILD_ROOT%{_datadir}/icons/{} \;
popd

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang indicator-printers


%files -f indicator-printers.lang
%doc AUTHORS
%dir %{_libdir}/indicators3/
%dir %{_libdir}/indicators3/7/
%{_libdir}/indicators3/7/libprintersmenu.so
%{_libexecdir}/indicator-printers-service
%{_datadir}/dbus-1/services/indicator-printers.service
%{_datadir}/icons/ubuntu-mono-dark/
%{_datadir}/icons/ubuntu-mono-light/


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.6-2.0ubuntu3
- Add translations

* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.1.6-1.0ubuntu3
- Initial release
- Version 0.1.6
- Ubuntu release 0ubuntu3
