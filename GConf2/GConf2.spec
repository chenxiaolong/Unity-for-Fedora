# Based off of Fedora 17's spec
# Modifications by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu2

%define libxml2_version 2.4.12
%define glib2_version 2.25.9
%define dbus_version 1.0.1
%define dbus_glib_version 0.74

Summary:	A process-transparent configuration system
Name:		GConf2
Version:	3.2.5
Release:	1.%{_ubuntu_rel}%{?dist}
Epoch:		1
License:	LGPLv2+
Group:		System Environment/Base
#VCS:		git:git://git.gnome.org/gconf
Source0:	http://download.gnome.org/sources/GConf/3.2/GConf-%{version}.tar.xz
Source1:	macros.gconf2
Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/gconf_%{version}-%{_ubuntu_rel}.debian.tar.gz
URL:		http://projects.gnome.org/gconf/

Patch0:		GConf-gettext.patch

BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:	libxslt-devel
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	gtk3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	pkgconfig >= 0.14
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	polkit-devel >= 0.92
BuildRequires:	dbus-glib-devel >= 0.8
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	autoconf automake libtool
Requires:	dbus
# for patch0
Requires:	/usr/bin/killall
Conflicts:	GConf2-dbus

%description
GConf is a process-transparent configuration database API used to
store user preferences. It has pluggable backends and features to
support workgroup administration.


%package devel
Summary:	Headers and libraries for GConf development
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libxml2-devel >= %{libxml2_version}
Requires:	glib2-devel >= %{glib2_version}
# we install a pc file
Requires:	pkgconfig
# we install an automake macro
Requires:	automake
Conflicts:	GConf2-dbus-devel

%description devel
GConf development package. Contains files needed for doing
development using GConf.


%package gtk
Summary:	Graphical GConf utilities
Group:		System Environment/Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gtk
The GConf2-gtk package contains graphical GConf utilities
which require GTK+.


%package common
Summary:	GConf common files
Group:		System Environment/Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description common
The GConf2-common package contains the default configuration
files as well as the polkit service for setting the defaults.


%prep
%setup -q -n GConf-%{version}
%patch0 -p1 -b .gettext

# Apply Ubuntu patches
tar zxvf "%{SOURCE99}"
# Do not apply these patches
  # Hide gsettings-data-convert.desktop from Startup Applications dialog
    sed -i '/05_nodisplay_autostart.patch/d' debian/patches/series
  # Same as Fedora's patch
    sed -i '/02_xml-gettext-domain.patch/d' debian/patches/series

for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done

autoreconf -i -f


%build
%configure --disable-static --enable-defaults-service --disable-orbit --with-gtk=3.0

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gconf/gconf.xml.system
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/rpm-state/gconf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/GConf/gsettings

install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/GConf/2/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/GConf/gsettings

%find_lang %name

## Install Ubuntu stuff ##

# Create directories -> from debian/gconf2-common.dirs
install -dm755 "$RPM_BUILD_ROOT%{_datadir}/gconf/defaults/"
install -dm755 "$RPM_BUILD_ROOT%{_datadir}/gconf/mandatory/"
install -dm755 "$RPM_BUILD_ROOT%{_datadir}/gconf/schemas/"
install -dm755 "$RPM_BUILD_ROOT%{_sharedstatedir}/gconf/defaults/"
install -dm755 "$RPM_BUILD_ROOT%{_sharedstatedir}/gconf/debian.defaults/"
install -dm755 "$RPM_BUILD_ROOT%{_sharedstatedir}/gconf/debian.mandatory/"

# Install xinit file
install -dm755 "$RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/"
install -m755 debian/70gconfd_path-on-session \
               "$RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/"

# Install configuration files
install -dm755 "$RPM_BUILD_ROOT%{_datadir}/gconf/"
install -m644 debian/default.path debian/default.path.md5sum \
               "$RPM_BUILD_ROOT%{_datadir}/gconf/"
install -dm755 "$RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/"
install -m644 debian/default.path \
               "$RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/path"

