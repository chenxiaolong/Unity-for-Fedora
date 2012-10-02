# Based off of Fedora 18's spec
# Modifications by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Required when the package is not built in koji
%global _host %{_target_platform}

%define _ubuntu_rel 0ubuntu2

# Note that this is NOT a relocatable package

%define bin_version 2.10.0

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name:		gtk2
Version:	2.24.13
Release:	1.%{_ubuntu_rel}%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.gtk.org
#VCS:		git:git://git.gnome.org/gtk+#gtk-2-24
Source:		http://download.gnome.org/sources/gtk+/2.24/gtk+-%{version}.tar.xz
Source2:	fedora_update-gtk-immodules
Source3:	fedora_im-cedilla.conf

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gtk+2.0_%{version}-%{_ubuntu_rel}.debian.tar.gz

# Biarch changes
Patch0:		fedora_gtk-lib64.patch
Patch1:		fedora_system-python.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=583273
Patch2:		fedora_icon-padding.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599618
Patch8:		fedora_tooltip-positioning.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=592582
#Patch14:	fedora_gtk2-landscape-pdf-print.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=611313
# Included in Ubuntu patch 062_dnd_menubar.patch
Patch15:	fedora_window-dragging.patch

# fix dso.
Patch17:	fedora_gtk2-fixdso.patch

# Patch from Arch Linux TU, György Balló, to fix build with the Ubuntu menuproxy
# code
Patch90:	fix-ubuntumenuproxy-build.patch

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)

BuildRequires:	libjpeg-turbo-devel
BuildRequires:	cups-devel

Provides:	gail = %{version}-%{release}
Obsoletes:	gail < 2.13.0-1

# required for icon theme apis to work
Requires:	hicolor-icon-theme

# We need to prereq these so we can run gtk-query-immodules-2.0
Requires(post):	atk
Requires(post):	glib2
Requires(post):	pango
# and these for gdk-pixbuf-query-loaders
Requires(post):	libtiff
Requires:	libXrandr

Provides:	gtk2-ubuntu = %{version}-%{release}

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.


%package immodules
Summary:	Input methods for GTK+
Group:		System Environment/Libraries

Requires:	gtk2%{?_isa} = %{version}-%{release}
# for /etc/X11/xinit/xinput.d
Requires:	imsettings

%description immodules
The gtk2-immodules package contains standalone input methods that are shipped
as part of GTK+.


%package immodule-xim
Summary:	XIM support for GTK+
Group:		System Environment/Libraries

Requires:	gtk2%{?_isa} = %{version}-%{release}

%description immodule-xim
The gtk2-immodule-xim package contains XIM support for GTK+.


%package devel
Summary:	Development files for GTK+
Group:		Development/Libraries

Requires:	gtk2%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	pkgconfig(atk)
Requires:	pkgconfig(cairo)
Requires:	pkgconfig(gdk-pixbuf-2.0)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(pango)
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

Provides:	gail-devel = %{version}-%{release}
Obsoletes:	gail-devel < 2.13.0-1

Provides:	gtk2-ubuntu-devel = %{version}-%{release}

%description devel
This package contains the libraries amd header files that are needed
for writing applications with the GTK+ widget toolkit. If you plan
to develop applications with GTK+, consider installing the gtk2-devel-docs
package.


%package devel-docs
Summary:	Developer documentation for GTK+
Group:		Development/Libraries

Requires:	gtk2%{?_isa} = %{version}-%{release}
#BuildArch:	noarch

%description devel-docs
This package contains developer documentation for the GTK+ widget toolkit.


%prep
%setup -q -n gtk+-%{version}

%patch0 -p1 -b .lib64
%patch1 -p1 -b .system-python
%patch2 -p1 -b .icon-padding
%patch8 -p1 -b .tooltip-positioning
#%patch14 -p1 -b .landscape-pdf-print
#%patch15 -p1 -b .window-dragging
%patch17 -p1 -b .fixdso

# Apply Ubuntu patches
tar zxvf "%{SOURCE99}"
# Do not apply these patches
  # Debian/Ubuntu multiarch
    sed -i '/041_ia32-libs.patch/d' debian/patches/series
    sed -i '/098_multiarch_module_path.patch/d' debian/patches/series
  # Static linking stuff for udebs
    sed -i '/001_static-linking-dont-query-immodules.patch/d' debian/patches/series
    sed -i '/002_static-linking-dont-build-perf.patch/d' debian/patches/series
  # Breaks pkgconfig
    sed -i '/003_gdk.pc_privates.patch/d' debian/patches/series
  # Ubuntu's multiarch gtk.immodules file location
    sed -i '/011_immodule-cache-dir.patch/d' debian/patches/series

for i in $(cat debian/patches/series | grep -v '#'); do
  patch -Np1 -i "debian/patches/${i}"
done

%patch90 -p1 -b .menuproxy

autoreconf -vfi


%build
%configure \
  --enable-gtk-doc \
  --with-xinput=xfree \
  --enable-debug \

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

# truncate NEWS
awk '/^Overview of Changes/ { seen+=1 }
{ if (seen < 2) print }
{ if (seen == 2) { print "For older news, see http://git.gnome.org/cgit/gtk+/plain/NEWS"; exit } }' NEWS > tmp; mv tmp NEWS


%install
# Deriving /etc/gtk-2.0/$host location
# NOTE: Duplicated below
#
# autoconf changes linux to linux-gnu
case "%{_host}" in
  *linux) host="%{_host}-gnu"
  ;;
  *) host="%{_host}"
  ;;
