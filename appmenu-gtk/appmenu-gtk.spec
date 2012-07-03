# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		appmenu-gtk
Version:	0.3.92
Release:	1%{?dist}
Summary:	Application menu module for GTK+

Group:		System Environment/Libraries
License:	GPLv3
URL:		https://launchpad.net/appmenu-gtk
Source0:	https://launchpad.net/appmenu-gtk/0.4/%{version}/+download/appmenu-gtk-%{version}.tar.gz

# Require Ubuntu version of GTK2 and GTK3
BuildRequires:	gtk2-devel >= 1:
BuildRequires:	gtk3-devel >= 1:

BuildRequires:	libtool
BuildRequires:	libX11-devel
BuildRequires:	libdbusmenu-glib-devel
BuildRequires:	libdbusmenu-gtk2-devel
BuildRequires:	libdbusmenu-gtk3-devel

%description
(This package contains no files)


%package -n appmenu-gtk2
Summary:	Application menu module for GTK+ - GTK2

%description -n appmenu-gtk2
This package provides a GTK2 module to export GTK menus over DBus.


%package -n appmenu-gtk3
Summary:	Application menu module for GTK+ - GTK3

%description -n appmenu-gtk3
This package provides a GTK3 module to export GTK menus over DBus.


%prep
%setup -q

autoreconf -vfi


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
rm -rf $RPM_BUILD_ROOT

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
%config(noreplace) %{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu.%{_lib}


%files -n appmenu-gtk3
%doc AUTHORS README
%{_libdir}/gtk-3.0/3.0.0/menuproxies/libappmenu.so
%config(noreplace) %{_sysconfdir}/X11/xinit/xinitrc.d/80appmenu-gtk3.%{_lib}


%changelog
* Thu Jun 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.3.92-1
- Initial release
- Version 0.3.92