# Install executables
install -dm755 "$RPM_BUILD_ROOT%{_sbindir}/"
install -m755 debian/gconf-schemas "$RPM_BUILD_ROOT%{_sbindir}/"
install -dm755 "$RPM_BUILD_ROOT%{_bindir}/"
install -m755 debian/update-gconf-defaults "$RPM_BUILD_ROOT%{_bindir}/"

# Install manual pages
install -dm755 "$RPM_BUILD_ROOT%{_mandir}/man8/"
install -m644 debian/update-gconf-defaults.8 "$RPM_BUILD_ROOT%{_mandir}/man8/"


%post
/sbin/ldconfig

if [ $1 -gt 1 ]; then
    if ! fgrep -q gconf.xml.system %{_sysconfdir}/gconf/2/path; then
        sed -i -e 's@xml:readwrite:$(HOME)/.gconf@&\n\n# Location for system-wide settings.\nxml:readonly:/etc/gconf/gconf.xml.system@' %{_sysconfdir}/gconf/2/path
    fi
fi


%postun
/sbin/ldconfig
# From debian/gconf2.postrm
if [ -d /var/lib/gconf ]; then
  find /var/lib/gconf -mindepth 2 -maxdepth 2 -exec rm -rf {} \;
fi


%post common
touch %{_sharedstatedir}/gconf/defaults/%gconf-tree.xml


%postun common
# From debian/gconf2-common.postrm
rm -rf /var/lib/gconf/