esac

# autoconf uses powerpc not ppc
host=`echo $host | sed "s/^ppc/powerpc/"`
# autoconf uses ibm-linux not redhat-linux (s390x)
host=`echo $host | sed "s/^s390\(x\)*-redhat/s390\1-ibm/"`

# Make sure that the host value that is passed to the compile
# is the same as the host that we're using in the spec file
#
compile_host=`grep 'host_triplet =' gtk/Makefile | sed "s/.* = //"`

if test "x$compile_host" != "x$host" ; then
  echo 1>&2 "Host mismatch: compile='$compile_host', spec file='$host'" && exit 1
fi

make install DESTDIR=$RPM_BUILD_ROOT        \
             RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk20
%find_lang gtk20-properties

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0
#
# Make cleaned-up versions of tutorials, examples, and faq for installation
#
mkdir -p tmpdocs
cp -aR docs/tutorial/html tmpdocs/tutorial
cp -aR docs/faq/html tmpdocs/faq

for dir in examples/* ; do
  if [ -d $dir ] ; then
     mkdir -p tmpdocs/$dir
     for file in $dir/* ; do
       install -m 0644 $file tmpdocs/$dir
     done
  fi
done

# We need to have separate 32-bit and 64-bit binaries
# for places where we have two copies of the GTK+ package installed.
# (we might have x86_64 and i686 packages on the same system, for example.)
case "$host" in
  alpha*|ia64*|powerpc64*|s390x*|x86_64*)
   mv $RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-2.0 $RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-2.0-64
   ;;
  *)
   mv $RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-2.0 $RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-2.0-32
   ;;
esac

# Install wrappers for the binaries
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/update-gtk-immodules

# Input method frameworks want this
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d
cp %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/*/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/$host
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/$host/gtk.immodules

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{bin_version}/filesystems

#
# We need the substitution of $host so we use an external
# file list
#
echo %dir %{_sysconfdir}/gtk-2.0/$host >> gtk20.lang
echo %ghost %{_sysconfdir}/gtk-2.0/$host/gtk.immodules >> gtk20.lang


%post
/sbin/ldconfig
/usr/bin/update-gtk-immodules %{_host}


%post immodules
/usr/bin/update-gtk-immodules %{_host}


%post immodule-xim
/usr/bin/update-gtk-immodules %{_host}


%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  /usr/bin/update-gtk-immodules %{_host}
fi


%postun immodules
/usr/bin/update-gtk-immodules %{_host}


%postun immodule-xim
/usr/bin/update-gtk-immodules %{_host}


%files -f gtk20.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gtk-query-immodules-2.0*
%{_bindir}/update-gtk-immodules
%{_bindir}/gtk-update-icon-cache
%{_libdir}/libgtk-x11-2.0.so.*
%{_libdir}/libgdk-x11-2.0.so.*
%{_libdir}/libgailutil.so.*
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/%{bin_version}
%{_libdir}/gtk-2.0/%{bin_version}/engines
%{_libdir}/gtk-2.0/%{bin_version}/filesystems
%dir %{_libdir}/gtk-2.0/%{bin_version}/immodules
%{_libdir}/gtk-2.0/%{bin_version}/printbackends
%{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_datadir}/themes/Raleigh
%dir %{_sysconfdir}/gtk-2.0
%{_libdir}/girepository-1.0


%files immodules
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-viqr.so
%{_sysconfdir}/X11/xinit/xinput.d/im-cedilla.conf
%config(noreplace) %{_sysconfdir}/gtk-2.0/im-multipress.conf


%files immodule-xim
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-xim.so


%files devel -f gtk20-properties.lang
%{_libdir}/lib*.so
%{_libdir}/gtk-2.0/include
%{_includedir}/*
%{_datadir}/aclocal/*
%{_bindir}/gtk-builder-convert
%{_libdir}/pkgconfig/*
%{_bindir}/gtk-demo
%{_datadir}/gtk-2.0
%{_datadir}/gir-1.0


%files devel-docs
%{_datadir}/gtk-doc
# oops, man pages went missing
# %{_mandir}/man1/*
%doc tmpdocs/tutorial
%doc tmpdocs/faq
%doc tmpdocs/examples


%changelog
* Tue Oct 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.13-1.0ubuntu2
- Ubuntu release 0ubuntu2
  - don't crash with latest overlay-scrollbar version
- Drop 0001_lib64_fix_100_overlay_scrollbar_loading.patch
  - Not needed anymore

* Mon Oct 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.13-1.0ubuntu1
- Version 2.24.13
- Ubuntu release 0ubuntu1

* Thu Sep 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.12-1.0ubuntu1
- Initial release for Fedora 18
- Version 2.24.12
- Ubuntu release 0ubuntu1
- Use pkgconfig for dependencies
- Removed Provides and Obsoletes tags for stuff that's not supported anymore
- Remove '-ubuntu' suffix on packages - yum priorities works in F18

* Sun Jul 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.11-1.0ubuntu1
- Version 2.24.11
- Ubuntu release 0ubuntu1

* Sat Jul 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.10-2.0ubuntu6
- Fix hardcoded path in patch for overlay scrollbars

* Fri Jul 06 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.24.10-1.0ubuntu6
- Stop using epochs to override official version

* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1:2.24.10-1.0ubuntu6
- Initial release based off of F17's gtk2 sources
- Version 2.24.10
- Ubuntu release 0ubuntu6
