# Based off of Fedora 17's spec
# Modifications by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _obsolete_ver 3.5.0-100

# 'fedora_' is prefixed to the sources and patches to group them together in OBS

%define _ubuntu_rel 0ubuntu0.3

%global glib2_version 2.32.0
%global pango_version 1.30.0
%global gdk_pixbuf_version 2.26.0
%global atk_version 2.1.5
%global cairo_version 1.10.0
%global xrandr_version 1.2.99.4-2

%global bin_version 3.0.0

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name:		gtk3-ubuntu
Version:	3.4.2
Release:	1.%{_ubuntu_rel}%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.gtk.org
#VCS:		git:git://git.gnome.org/gtk+
Source:		http://download.gnome.org/sources/gtk+/3.4/gtk+-%{version}.tar.xz
Source1:	fedora_im-cedilla.conf

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gtk+3.0_%{version}-%{_ubuntu_rel}.debian.tar.gz

# upstream fix
Patch0:		fedora_0002-GtkPlug-fix-handling-of-key-events-for-different-lay.patch

BuildRequires:	gnome-common autoconf automake intltool gettext
BuildRequires:	atk-devel >= %{atk_version}
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	cairo-devel >= %{cairo_version}
BuildRequires:	cairo-gobject-devel >= %{cairo_version}
BuildRequires:	pango-devel >= %{pango_version}
BuildRequires:	gdk-pixbuf2-devel >= %{gdk_pixbuf_version}
BuildRequires:	gtk2-devel
BuildRequires:	libXi-devel
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	cups-devel
BuildRequires:	libXrandr-devel >= %{xrandr_version}
BuildRequires:	libXrender-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXi-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	colord-devel

# required for icon theme apis to work
Requires:	hicolor-icon-theme

# We need to prereq these so we can run gtk-query-immodules-3.0
Requires(post):	glib2 >= %{glib2_version}
Requires(post):	atk >= %{atk_version}
Requires(post):	pango >= %{pango_version}
Requires:	libXrandr >= %{xrandr_version}

# gtk3 no longer provides the GtkThemeEngine interface used there
Obsoletes:	gtk3-engines <= 2.91.5-5.fc15

Provides:	gtk3%{?_isa} = %{version}-%{release}
Provides:	gtk3         = %{version}-%{release}
Obsoletes:	gtk3%{?_isa} < %{_obsolete_ver}
Obsoletes:	gtk3         < %{_obsolete_ver}

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+.


%package immodules
Summary:	Input methods for GTK+
Group:		System Environment/Libraries
Requires:	gtk3-ubuntu%{?_isa} = %{version}-%{release}
# for /etc/X11/xinit/xinput.d
Requires:	imsettings

Provides:	gtk3-immodules%{?_isa} = %{version}-%{release}
Provides:	gtk3-immodules         = %{version}-%{release}
Obsoletes:	gtk3-immodules%{?_isa} < %{_obsolete_ver}
Obsoletes:	gtk3-immodules         < %{_obsolete_ver}

%description immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.


%package immodule-xim
Summary:	XIM support for GTK+
Group:		System Environment/Libraries
Requires:	gtk3-ubuntu%{?_isa} = %{version}-%{release}

Provides:	gtk3-immodule-xim%{?_isa} = %{version}-%{release}
Provides:	gtk3-immodule-xim         = %{version}-%{release}
Obsoletes:	gtk3-immodule-xim%{?_isa} < %{_obsolete_ver}
Obsoletes:	gtk3-immodule-xim         < %{_obsolete_ver}

%description immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.


%package devel
Summary:	Development files for GTK+
Group:		Development/Libraries
Requires:	gtk3-ubuntu = %{version}-%{release}
Requires:	gdk-pixbuf2-devel
Requires:	libX11-devel, libXcursor-devel, libXinerama-devel
Requires:	libXext-devel, libXi-devel, libXrandr-devel
Requires:	libXfixes-devel, libXcomposite-devel
# for /usr/share/aclocal
Requires:	automake

Obsoletes:	gtk3-engines-devel <= 2.91.5-5.fc15

Provides:	gtk3-devel%{?_isa} = %{version}-%{release}
Provides:	gtk3-devel         = %{version}-%{release}
Obsoletes:	gtk3-devel%{?_isa} < %{_obsolete_ver}
Obsoletes:	gtk3-devel         < %{_obsolete_ver}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 3 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk3-devel-docs package.


%package devel-docs
Summary:	Developer documentation for GTK+
Group:		Development/Libraries
Requires:	gtk3-ubuntu = %{version}-%{release}

