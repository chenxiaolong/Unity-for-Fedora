# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _git_date 20120521
%define _fedora_epoch 1
%define _fedora_rel 9
%define _ubuntu_ver 0.9.4.1
%define _ubuntu_rel 0ubuntu2

%define _fedora_fullver %{_fedora_epoch}:%{version}-%{_fedora_rel}.git%{_git_date}%{?dist}
%define _obsolete_ver %{_fedora_epoch}:0.9.5.0-100

Name:		NetworkManager-gnome-ubuntu
Version:	0.9.4.0
# Long enough? :P
Release:	1.git%{_git_date}.fedora%{_fedora_rel}.ubuntu%{_ubuntu_ver}.%{_ubuntu_rel}%{?dist}
Summary:	Network Manager applet for GNOME and Unity

Group:		Applications/Internet
License:	GPLv2+
URL:		http://projects.gnome.org/NetworkManager/
# The sources were made by Fedora 17's NetworkManager maintainer. Sources can be
# downloaded by running:
#   fedpkg co -a -B NetworkManager
#   cd f17/
#   fedpkg sources
Source0:	network-manager-applet-0.9.4.0.git20120521.tar.bz2

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/network-manager-applet_%{_ubuntu_ver}-%{_ubuntu_rel}.debian.tar.gz

Patch0:		0001_Disable_-Werror.patch

# Fedora's patches
Patch10:	fedora_nm-applet-no-notifications.patch
Patch11:	fedora_nm-applet-wifi-dialog-ui-fixes.patch
Patch12:	fedora_applet-ignore-deprecated.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libnm-glib-vpn)
BuildRequires:	pkgconfig(libnm-util)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(NetworkManager)

Requires(pre):	GConf2
Requires(post):	GConf2
Requires(preun):	GConf2

Requires:	gnome-icon-theme

Requires:	NetworkManager      = %{_fedora_fullver}
Requires:	NetworkManager-glib = %{_fedora_fullver}
Requires:	NetworkManager-gtk  = %{_fedora_fullver}

# Replace official version
Provides:	NetworkManager-gnome%{?_isa} = %{_fedora_fullver}
Provides:	NetworkManager-gnome         = %{_fedora_fullver}
Obsoletes:	NetworkManager-gnome%{?_isa} < %{_obsolete_ver}
Obsoletes:	NetworkManager-gnome         < %{_obsolete_ver}

%description
This package contains the applet for the GNOME and Unity desktops for connecting
to wired and wireless networks.


%prep
%setup -q -n network-manager-applet-%{version}

%patch0 -p1 -b .Werror

# Apply Fedora's patches
%patch10 -p2 -b .notifications
%patch11 -p2 -b .ui-fixes
%patch12 -p2 -b .deprecated

# Apply Ubuntu's patches
tar zxvf '%{SOURCE99}'

# Disable patches
  # Some UI stuff
    sed -i '/revert_git_policy_error_dialog_ba8381a.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -vfi

# Use Ubuntu's icons
cp debian/icons/22/* icons/22/


%build
%configure \
  --enable-indicator \
  --with-bluetooth \
  --with-gtkver=3 \
  --disable-schemas-install \
  --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

# Create manual page
pushd debian/
docbook2man nm-applet.sgml || :
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Install Ubuntu's files
install -dm755 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/

install -m644 debian/icons/22/nm-device-wired-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
# --------
install -m644 debian/icons/22/nm-signal-00-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
ln -s nm-signal-00.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-none.png
ln -s nm-signal-00-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-none-secure.png
# --------
install -m644 debian/icons/22/nm-signal-25-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
ln -s nm-signal-25.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-low.png
ln -s nm-signal-25-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-low-secure.png
# --------
install -m644 debian/icons/22/nm-signal-50-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
ln -s nm-signal-50.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-medium.png
ln -s nm-signal-50-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-medium-secure.png
# --------
install -m644 debian/icons/22/nm-signal-75-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
ln -s nm-signal-75.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-high.png
ln -s nm-signal-75-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-high-secure.png
# --------
install -m644 debian/icons/22/nm-signal-100-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/
ln -s nm-signal-100.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-full.png
ln -s nm-signal-100-secure.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/gsm-3g-full-secure.png

# Remove files not belonging to this package
rm -v $RPM_BUILD_ROOT%{_libdir}/libnm-gtk.*
rm -rv $RPM_BUILD_ROOT%{_datadir}/libnm-gtk/
rm -rv $RPM_BUILD_ROOT%{_includedir}/libnm-gtk/
rm -rv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libnm-gtk.pc

# Validate desktop files
desktop-file-validate \
  $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/nm-applet.desktop
desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/nm-connection-editor.desktop

# The original package provides this directory, so we will too
install -dm755 $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties/

# Install manual page
install -dm755 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m644 debian/nm-applet.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

%find_lang nm-applet


%files -f nm-applet.lang
%doc NEWS
%{_bindir}/nm-applet
%{_bindir}/nm-connection-editor
%{_libdir}/gnome-bluetooth/plugins/libnma.so
%{_sysconfdir}/gconf/schemas/nm-applet.schemas
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/nm-device-wireless.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%dir %{_datadir}/gnome-vpn-properties/
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/*.ui
%{_datadir}/nm-applet/keyring.png
%{_mandir}/man1/nm-applet.1.gz


%pre
%gconf_schema_prepare nm-applet

%post
%gconf_schema_upgrade nm-applet
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%preun
%gconf_schema_remove nm-applet

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%changelog
* Tue Jul 17 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.4.0-1.git20120521.fedora9.ubuntu0.9.4.1.0ubuntu2
- Initial release
- Version 0.9.4.0 with git snapshot from May 21, 2012
- Ubuntu version 0.9.4.1
- Ubuntu release 0ubuntu2
- Provides Fedora release 9 and epoch 1
