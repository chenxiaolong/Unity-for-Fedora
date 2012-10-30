# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# Based off of Fedora 18's spec file

# Nautilus 3.6 won't be included in Ubuntu 12.10, so we'll use the patches from
# the GNOME3 PPA
%define _ppa_rel 0ubuntu1~ubuntu12.10.2

Name:		nautilus
Version:	3.6.1
Release:	101.ppa%{_ppa_rel}%{?dist}
Summary:	File manager for GNOME

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://projects.gnome.org/nautilus/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/nautilus/3.6/nautilus-%{version}.tar.xz
Source99:	http://ppa.launchpad.net/gnome3-team/gnome3/ubuntu/pool/main/n/nautilus/nautilus_%{version}-%{_ppa_rel}.debian.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
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
BuildRequires:	pkgconfig(tracker-sparql-0.14)
BuildRequires:	pkgconfig(unity)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zeitgeist-1.0)

# The nautilus binary links against the main .so file, rather than the versioned
# .so file, so rpm's soname dependency won't work.
Requires:	nautilus-extensions = %{version}-%{release}

Requires:	gsettings-desktop-schemas
Requires:	gvfs
Requires:	redhat-menus

Provides:	nautilus-ubuntu = %{version}-%{release}

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

Provides:	nautilus-ubuntu-extensions = %{version}-%{release}

%description extensions
This package provides the libraries used by nautilus extensions.


%package devel
Summary:	Support for developing nautilus extensions
License:	LGPLv2+
Group:		Development/Libraries

Requires:	%{name}%{_isa} = %{version}-%{release}

Provides:	nautilus-ubuntu-devel = %{version}-%{release}

%description devel
This package provides libraries and header files needed for developing nautilus
extensions.


%prep
%setup -q -n nautilus-%{version}

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Don't use Ubuntu help
    sed -i '/15_use-ubuntu-help.patch/d' debian/patches/series
  # Do not hide nautilus from the startup applications tool
    sed -i '/08_clean_session_capplet.patch/d' debian/patches/series

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
update-mime-database %{_datadir}/mime/ &>/dev/null || :

%postun
update-mime-database %{_datadir}/mime/ &>/dev/null || :

if [ ${1} -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null || :


%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig


%files -f nautilus.lang
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS
%{_bindir}/nautilus
%{_bindir}/nautilus-autorun-software
%{_bindir}/nautilus-connect-server
%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop
%dir %{_libdir}/nautilus/
%dir %{_libdir}/nautilus/extensions-3.0/
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_libexecdir}/nautilus-convert-metadata
%{_libexecdir}/nautilus-shell-search-provider
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/applications/nautilus-autorun-software.desktop
%{_datadir}/applications/nautilus-connect-server.desktop
%{_datadir}/applications/nautilus-folder-handler.desktop
%{_datadir}/applications/nautilus-home.desktop
%{_datadir}/applications/nautilus.desktop
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/gnome-shell/search-providers/nautilus-search-provider.ini
%{_datadir}/mime/packages/nautilus.xml
%dir %{_datadir}/nautilus/
%{_datadir}/nautilus/nautilus-extras.placeholder
%{_datadir}/nautilus/nautilus-suggested.placeholder
%{_datadir}/pixmaps/nautilus.xpm
%{_mandir}/man1/nautilus-connect-server.1.gz
%{_mandir}/man1/nautilus.1.gz


%files extensions
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS
%{_libdir}/libnautilus-extension.so.1
%{_libdir}/libnautilus-extension.so.1.4.0
%{_libdir}/girepository-1.0/Nautilus-3.0.typelib
%dir %{_libdir}/nautilus/


%files devel
%doc AUTHORS ChangeLog HACKING NEWS README README.commits THANKS
%dir %{_includedir}/nautilus/
%dir %{_includedir}/nautilus/libnautilus-extension/
%{_includedir}/nautilus/libnautilus-extension/*.h
%{_libdir}/libnautilus-extension.so
%{_libdir}/pkgconfig/libnautilus-extension.pc
%{_datadir}/gir-1.0/Nautilus-3.0.gir
%doc %{_datadir}/gtk-doc/html/libnautilus-extension/


%changelog
* Mon Oct 29 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-101.ppa0ubuntu1~ubuntu12.10.2
- PPA release 0ubuntu1~ubuntu12.10.2

* Sat Oct 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.1-100.ppa3.6.0.ppa0ubuntu1~ubuntu12.10.1
- Version 3.6.1

* Fri Sep 28 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.6.0-100.0ubuntu1~ubuntu12.10.1
- Version 3.6.0
- GNOME 3 PPA release 0ubuntu1~ubuntu12.10.1

* Sun Sep 23 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.5.92-100.0ubuntu1~ubuntu12.10.2
- Initial release for Fedora 18
- Version 3.5.92
- GNOME 3 PPA release 0ubuntu1~ubuntu12.10.2

* Tue Sep 18 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-3.0ubuntu4
- Remove "Ubuntu Help" from desktop menu

* Wed Aug 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-2.0ubuntu4
- Fix directory ownership

* Sat Aug 11 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.2-1.0ubuntu4
- Initial release
- Based off of Fedora 17's spec file
- Version 3.4.2
- Ubuntu release 0ubuntu4
