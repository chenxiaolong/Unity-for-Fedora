# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		appmenu-gtk
Version:	12.10.2
Release:	1%{?dist}
Summary:	Application menu module for GTK+

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/appmenu-gtk
Source0:	https://launchpad.net/appmenu-gtk/12.10/%{version}/+download/appmenu-gtk-%{version}.tar.gz

# Require Ubuntu's version of GTK 2 and GTK 3
BuildRequires:	gtk2-ubuntu-devel
BuildRequires:	gtk3-ubuntu-devel

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(x11)

%description
(This package contains no files)


%package -n appmenu-gtk2
Summary:	Application menu module for GTK+ - GTK 2 version

%description -n appmenu-gtk2
This package provides a GTK 2 module to export GTK menus over DBus.


%package -n appmenu-gtk3
Summary:	Application menu module for GTK+ - GTK 3 version

%description -n appmenu-gtk3
This package provides a GTK 3 module to export GTK menus over DBus.


%prep
%setup -q

# Fix script-without-shebang rpmlint error
sed -i '1 i #!/bin/bash' 80appmenu.in


%build
%global _configure ../configure
mkdir build-gtk2 build-gtk3

pushd build-gtk2
%configure --with-gtk2 --disable-static
make %{?_smp_mflags}
popd

pushd build-gtk3
%configure --with-gtk3 --disable-static
make %{?_smp_mflags}
popd


%install
pushd build-gtk2
make install DESTDIR=$RPM_BUILD_ROOT
popd

pushd build-gtk3
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Put xinit files in correct directory
install -dm755 \
   $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xsession.d/80appmenu \
   $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu.%{_lib}
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xsession.d/80appmenu-gtk3 \
   $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu-gtk3.%{_lib}
chmod 755 \
   $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu{,-gtk3}.%{_lib}

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%files -n appmenu-gtk2
%doc AUTHORS README
%{_libdir}/gtk-2.0/2.10.0/menuproxies/libappmenu.so
%{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu.%{_lib}


%files -n appmenu-gtk3
%doc AUTHORS README
%{_libdir}/gtk-3.0/3.0.0/menuproxies/libappmenu.so
%{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu-gtk3.%{_lib}


%changelog
* Sat Oct 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.2-1
- Version 12.10.2

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.1-1
- Version 12.10.1

* Mon Aug 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 12.10.0-1
- Version 12.10.0

* Sat Aug 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.92-2
- Remove config macro on X11 startup scripts
- Use pkgconfig for dependencies
- Fix rpmlint script-without-shebang error
- Remove useless autoreconf line

* Thu Jun 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.92-1
- Initial release
- Version 0.3.92
