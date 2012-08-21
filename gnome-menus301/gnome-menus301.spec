# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Required for unity-lens-applications

# Partially based off of Fedora 15's spec file

Name:		gnome-menus301
Version:	3.0.1
Release:	1%{?dist}
Summary:	A menu system for the GNOME project

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/gnome-menus/3.0/gnome-menus-%{version}.tar.bz2

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(gamin)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(python2)

Requires:	redhat-menus

%description
gnome-menus is an implementation of the draft "Desktop Menu Specification" from
freedesktop.org. This package also contains the GNOME menu layout configuration
files, .directory files and assorted menu related utility programs, Python
bindings, and a simple menu editor.


%package devel
Summary:	Development files for gnome-menus301
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the gnome-menus301 library.


%prep
%setup -q -n gnome-menus-%{version}


%build
%configure --disable-static --disable-introspection

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
# Install library only
make -C libmenu install DESTDIR=$RPM_BUILD_ROOT
make -C python install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Remove Python binding
rm $RPM_BUILD_ROOT%{python_sitearch}/gmenu.so


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS NEWS COPYING.LIB
%{_libdir}/libgnome-menu.so.2
%{_libdir}/libgnome-menu.so.2.4.13


%files devel
%doc AUTHORS NEWS COPYING.LIB
%dir %{_includedir}/gnome-menus/
%{_includedir}/gnome-menus/gmenu-tree.h
%{_libdir}/libgnome-menu.so
%{_libdir}/pkgconfig/libgnome-menu.pc


%changelog
* Tue Aug 21 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.1-2
- Remove useless Python binding
- Use pkgconfig for dependencies

* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.1-1
- Initial release
- Version 3.0.1
