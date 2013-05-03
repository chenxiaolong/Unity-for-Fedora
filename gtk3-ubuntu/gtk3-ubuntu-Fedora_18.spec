# Based off of Fedora 18's spec
# Modifications by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu8

%global bin_version 3.0.0

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name:		gtk3
Version:	3.6.4
Release:	100.%{_ubuntu_rel}%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.gtk.org
#VCS:		git:git://git.gnome.org/gtk+
Source:		http://download.gnome.org/sources/gtk+/3.6/gtk+-%{version}.tar.xz
Source1:	fedora_im-cedilla.conf

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gtk+3.0_%{version}-%{_ubuntu_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool

BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(atk-bridge-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)

BuildRequires:	cups-devel

# required for icon theme apis to work
Requires:	hicolor-icon-theme

# We need to prereq these so we can run gtk-query-immodules-3.0
Requires(post):	atk
Requires(post):	glib2
Requires(post):	pango
Requires:	libXrandr

Provides:	gtk3-ubuntu = %{version}-%{release}

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+.


%package immodules
Summary:	Input methods for GTK+
Group:		System Environment/Libraries

Requires:	gtk3%{?_isa} = %{version}-%{release}

%description immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.


%package immodule-xim
Summary:	XIM support for GTK+
Group:		System Environment/Libraries

Requires:	gtk3%{?_isa} = %{version}-%{release}

%description immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.


%package devel
Summary:	Development files for GTK+
Group:		Development/Libraries

Requires:	gtk3 = %{version}-%{release}
Requires:	pkgconfig(gdk-pixbuf-2.0)
Requires:	pkgconfig(x11)
Requires:	pkgconfig(xcomposite)
Requires:	pkgconfig(xcursor)
Requires:	pkgconfig(xext)
Requires:	pkgconfig(xfixes)
Requires:	pkgconfig(xi)
Requires:	pkgconfig(xinerama)
Requires:	pkgconfig(xrandr)
# for /usr/share/aclocal
Requires:	automake

Provides:	gtk3-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 3 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk3-devel-docs package.


%package devel-docs
Summary:	Developer documentation for GTK+
Group:		Development/Libraries

Requires:	gtk3 = %{version}-%{release}

%description devel-docs
This package contains developer documentation for version 3 of the GTK+
widget toolkit.


%prep
%setup -q -n gtk+-%{version}

# Apply Ubuntu patches
tar zxvf "%{SOURCE99}"
# Do not apply these patches
  # Debian/Ubuntu's multiarch
    sed -i '/061_multiarch_module_fallback.patch/d' debian/patches/series
  # Fedora's tracker is not compiled with FTS
    sed -i '/044_tracker_fts.patch/d' debian/patches/series
  # Ubuntu's defaults
    sed -i '/022_disable-viqr-im-for-vi-locale.patch/d' debian/patches/series
  # Not needed
    sed -i '/071_fix-installation-of-HTML-images.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
%configure \
  --enable-gtk-doc \
  --enable-gtk2-dependency \
  --enable-xkb \
  --enable-xinerama \
  --enable-xrandr \
  --enable-xfixes \
  --enable-xcomposite \
  --enable-xdamage \
  --enable-x11-backend \
  --enable-colord

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk30
%find_lang gtk30-properties

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gtk-query-immodules-3.0 gtk-query-immodules-3.0-%{__isa_bits}
)

# Input method frameworks want this
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/*/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/theming-engines


%post
/sbin/ldconfig
gtk-query-immodules-3.0-%{__isa_bits} --update-cache
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post devel
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache


%post immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache


%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gtk-query-immodules-3.0-%{__isa_bits} --update-cache
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%postun devel
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%postun immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache


%postun immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache


%files -f gtk30.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-3.0*
%{_bindir}/gtk-launch
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/libgailutil-3.so.*
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/%{bin_version}
%{_libdir}/gtk-3.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-3.0/%{bin_version}/immodules
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-3.0/%{bin_version}/printbackends
%{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%dir %{_sysconfdir}/gtk-3.0
%dir %{_sysconfdir}/X11/xinit/xinput.d/
%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk-query-immodules-3.0.1.gz
%{_mandir}/man1/gtk-launch.1.gz
%exclude %{_mandir}/man1/gtk-update-icon-cache.1.gz
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml


%files immodules
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-viqr.so
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf


%files immodule-xim
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-xim.so


%files devel -f gtk30-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/gtk-3.0
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml


%files devel-docs
%{_datadir}/gtk-doc


%changelog
* Fri May 03 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.4-100.0ubuntu8
- Version 3.6.4
- Ubuntu release 0ubuntu8

* Sat Jan 26 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.4-100.0ubuntu3
- Version 3.6.4
- Ubuntu release 0ubuntu3

* Mon Nov 26 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.2-101.0ubuntu1
- Version 3.6.2
- Ubuntu release 0ubuntu1

* Sun Nov 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.2-1.ubuntu3.6.0.0ubuntu3.1
- Version 3.6.2

* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-1.ubuntu3.6.0.0ubuntu3.1
- Ubuntu release 0ubuntu3.1
- Merge Fedora's changes:
  - 3.6.1-2: Don't pull in imsettings just for a directory

* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-1.ubuntu3.6.0.0ubuntu3
- Version 3.6.1
- Ubuntu version 3.6.0
- Ubuntu release 0ubuntu3

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-1.0ubuntu2
- Version 3.6.0
- Ubuntu release 0ubuntu2

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.18-1.0ubuntu2
- Initial release for Fedora 18
- Version 3.5.18
- Ubuntu release 0ubuntu2
- Use pkgconfig for dependencies
- Remove '-ubuntu' suffix from packages - yum priorities works in F18
- Remove obsoletes for packages unsupported in Fedora 18
- Drop fixed 100_overlay_scrollbar_loading.patch patch
  - No longer needed with new scrollbar code

* Mon Sep 03 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu0.4
- Ubuntu release 0ubuntu0.4

* Sat Jul 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu0.3
- Fix hardcoded path in patch for overlay scrollbars

* Thu Jul 12 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu0.3
- Update to Ubuntu release 0ubuntu0.3

* Fri Jul 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu0.2
- Stop using epochs to override official packages

* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1:3.4.2-1.0ubuntu0.2
- Version 3.4.2
- Ubuntu release 0ubuntu0.2

* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1:3.4.1-1.0ubuntu1
- Initial release based off of F17's gtk3 packaging
- Version 3.4.1
- Ubuntu release 0ubuntu6
