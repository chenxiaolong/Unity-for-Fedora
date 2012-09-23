# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of Fedora 17's spec file

%define _ubuntu_rel 0ubuntu4
%define _obsolete_ver 3.5.0-100

Name:		nautilus-ubuntu
Version:	3.4.2
Release:	3.%{_ubuntu_rel}%{?dist}
Summary:	File manager for GNOME

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://projects.gnome.org/nautilus/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/nautilus/3.4/nautilus-%{version}.tar.xz
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/nautilus_%{version}-%{_ubuntu_rel}.debian.tar.gz

# Fedora's patches
Patch10:	fedora_rtl-fix.patch
# GVfs apps should convey when eject/unmount takes a long time
# https://bugzilla.redhat.com/show_bug.cgi?id=819492
Patch11:	fedora_nautilus-3.4.3-unmount-notification.patch

# Remove Ubuntu Help Menu Entry
Patch20:	0001_Remove_Ubuntu_Help.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zeitgeist-1.0)

# The nautilus binary links against the main .so file, rather than the versioned
# .so file, so rpm's soname dependency won't work.
Requires:	nautilus-extensions = %{version}-%{release}

Requires:	gnome-icon-theme
Requires:	gsettings-desktop-schemas
Requires:	gvfs
Requires:	redhat-menus

Provides:	nautilus%{?_isa} = %{version}-%{release}
Provides:	nautilus         = %{version}-%{release}
Obsoletes:	nautilus%{?_isa} < %{_obsolete_ver}
Obsoletes:	nautilus         < %{_obsolete_ver}

%description
Nautilus is the file manager and graphical shell for the GNOME desktop that
makes it easy to manage your files and the rest of your system. It allows to
browse directories on local and remote filesystems, preview files and launch
applications associated with them. It is also responsible for handling the icons
on the GNOME desktop.


%package extensions
Summary:	Nautilus extensions library
License:	LGPLv2+
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

Provides:	nautilus-extensions%{?_isa} = %{version}-%{release}
Provides:	nautilus-extensions         = %{version}-%{release}
Obsoletes:	nautilus-extensions%{?_isa} < %{_obsolete_ver}
Obsoletes:	nautilus-extensions         < %{_obsolete_ver}

%description extensions
This package provides the libraries used by nautilus extensions.


%package devel
Summary:	Support for developing nautilus extensions
License:	LGPLv2+
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

Provides:	nautilus-devel%{?_isa} = %{version}-%{release}
Provides:	nautilus-devel         = %{version}-%{release}
Obsoletes:	nautilus-devel%{?_isa} < %{_obsolete_ver}
Obsoletes:	nautilus-devel         < %{_obsolete_ver}

%description devel
This package provides libraries and header files needed for developing nautilus
extensions.


%prep
%setup -q -n nautilus-%{version}

# Apply Fedora's patches
%patch10 -p1 -b .rtl-fix
%patch11 -p1 -b .unmount-notification

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Don't use Ubuntu help
    sed -i '/15_use-ubuntu-help.patch/d' debian/patches/series
  # Don't use launchpad-integration
    sed -i '/01_lpi.patch/d' debian/patches/series
  # Do not hide nautilus from the startup applications tool
    sed -i '/08_clean_session_capplet.patch/d' debian/patches/series

# Fix patches
  # Remove Ubuntu Help
%patch20 -p0 -b .no-nautilus-help

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi


%build
CFLAGS="$RPM_OPT_FLAGS -g -DNAUTILUS_OMIT_SELF_CHECK" \
  %configure \
    --disable-more-warnings \
    --disable-update-mimedb

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

## Install Ubuntu's files

# Pixmap
install -dm755 $RPM_BUILD_ROOT%{_datadir}/pixmaps/
install -m644 debian/nautilus.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/

# GSettings defaults
install -dm755 $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/
install -m644 debian/nautilus.gsettings-override \
  $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override

# Desktop files
install -m644 \
  debian/nautilus-home.desktop \
  debian/nautilus-folder-handler.desktop \
  $RPM_BUILD_ROOT%{_datadir}/applications/

# Verify and modify desktop files
desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  --add-only-show-in GNOME \
  --add-only-show-in Unity \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

#desktop-file-validate \
#  $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang nautilus


%post
/sbin/ldconfig
update-mime-database %{_datadir}/mime/ &>/dev/null || :

%postun
/sbin/ldconfig
update-mime-database %{_datadir}/mime/ &>/dev/null || :

if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolors/ &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :


%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig


%files -f nautilus.lang
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS TODO
%{_bindir}/nautilus
%{_bindir}/nautilus-autorun-software
%{_bindir}/nautilus-connect-server
%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop
%dir %{_libdir}/nautilus/
%dir %{_libdir}/nautilus/extensions-3.0/
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_libexecdir}/nautilus-convert-metadata
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/applications/nautilus-autorun-software.desktop
%{_datadir}/applications/nautilus-folder-handler.desktop
%{_datadir}/applications/nautilus-home.desktop
%{_datadir}/applications/nautilus.desktop
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/icons/hicolor/16x16/apps/nautilus.png
%{_datadir}/icons/hicolor/22x22/apps/nautilus.png
%{_datadir}/icons/hicolor/24x24/apps/nautilus.png
%{_datadir}/icons/hicolor/32x32/apps/nautilus.png
%{_datadir}/icons/hicolor/scalable/apps/nautilus.svg
%{_datadir}/mime/packages/nautilus.xml
%dir %{_datadir}/nautilus/
%{_datadir}/nautilus/icons/
%{_datadir}/nautilus/nautilus-extras.placeholder
%{_datadir}/nautilus/nautilus-suggested.placeholder
%{_datadir}/pixmaps/nautilus.xpm
%{_mandir}/man1/nautilus-connect-server.1.gz
%{_mandir}/man1/nautilus.1.gz


%files extensions
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS TODO
%{_libdir}/libnautilus-extension.so.1
%{_libdir}/libnautilus-extension.so.1.4.0
%{_libdir}/girepository-1.0/Nautilus-3.0.typelib
%dir %{_libdir}/nautilus/


%files devel
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS TODO
%dir %{_includedir}/nautilus/
%dir %{_includedir}/nautilus/libnautilus-extension/
%{_includedir}/nautilus/libnautilus-extension/*.h
%{_libdir}/libnautilus-extension.so
%{_libdir}/pkgconfig/libnautilus-extension.pc
%{_datadir}/gir-1.0/Nautilus-3.0.gir
%doc %{_datadir}/gtk-doc/html/libnautilus-extension/


%changelog
* Tue Sep 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.0ubuntu4
- Remove "Ubuntu Help" from desktop menu

* Wed Aug 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu4
- Fix directory ownership

* Sat Aug 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu4
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu4