%files -f %{name}.lang
%doc COPYING NEWS README
%config(noreplace) %{_sysconfdir}/gconf/2/path
%dir %{_sysconfdir}/gconf
%dir %{_sysconfdir}/gconf/2
%dir %{_sysconfdir}/gconf/gconf.xml.defaults
%dir %{_sysconfdir}/gconf/gconf.xml.mandatory
%dir %{_sysconfdir}/gconf/gconf.xml.system
%dir %{_sysconfdir}/gconf/schemas
%{_bindir}/gconf-merge-tree
%{_bindir}/gconftool-2
%{_bindir}/gsettings-data-convert
%doc %{_mandir}/man1/gsettings-data-convert.1*
%{_sysconfdir}/xdg/autostart/gsettings-data-convert.desktop
%{_libexecdir}/gconfd-2
%{_libdir}/*.so.*
%{_libdir}/GConf/2/*.so
%dir %{_datadir}/sgml
%{_datadir}/sgml/gconf
%{_datadir}/GConf
%{_mandir}/man1/*
%dir %{_libdir}/GConf
%dir %{_libdir}/GConf/2
%{_sysconfdir}/rpm/macros.gconf2
%{_sysconfdir}/dbus-1/system.d/org.gnome.GConf.Defaults.conf
%{_libexecdir}/gconf-defaults-mechanism
%{_datadir}/polkit-1/actions/org.gnome.gconf.defaults.policy
%{_datadir}/dbus-1/system-services/org.gnome.GConf.Defaults.service
%{_datadir}/dbus-1/services/org.gnome.GConf.service
# Something else should probably own this, but I'm not sure what.
%dir %{_localstatedir}/lib/rpm-state/
%{_localstatedir}/lib/rpm-state/gconf/
%{_libdir}/gio/modules/libgsettingsgconfbackend.so
%{_libdir}/girepository-1.0


%files gtk
%{_libexecdir}/gconf-sanity-check-2


%files devel
%{_libdir}/*.so
%{_includedir}/gconf
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/gconf
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0
%{_bindir}/gsettings-schema-convert
%doc %{_mandir}/man1/gsettings-schema-convert.1*


%files common
%defattr(-,root,root,-)
%dir %{_datadir}/gconf/defaults/
%dir %{_datadir}/gconf/mandatory/
%dir %{_datadir}/gconf/schemas/
%dir %{_sharedstatedir}/gconf/defaults/
%dir %{_sharedstatedir}/gconf/debian.defaults/
%dir %{_sharedstatedir}/gconf/debian.mandatory/
%{_datadir}/gconf/default.path
%{_datadir}/gconf/default.path.md5sum
%{_sbindir}/gconf-schemas
%{_bindir}/update-gconf-defaults
%{_mandir}/man8/update-gconf-defaults.8.gz
%{_sysconfdir}/X11/xinit/xinitrc.d/70gconfd_path-on-session


%changelog
* Mon Jun 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 1:3.2.5-1.0ubuntu2
- Initial release based off of F17's GConf2 packaging
- Version 3.2.5
- Ubuntu release 0ubuntu2

* Thu Mar 15 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.5-1
- Update to 3.2.5

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.4-1
- Update to 3.2.4

* Mon Feb 13 2012 Ray Strode <rstrode@redhat.com> 3.2.3-4
- Potentially fix crasher bug
  Resolves: #756245

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.3-3
- Don't build the openldap backend
- Deal gracefully with missing schemas in gsettings-data-convert

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.3-1
- Update to 3.2.3

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Jul 25 2011 Matthew Barnes <mbarnes@redhat.com> 3.1.4-1
- Update to 3.1.4

* Tue Jul 05 2011 Ray Strode <rstrode@redhat.com> 3.1.3-2
- Add back one of the non-upstream patches, since
  it introduced a non-backward compatible change
  to the file format and it's going to be upstreamed soon
  anyway
  Related GNOME: #653922

* Fri Jul 01 2011 Ray Strode <rstrode@redhat.com> 3.1.3-1
- Update to 3.1.3
- Remove orbit dependency
- drop unupstreamed patches judiciously

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.32.4-1
- Update to 2.32.4

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> 2.32.3-1
- Update to 2.32.3

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> 2.32.2-1
- Update to 2.32.2

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.32.1-8
- Rebuild against newer gtk3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-5
- Rebuild against newer gtk3

* Sun Jan 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-4
- Co-own /usr/share/sgml

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-3
- Rebuild against newer gtk3

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.1-2
- Rebuild against new gtk

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-2
- Rebuild against newer gobject-introspection

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Fri Aug 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.7-2
- Strip x permissions from rpm macros file. (#600635)

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.7-1
- Update to 2.31.7

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.31.6-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Tue Jun 29 2010 Matthew Garrett <mjg@redhat.com> - 2.31.5-2
- Fix crasher in gsettings-data-convert caused by wrong realloc size

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Mon Jun 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Thu May 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.31.3-2
- Rebuild for pkgconfig deps (ref: #596433)

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-4
- Install an autostart file for gsettings-data-convert

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-3
- Rebuild against newer glib

* Sun May 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Rebuild against newer glib

* Fri Apr 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.31.1
- Include introspection data

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Thu Mar 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.28.0-10
- own /var/lib/rpm-state/ too

* Wed Mar 03 2010 Tom "spot" Callaway <tcallawa@redhat.com> 2.28.0-9
- add macros.gconf2
- own /var/lib/rpm-state/gconf

* Mon Feb 01 2010 Colin Walters <walters@verbum.org> 2.28.0-8
- Add defaults patch from f-12 branch 

* Mon Feb 01 2010 Colin Walters <walters@verbum.org> 2.28.0-6
- Do not catch segv etc. let abrt catch them

* Thu Jan 28 2010 Ray Strode <rstrode@redhat.com> 2.28.0-5
- Add defattr directive to gtk subpackage files section

* Tue Jan 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.0-4
- Make the defaults mechanism use the right polkit actions

* Mon Dec 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Avoid a crash when gconftool-2 can't read the db  (#547238)

* Wed Oct  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Fix a problem with schema translations

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 2.26.2-6
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.2-4
- Minor directory ownership cleanup

* Tue Jun  9 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.2-3
- Improve the port

* Tue Jun  9 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.2-2
- Port to PolicyKit 1

* Fri May 15 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.2-1
- Update to 2.26.2
- See http://download.gnome.org/sources/GConf/2.26/GConf-2.26.1.news
- See http://download.gnome.org/sources/GConf/2.26/GConf-2.26.2.news

* Mon Apr 27 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-3
- Support client-side translations

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 2.26.0-2
- Explicit Conflicts: GConf2-dbus (#492636)

* Mon Mar 16 2009 Ray Strode <rstrode@redhat.com> - 2.26.0-1
- update to 2.26.0

* Tue Mar  3 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-2
- Avoid some gratitious extra work in the markup backend

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Sun Feb 15 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Sat Jan 10 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.0-1
- Update to 2.25.0

* Tue Dec 16 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-3
- Rebuild for pkg-config requires

* Fri Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-2
- Better URL

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0
- Drop obsolete timeout patch

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2
- Drop upstreamed patches

* Wed Jun  4 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.1-1
- Upodate to 2.23.1

* Mon Jun  2 2008 Matthias Clasen  <mclasen@redhat.com> - 2.22.0-10
- Make gconfd notice defaults changes

* Wed May 21 2008 Ray Strode <rstrode@redhat.com> - 2.22.0-9
- Don't ever try to autolaunch a bus if DISPLAY is unset

* Wed May 21 2008 Ray Strode <rstrode@redhat.com> - 2.22.0-8
- If the session bus isn't running, assume local client side
  access to the database (bug 446703)

* Wed May 14 2008 Ray Strode <rstrode@redhat.com> - 2.22.0-7
- update add_seconds patch to not remove timeouts that aren't
  created anymore

* Mon May 12 2008 Ray Strode <rstrode@redhat.com> - 2.22.0-6
- If the session bus isn't running, don't autolaunch it unless
  we also want to autostart gconfd.

* Thu May 8 2008 Ray Strode <rstrode@redhat.com> - 2.22.0-5
- Tie gconf to session bus.  This means it will exit when the session
  exits and won't leave /tmp/gconf-$USER DoS possibilities

* Sun May 4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-4
- Apply some patches: 
  - Don't spam syslog
  - Handle unsetting mandatory keys without critical warnings 

* Fri May 2 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Add a dbus service to set defaults

* Fri May 2 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Use g_timeout_add_seconds for long timeouts

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.21.90-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Wed Jan  9 2008 Caolan McNamara <caolanm@redhat.com> - 2.21.1-2
- fix .pc so I can build

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1
- Drop upstreamed patches

* Mon Dec  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-4
- Rebuild against new openldap

* Fri Nov 16 2007 Ray Strode <rstrode@redhat.com> - 2.20.1-3
- Add the system-wide settings location in post to be more
  upgrade friendly (config file is noreplace)

* Sun Nov 3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Add a location for system-wide settings

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- 2.20.1 (translation and documentation updates)

* Sat Sep 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Require /usr/bin/killall, since gconftool uses it

* Wed Sep 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-5
- Some more leak fixes

* Tue Sep 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-4
- Fix memory leaks

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.19.1-3
- Rebuild for ppc toolchain bug

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Update license field

* Mon Jun 25 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0.1-2
- Fix a directory ownership issue.  (#233756)

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0.1-1
- Update to 2.18.0.1

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Feb  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.16.0-6
- Split off a -gtk subpackage to reduce dependencies

* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.16.0-5
- Minor cleanups from package review

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.16.0-4
- Own the /etc/gconf/schemas directory
- Misc cleanups

* Sun Oct 29 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-3
- run autoreconf, so that configure gets updated before 
  it generates libtool (so it doesn't just regenerate
  the original, broken libtool) (again bug 203813)

* Tue Oct 24 2006 Ray Strode <rstrode@redhat.com> - 2.16.0-2
- regenerate packaged libtool from RHEL version of libtool so
  that rpath's don't get added to plugin DSOs (bug 203813).

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- 2.16.0
- Update reload patch

* Thu Oct 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-5
- Require a new enough glib2 to fix upgrade issues (#203813)

* Fri Oct  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-4
- Fix an issue with error reporting (#202549)
- Don't ship static libraries
- Require pkgconfig for the -devel package

* Mon Sep 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-3
- Make sure that gconfd dies shortly after the session ends

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-2.1
- rebuild

* Tue Jun  6 2006 Adam Jackson <ajackson@redhat.com> 2.14.0-2
- Rebuild.

* Sun Mar 19 2006 Ray Strode <rstrode@redhat.com> 2.14.0-1
- Update to 2.14.0

* Mon Mar  6 2006 Ray Strode <rstrode@redhat.com> 2.13.5-5
- Only sync the database once when installing multiple
  schema files.  Patch by Josselin Mouette <joss@debian.org>.
  (upstream bug 333353)

* Wed Feb 15 2006 Christopher Aillon <caillon@redhat.com> 2.13.5-4
- Send SIGTERM instead of SIGHUP to gconfd

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> 2.13.5-3.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 2.13.5-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 2.13.5-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Christopher Aillon <caillon@redhat.com> 2.13.5-3
- Use the correct patch ;-)

* Wed Feb  1 2006 Christopher Aillon <caillon@redhat.com> 2.13.5-2
- Add patch from Mandriva to reload GConf2 every time a schema is
  added or removed (solves bug 173869)

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Dan Williams <dcbw@redhat.com> 2.12.1-2
- Fix segfault in gconf_unescape_key().  GNOME #323479

* Thu Nov  3 2005 Alexander Larsson <alexl@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Ray Strode <rstrode@redhat.com> 2.11.90-2
- rebuild

* Wed Aug 03 2005 Ray Strode <rstrode@redhat.com> 2.11.90-1
- Newer upstream version

* Fri Jul 15 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1-1
- Newer upstream version
- Drop upstreamed patch

* Mon May  9 2005 Mark McLoughlin <markmc@redhat.com> 2.10.0-4
- Update to upstream evoldap.schema which uses GNOME's OID base
  rather than Red Hat's OID.

* Wed Apr 27 2005 Mark McLoughlin <markmc@redhat.com> 2.10.0-3
- Fix undefined symbol in the evoldap backend

* Mon Apr 18 2005 Mark McLoughlin <markmc@redhat.com> - 2.10.0-2
- Add evolution mail accounts backend

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> 2.10.0-1
- Update to 2.10.0

* Mon Feb  7 2005 Mark McLoughlin <markmc@redhat.com> 2.9.91-1
- Update to 2.9.91

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> 2.9.2-1
- Update to 2.9.2

* Wed Jan 19 2005 Mark McLoughlin <markmc@redhat.com> 2.8.1-2
- Backport some fixes from upstream CVS

* Tue Oct 12 2004 Mark McLoughlin <markmc@redhat.com> 2.8.1-1
- Update to 2.8.1

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0.1-1
- Update to 2.8.0.1

* Mon Aug 30 2004 Mark McLoughlin <markmc@redhat.com> 2.7.92-1
- Update to 2.7.92

* Thu Aug 19 2004 Mark McLoughlin <markmc@redhat.com> 2.7.91.1-1
- Update to 2.7.91.1

* Wed Aug 18 2004 Mark McLoughlin <markmc@redhat.com> 2.7.91-1
- Update to 2.7.91

* Tue Aug  3 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90
- Add patch to disable merge files for now

* Fri Jul  2 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-7
- Add patch to fix problem when using merged files. Mainly
  neccessary only to work will with GConf 2.8.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Colin Walters <walters@redhat.com> - 2.6.0-5
- Apply patch to move temporary directory creation into daemon,
  needed for SELinux GConf policy

* Wed Apr 14 2004 Warren Togami <wtogami@redhat.com> - 2.6.0-4
- #110724 BR gtk2-devel gettext
- #106283 add versioned ORBit2 minimum
- #112863 own /etc/gconf/2/
- really kill *.la

* Mon Apr  5 2004 Mark McLoughlin <markmc@redhat.com> - 2.6.0-3
- Remove the dont-dump-schema-default patch

* Thu Apr  1 2004 Mark McLoughlin <markmc@redhat.com> - 2.6.0-2
- Backport some fixes from HEAD for lockdown/deployment type stuff 

* Tue Mar 23 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 24 2004 Mark McLoughlin <markmc@redhat.com> 2.5.90-1
- Update to 2.5.90

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Jonathan Blandford <jrb@redhat.com> 2.5.1-1
- new version

* Tue Sep  9 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Thu Aug  7 2003 Jonathan Blandford <jrb@redhat.com>
- begin the move to GNOME-2.4
- locking patch appears to be upstream.  Removing.

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.2.1-3
- Fix libtool

* Mon Jul 14 2003 Havoc Pennington <hp@redhat.com>
- automated rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 2.2.1-1
- upgrade to 2.2.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr  8 2003 Matt Wilson <msw@redhat.com> 2.2.0-2
- use system libtool (#88338)

* Tue Feb  4 2003 Havoc Pennington <hp@redhat.com> 2.2.0-1
- 2.2.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Jan 12 2003 Havoc Pennington <hp@redhat.com>
- 2.1.90

* Fri Jan 10 2003 Havoc Pennington <hp@redhat.com>
- rebuild as libc seems to have changed or something

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- rebuild
- standardize spec file name

* Fri Aug 30 2002 Havoc Pennington <hp@redhat.com>
- add GCONF_LOCAL_LOCKS mode, and syslog encoding patch from tagoh

* Wed Aug 21 2002 Havoc Pennington <hp@redhat.com>
- add dialog to offer to delete gconf locks

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 1.2.1
- include libexecdir stuff

* Wed Jul 31 2002 Havoc Pennington <hp@redhat.com>
- move .pc fle to -devel package

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- fix warning on gnome-panel install

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 1.2.0
- own libdir/GConf/2 directory
- include gtk-doc docs
- don't include static lib for backend modules

* Thu Jun 06 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 1.1.11
- remove AUTHORS for rpmlint

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 1.1.10

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.1.9

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.1.8
- remove .la files

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.1.6
- Rebuild for dependencies

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jan  4 2002 Havoc Pennington <hp@redhat.com>
- 1.1.5.93 snap with important bugfix so gconf actually works

* Thu Jan  3 2002 Havoc Pennington <hp@redhat.com>
- 1.1.5.92 snap with GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

* Thu Jan  3 2002 Havoc Pennington <hp@redhat.com>
- 1.1.5.91 snap with gconf.m4 fix for libgnome

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- since every other build seems to avoid libglib-1.3.so.11, 
  rebuild and hope

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- cvs snap 1.1.5.90

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- GConf 1.1.5, glib 1.3.11

* Sat Oct 27 2001 Havoc Pennington <hp@redhat.com>
- rebuild for glib 1.3.10

* Sun Oct 14 2001 Havoc Pennington <hp@redhat.com>
- 1.1.3

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- cvs snap, remove bonobo-activation deps

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- update to new CVS snap, rebuild

* Mon Sep 17 2001 Havoc Pennington <hp@redhat.com>
- create gconf2 rpm based on gconf1, comment out pofiles 
- include .pc files

* Fri Sep 14 2001 Havoc Pennington <hp@redhat.com>
- fix description/summary

* Fri Aug 31 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Wed Aug 15 2001 Havoc Pennington <hp@redhat.com>
- upgrade to 1.0.4 release I just made
- fixes #51223, syslog spew

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- move gconf-config to devel RPM

* Mon Jul 23 2001 Havoc Pennington <hp@redhat.com>
- how many releases of GConf can I make before it works?

* Sun Jul 22 2001 Havoc Pennington <hp@redhat.com>
- Upgrade to 1.0.2 (which contains only bugfixes that 
  I reviewed and/or wrote myself)

* Wed Jul 18 2001 Havoc Pennington <hp@redhat.com>
- create the /etc/gconf/gconf.xml.defaults directory 

* Fri Jul  6 2001 Alexander Larsson <alexl@redhat.com>
- Install the .la files in the devel package.

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{_tmppath}
- Move the .so files to the devel subpackage
- langify
- Move changelog to the end, where it should be :)
- Don't specify (a bad) doc directory
- Don't define name, version and release and use it in the rpm headers later
- Remove "Packager:"
- s/Copyright/License/

* Fri Jun 22 2001 Havoc Pennington <hp@redhat.com>
- add --direct option to gconftool to avoid spawning oafd,
  then commented out gconftool entirely since it checks
  whether gconfd is running and that spawns oafd anyhow.
  oafd simply needs to exit when unused.

* Tue May 15 2001 Havoc Pennington <hp@redhat.com>
- Fix post, pointed out by Bill

* Mon May 14 2001 Havoc Pennington <hp@redhat.com>
- Upgrade to 1.0.1

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- Import to Red Hat build system.

* Sun Jun 11 2000  Eskil Heyn Olsen <deity@eazel.com>

- Created the .spec file