Provides:	gtk3-devel-docs%{?_isa} = %{version}-%{release}
Provides:	gtk3-devel-docs         = %{version}-%{release}
Obsoletes:	gtk3-devel-docs%{?_isa} < %{_obsolete_ver}
Obsoletes:	gtk3-devel-docs         < %{_obsolete_ver}

%description devel-docs
This package contains developer documentation for version 3 of the GTK+
widget toolkit.


%prep
%setup -q -n gtk+-%{version}
%patch0 -p1

# Apply Ubuntu patches
tar zxvf "%{SOURCE99}"
# Do not apply these patches
  # Debian/Ubuntu's multiarch
    sed -i '/061_multiarch_module_fallback.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build

(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
        --enable-gtk2-dependency \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
        --enable-colord \
)

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
%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk-query-immodules-3.0.1.gz
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

* Fri May 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.3-2
- Fix handling of keyboard layouts in plug/socket

* Fri May 11 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.3-1
- Update to 3.4.3

* Fri Apr 13 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Mon Apr  2 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.0-2
- Bump up glib dependency (#806042)

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.20-1
- Update to 3.3.20

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.18-1
- Update to 3.3.18

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.16-1
- Update to 3.3.16

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.14-1
- Update to 3.3.14

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.10-1
- Update to 3.3.10

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.8-1
- Update to 3.3.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-2
- Revert a problematic focus handling change

* Mon Dec 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-1
- Update to 3.3.6

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Wed Nov  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Oct 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-2
- Fix crashes when turning a11y on and off repeatedly

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep 13 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.18-1
- Update to 3.1.18

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.16-1
- Update to 3.1.16

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.12-1
- Update to 3.1.12

* Sat Jul 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Tue Jul  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.8-1
- Update to 3.1.8

* Tue Jun 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.9-1
- Update to 3.0.9

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-3
- Move im-cedilla back to the main package (#637399)

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-2
- Add a missed backport

* Sun Apr  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-1
- Update to 3.0.8

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.7-1
- Update to 3.0.7

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.6-1
- Update to 3.0.6

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.5-1
- Update to 3.0.5

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Sat Feb 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Fix frequent crashes on double-click events

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-1
- Update to 2.99.3

* Mon Jan 24 2011 Dan Williams <dcbw@redhat.com> 2.99.2-2
- Fix bug in gtk_show_uri() which caused crashes when plugging in USB drives

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> 2.99.2-1
- Update to 2.99.2

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.1-1
- Update to 2.99.1

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-3
- Obsolete gtk3-engines

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-2
- Provide the right directory for theming engines

* Thu Jan  6 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-1
- Update to 2.99.0
- Drop gtk-update-icon-cache and gtk-builder-convert to
  avoid conflict with gtk2
- Drop the tooltips-style patch for now

* Thu Dec  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-2
- Make gnome-terminal work again

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Wed Oct 20 2010 Richard Hughes <richard@hughsie.com> 2.91.1-1
- Update to 2.91.1

* Tue Oct 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-2
- Fix a crash in the tooltip code

* Sat Oct  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.7-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclaesn@redhat.com> 2.90.7-2
- Reinstate the tooltip look

* Mon Sep 20 2010 Bastien Nocera <bnocera@redhat.com> 2.90.7-1
- Update to 2.90.7

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.5-5
- Co-own /usr/share/gtk-doc
- gtk3-devel requires gdk-pixbuf2-devel

* Mon Jul 26 2010 Colin Walters <walters@verbum.org> - 2.90.5-4
- gtk3-devel requires gdk-pixbuf-devel

* Thu Jul 22 2010 Colin Walters <walters@verbum.org> - 2.90.5-2
- Rebuild with new gobject-introspection

* Mon Jul 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.5-1
- Update to 2.90.5

* Fri Jul  9 2010 Colin Walters <walters@verbum.org> - 2.90.4-3
- Update tooltip style patch to remove unused GdkRegion

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.90.4-2
- Changes to support rebuilds from snapshots

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-1
- Update to 2.90.4

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> 2.90.3-1
- Update to 2.90.3

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-2
- Copy some tweaks from gtk2

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-1
- Update to 2.90.2

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> 2.90.1-1
- Update to 2.90.1

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-5
- Some more package review feedback

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-4
- Remove %%check again, it causes trouble

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-3
- More review feedback

* Wed May 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-2
- Incorporate review feedback

* Wed May 11 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-1
- Update to the 2.90.0 release
- Complete parallel installability

* Mon May 10 2010 Richard Hughes <richard@hughsie.com> 2.90.0-0.0.20100510git
- Update from git
