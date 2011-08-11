%define expat_version           1.95.5
%define glib2_version           2.6.0
%define dbus_version            0.90
%define dbus_glib_version       0.70
%define dbus_python_version     0.70
%define pygtk2                  2.0.0
%define gnome_python2           2.0.0
%define udev_version            145
%define util_linux_version      2.12a-16
%define initscripts_version     8.04-1
%define kernel_version          2.6.17
%define gettext_version         0.14.1-14
%define libusb_version          0.1.10a-1
%define pciutils_version        2.2.1
%define dmidecode_version       2.7
%define cryptsetup_luks_version 1.0.1-2
%define pm_utils_version        0.10-1
%define gtk_doc_version         1.4
%define consolekit_version      0.2.0
%define acl_version             2.2.39
%define gperf_version           3.0.1

%define hal_user_uid            68

Summary: Hardware Abstraction Layer
Name: hal
Version: 0.5.14
Release: 8%{?dist}
URL: http://www.freedesktop.org/Software/hal
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.bz2

# OLPC specific, not upstream as is a hack until OFW lands
Source1: 05-olpc-detect.fdi

# Change priority in the init sequence so that HAL loads before any of
# the virt tools.
Patch2: hal-change-priority.patch

# We don't ship dellWirelessCtl -- remove it.
# https://bugzilla.redhat.com/show_bug.cgi?id=488177
Patch4: hal-remove-dell-killswitch.patch

# Identify American Megatrends Inc. Virtual Keyboard and Mouse as an
# evdev device.
# http://lists.freedesktop.org/archives/hal/2009-March/013125.html
Patch9: hal-KVM-evdev.patch

# ThinkPad HDAPS accelerometer is not an input device.
# http://bugs.freedesktop.org/show_bug.cgi?id=22442
Patch11: hal-HDAPS-blacklist.patch

# Un-ignore absolute axes for the Xen Virtual Pointer
# Not required upstream anymore.
# https://bugzilla.redhat.com/show_bug.cgi?id=523914
Patch13: hal-xen-unignore-axes.patch

# Bump HAL_PATH_MAX to 4096 to match upstream.
# Already committed upstream, a2c3dd5a04d79265772c09c4280606d5c2ed72c6
Patch14: hal-0.5.14-use-correct-path-length.patch

# Don't use error prio init and segfault the prober.
# Already committed upstream, dcb2829b8eff61463b0869614ddb07b1c86cecaa
Patch15: hal-0.5.15-no-segfault-probe-input.patch

# Make the initscript LSB compliant. Part of a RHEL initiative.
# Already committed upstream, 18a43206d2f3c1664d853566b2a264dc756ada7e
Patch16: hal-0.5.15-make-initscript-lsb-compliant.patch

# With new dm-udev rules (included since device-mapper 1.02.39) there
# is DM_UDEV_DISABLE_OTHER_RULES_FLAG variable which controls that scan
# should be ignored for this device (it is set for all internal devices,
# including temporary cryptsetup, internal parts of lvm devices etc.)
# See http://article.gmane.org/gmane.linux.hotplug.devel/15936
Patch17: hal-0.5.15-ignore-device-requested-by-DM-udev-rules.patch

# Only allow users at the local console to manipulate devices.
# Not required upstream anymore, as we're using ConsoleKit.
Patch100: hal-use-at-console.patch

License: AFL or GPLv2
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(post): /sbin/ldconfig
Requires(pre): /usr/sbin/useradd
Requires(postun): gawk, grep, coreutils, /sbin/ldconfig
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: python-devel
BuildRequires: hwdata
BuildRequires: gettext >= %{gettext_version}
BuildRequires: dbus-glib >= %{dbus_glib_version}
BuildRequires: perl(XML::Parser)
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: libblkid-devel
BuildRequires: pciutils-devel >= %{pciutils_version}
BuildRequires: xmlto
BuildRequires: gperf >= %{gperf_version}

%ifnarch s390 s390x
BuildRequires: libusb-devel >= %{libusb_version}
%endif
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: glib2 >= %{glib2_version}
Requires: udev >= %{udev_version} 
Requires: util-linux >= %{util_linux_version} 
Requires: initscripts >= %{initscripts_version}
Requires: cryptsetup-luks >= %{cryptsetup_luks_version}
%ifnarch s390 s390x
Requires: pm-utils >= %{pm_utils_version}
%endif 
Conflicts: kernel < %{kernel_version}
%ifnarch s390 s390x
Requires: libusb >= %{libusb_version}
%endif
%ifarch %{ix86} x86_64
Requires: dmidecode >= %{dmidecode_version}
%endif
Requires: ConsoleKit >= %{consolekit_version}
Requires: acl >= %{acl_version}
Requires: hal-libs = %{version}-%{release}
Requires: hal-info
Obsoletes: %{name} < 0.5.9-1
Obsoletes: %{name}-gnome

BuildRequires: autoconf, automake, libtool

%description
HAL is a daemon for collecting and maintaining information from several
sources about the hardware on the system.

%package libs
Summary: Libraries for accessing HAL
Group: Development/Libraries
Requires: dbus >= %{dbus_version}
Obsoletes: %{name} < 0.5.9-1

%description libs
Libraries for accessing HAL.

%package devel
Summary: Libraries and headers for HAL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel >= %{dbus_version}
Requires: pkgconfig

%description devel
Headers and libraries for HAL.

%package docs
Summary: Documentation for HAL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description docs
API docs for HAL.

%package storage-addon
Summary: Storage polling support for HAL
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description storage-addon
Storage polling support for HAL

%prep
%setup -q -n %{name}-%{version}
%patch2 -p1 -b .priority
%patch4 -p1 -b .dell-killswitch
%patch9 -p1 -b .kvm-evdev
%patch11 -p1 -b .hdaps-blacklist
%patch13 -p1 -b .xen-unignore
%patch14 -p1 -b .use-correct-path-len
%patch15 -p1 -b .no-segfault-probe-input
%patch16 -p1 -b .initscript-lsb
%patch17 -p1 -b .ignore-device
%patch100 -p1 -b .drop-polkit

autoreconf -i -f

%build
%configure					\
    --enable-docbook-docs			\
    --docdir=%{_docdir}/%{name}-%{version}	\
    --with-os-type=redhat			\
    --with-udev-prefix=/etc			\
    --disable-console-kit			\
    --disable-policy-kit			\
    --disable-acpi-ibm				\
    --disable-smbios				\
    --enable-umount-helper			\
    --without-usb-csr				\
    --without-cpufreq				\
    --with-eject=%{_sbindir}/eject

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# deprecated keys
cp -p fdi/information/10freedesktop/01-deprecated-keys.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop/

cp README AUTHORS NEWS COPYING HACKING $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# So that this can be %ghost-ed
touch $RPM_BUILD_ROOT%{_localstatedir}/run/hald/acl-list

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "haldaemon" user and group
getent group haldaemon >/dev/null || groupadd -g %{hal_user_uid} -r haldaemon
getent passwd haldaemon >/dev/null || \
	useradd -r -u %{hal_user_uid} -g haldaemon -G haldaemon -d '/' -s /sbin/nologin \
	-c "HAL daemon" haldaemon

%post
/sbin/ldconfig
/sbin/chkconfig --add haldaemon

%preun
if [ $1 = 0 ]; then
    service haldaemon stop > /dev/null 2>&1
    /sbin/chkconfig --del haldaemon
fi

%postun
/sbin/ldconfig
#if [ "$1" -ge "1" ]; then
#  service haldaemon condrestart > /dev/null 2>&1
#fi

%triggerpostun -- hal < 0.5.7-3
#remove lingering fstab-sync entries from /etc/fstab
/bin/cp -f /etc/fstab /etc/fstab.hal-save
(IFS="
"; while read line; do echo $line | awk '{print $4}' | grep -q managed || echo $line | grep -q "^#.*fstab-sync" || echo $line; done < /etc/fstab > fstab.replace)

if [ -s fstab.replace ]; then
  /bin/cp -f fstab.replace /etc/fstab
fi

%triggerpostun -- hal < 0.5.11-0.1.rc1
if [ "$1" -ge "1" ]; then
  mv -uf %{_localstatedir}/lib/hal/acl-list %{_localstatedir}/run/hald 2>/dev/null || :
  rm -rf %{_localstatedir}/lib/hal
fi

%files
%defattr(-,root,root,-)

%doc %dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/NEWS
%doc %{_datadir}/doc/%{name}-%{version}/COPYING
%doc %{_datadir}/doc/%{name}-%{version}/AUTHORS
%doc %{_datadir}/doc/%{name}-%{version}/HACKING
%doc %{_datadir}/doc/%{name}-%{version}/README

%config %{_sysconfdir}/dbus-1/system.d/hal.conf

%config %{_sysconfdir}/rc.d/init.d/haldaemon

%dir %{_sysconfdir}/hal
%{_sysconfdir}/hal/*

/sbin/umount.hal
%{_sbindir}/hald
%{_bindir}/*

%{_libexecdir}/*
%exclude %{_libexecdir}/hald-addon-storage

%dir %{_datadir}/hal
%dir %{_datadir}/hal/fdi
%{_datadir}/hal/fdi/*

%dir %{_libexecdir}/scripts
%{_libexecdir}/scripts/*
%{_mandir}/man1/*
%{_mandir}/man8/*

/etc/udev/rules.d/90-hal.rules

%attr(0700,haldaemon,haldaemon) %dir %{_localstatedir}/cache/hald
%attr(0700,haldaemon,haldaemon) %dir %{_localstatedir}/run/hald
%ghost %{_localstatedir}/run/hald/acl-list

%files libs
%defattr(-,root,root,-)
%{_libdir}/*hal*.so.*

%files devel
%defattr(-,root,root,-)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files docs
%defattr(-,root,root,-)

%doc %dir %{_datadir}/doc/%{name}-%{version}/spec
%doc %{_datadir}/doc/%{name}-%{version}/spec/*

%dir %{_datadir}/gtk-doc/html/libhal
%{_datadir}/gtk-doc/html/libhal/*

%dir %{_datadir}/gtk-doc/html/libhal-storage
%{_datadir}/gtk-doc/html/libhal-storage/*

%files storage-addon
%defattr(-,root,root,-)
%{_libexecdir}/hald-addon-storage

%changelog
* Wed Jul 28 2010 Richard Hughes <rhughes@redhat.com> 0.5.14-8
- Ignore internal DM devices with new DM udev rules.
- Resolves: #613982

* Tue Jul 13 2010 Richard Hughes <rhughes@redhat.com> 0.5.14-7
- Make the initscript more LSB compliant.
- Resolves: #560631

* Thu Jun 17 2010 Richard Hughes <rhughes@redhat.com> 0.5.14-6
- Split out storage-related files in order to avoid unnecessary polling
- Resolves: #571482

* Mon Jun 07 2010 Richard Hughes <rhughes@redhat.com> - 0.5.14-5
- Properly add the haldaemon user this time.
- Resolves: #594305

* Mon Jun 07 2010 Richard Hughes <rhughes@redhat.com> - 0.5.14-4
- Create a haldaemon group in the spec file as shadow-utils has been updated
  and no longer automatically creates a private group for UIDs < 200.
- Resolves: #594305

* Tue May 04 2010 Richard Hughes <rhughes@redhat.com> - 0.5.14-3
- Do not crash if hald-probe-input is run on a device with an unknown type.
- Resolves: #561838

* Thu Feb 25 2010 Richard Hughes <rhughes@redhat.com> - 0.5.14-2
- Use the correct array length to fix a bug when using realpath()
- Resolves: #566709

* Fri Dec 04 2009 Richard Hughes <rhughes@redhat.com> - 0.5.14-1
- New release.
- See http://lists.freedesktop.org/archives/hal/2009-November/013671.html

* Wed Nov 18 2009 Adam Jackson <ajax@redhat.com> 0.5.13-10
- hal-0.5.13-touchpad.patch: Make the logic for input.touchpad match the
  logic in the synaptics driver.

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.5.13-9
- hal-xen-unignore-axes.patch: force evdev to allow rel+abs axes on the Xen
  Virtual Pointer device (#523914)

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.5.13-8
- Use bzipped upstream tarball.

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 0.5.13-7
- Grant root access to devices

* Wed Jul 29 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-6
- Don't compile with csr, ibm or cpufreq options, this functionality is
  obsolete.

* Tue Jul 28 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-5
- Apply a patch to fix mdraid devices.
- Fixes #507782

* Tue Jul 28 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-4
- Fix build harder

* Tue Jul 28 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-3
- Fix file lists to fix build

* Tue Jul 28 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-2
- Drop upstreamed patches to fix build

* Mon Jul 27 2009 Richard Hughes <rhughes@redhat.com> - 0.5.13-1
- Use the release tarball, we did have a release against all the odds.

* Sat Jul 25 2009 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.12-28.20090226git.4
- hal-HDAPS-blacklist.patch: blacklist Thinkpad HDAPS accelerometer device,
  it screws with X (FDO #22442).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-27.20090226git.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 David Zeuthen <davidz@redhat.com> - 0.5.12-26.20090226git.4
- Disable ConsoleKit+PolicyKit support and lock down most interfaces with at_console
- Disable ACL management, this is now handled by udev >= 145

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 0.5.12-26.20090226git.3
- Should not own /etc/dbus-1/system.d

* Tue Jun 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.5.12-26.20090226git.2
- drop Req: libvolume_id dep too

* Mon Jun  9 2009 Matthias Clasen <mclasen@redhat.com> - 0.5.12-26.20090226git.1
- Rebuild against new util-linux-ng
- Drop libvolume_id dep, use libbklkid

* Fri Mar 27 2009 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.12-26.20090226git
- hal-KVM-evdev.patch: force the evdev driver for American Megatrends KVM
  (#484776)

* Sat Mar 14 2009 - Matthew Garrett <mjg@redhat.com> - 0.5.12-25.20090226git
- Fully disable smbios support - backlight control is in-kernel on Dells now.

* Fri Mar 06 2009 - Matthew Garrett <mjg@redhat.com> - 0.5.12-24.20090226git
- Remove Toshiba hotkey support. toshiba_acpi can handle them now.

* Tue Mar 03 2009 - Bastien Nocera <bnocera@redhat.com> - 0.5.12-23.20090226git
- Remove Dell killswitches support, they're handled through the kernel's
  dell_laptop module instead now (#488177), removes requires for smbios-utils

* Tue Mar 03 2009 Peter Hutterer <peter.hutterer@redhat.com>
- purge hal-tablet.patch: fixed upstream in a different manner, see b0a2575f1.

* Sat Feb 28 2009 Richard Hughes <rhughes@redhat.com> - 0.5.12-22.20090226git
- Fix the udev install path, as upstream hal is broken

* Thu Feb 26 2009 Richard Hughes <rhughes@redhat.com> - 0.5.12-21.20090226git
- Update to git snapshot 20090226git
- Remove upstreamed patches
- Disable a patch that should be upstream and no longer applies
- Use the correct loaction for udev rules.d

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-20.20081219git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.12-19.20081219git
- hal-joystick.patch: init bitmask before checking it
- Add hal-tablet.patch: move tablet check out of questionable axis check
- Add hal-tablet-evdev.patch: if it's a tablet, use evdev

* Fri Dec 19 2008 Colin Walters <walters@verbum.org> - 0.5.12-18.20081219git
- Update dbus permissions patch to include KillSwitch which NetworkManager needs

* Fri Dec 19 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-17.20081219git
- Don't run autoreconf in the build-phase, it breaks libtool

* Fri Dec 19 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-16.20081219git
- Update to git snapshot 20081219git

* Tue Dec 09 2008 Colin Walters <walters@verbum.org> - 0.5.12-15
- Add introspection allow

* Mon Dec 01 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-14
- Update to 0.5.12 release candidate 1.

* Mon Nov 24 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-13.20081027git
- For OLPC, set system.firmware.version to the main system firmware version,
  rather than the version of the embedded controller microcode.
  Thanks to Mitch Bradley for the pointer.

* Wed Nov  5 2008 Jeremy Katz <katzj@redhat.com> - 0.5.12-12.20081027git
- Fix up OLPC detection with regard to what's in the upstream kernel

* Wed Nov 05 2008 Matthew Garrett <mjg@redhat.com> - 0.5.12-11.20081027git
- Add support for the memstick bus

* Wed Nov 05 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-10.20081027git
- Add a small FDI file to match OLPC devices so we can remap the keyboard.

* Tue Oct 28 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-9.20081027git
- Remove the newly added BDI devices to fix #468850

* Mon Oct 27 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-8.20081027git
- Update to git snapshot 20081027git to fix #468692

* Mon Oct 22 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-7.20081022git
- Upload correct sources...

* Mon Oct 22 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-6.20081022git
- Update to git snapshot 20081022git

* Tue Oct 21 2008 Matthew Garrett <mjg@redhat.com> - 0.5.12-5.20081013git
- Fix input.joystick handling

* Mon Oct 20 2008 Matthew Garrett <mjg@redhat.com> - 0.5.12-4.20081013git
- Add input.keys capability to appropriate button devices

* Mon Oct 13 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-3.20081013git
- Update to git snapshot 20081013git

* Mon Oct 08 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-2.20081001git
- Add a patch from the mailing list to fix rh#466150

* Mon Oct 06 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-1.20081001git
- Add a patch from the mailing list to try and fix rh#442457

* Wed Oct 01 2008 Richard Hughes <rhughes@redhat.com> - 0.5.12-0.20081001git
- Update to git snapshot 20081001git

* Tue Sep 02 2008 Richard Hughes <rhughes@redhat.com> - 0.5.11-4
- Rebuild for new udev (libvolume_id)

* Tue Jul 22 2008 Jon McCann  <jmccann@redhat.com> - 0.5.11-3
- Fix for CK API changes

* Thu Jun 12 2008 Richard Hughes <rhughes@redhat.com> - 0.5.11-2
- Fix unmounting of USB drives when using SELinux due to a leaking file
  descriptor (#447195)

* Fri May 09 2008 Richard Hughes <rhughes@redhat.com> - 0.5.11-1
- Update to latest upstream release

* Tue Apr 29 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.7.rc2
- Fix addon input cpu eating habits (#437500)

* Thu Apr 17 2008 Bill Nottingham <notting@redhat.com> - 0.5.11-0.6.rc2
- Adjust start/stop priority earlier for use by NetworkManager (#441658)

* Mon Apr  7 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.5.rc2
- Rebuild

* Mon Apr  7 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.4.rc2
- Add deprecated keys back to avoid things like gphoto2 fdi file breakage

* Mon Apr  7 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.3.rc2
- Avoid using at_console since that breaks g-p-m running under gdm

* Tue Mar 18 2008 Jeremy Katz <katzj@redhat.com> - 0.5.11-0.2.rc2
- Fix build errors 

* Tue Mar 18 2008 Jeremy Katz <katzj@redhat.com> - 0.5.11-0.1.rc2
- Update to 0.5.11rc2

* Sat Mar 15 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.5.11-0.1.rc1
- hal-0.5.11rc1
- Move acl list from older versions to proper place
- Fix license tag
- Fix macro use in changelog
- Drop the vio patch
- Nuke rpaths
- Parallel build

* Mon Mar 10 2008 Adam Jackson <ajax@redhat.com> 0.5.11-0.git20080304.4
- hal-0.5.10-set-property-direct.patch: Add --direct option to
  hal-set-property(1).

* Wed Mar  5 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.git20080304.3%{?dist}
- vio support (#431045, thanks dwmw2)

* Tue Mar  4 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.git20080304.2%{?dist}
- Another git snapshot

* Tue Mar  4 2008 David Zeuthen <davidz@redhat.com> - 0.5.11-0.git20080304%{?dist}
- Drop patches as they were committed upstream
- Ship a git snapshot that should fix a number of issues
  - ps3, virtio, iscsi support
  - ACL's are not always restored
  - multiple batteries are shown (and other battery related bugs)
  - /sbin/umount.hal is always returning 1
  - other general bugfixes

* Mon Mar 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.5.10-5%{?dist}
- Require smbios-utils, not libsmbios-bin

* Thu Feb 14 2008 Adam Tkac <atkac redhat com> - 0.5.10-5%{?dist}
- rebuild against new libsmbios

* Tue Jan  8 2008 David Zeuthen <davidz@redhat.com> - 0.5.10-4%{?dist}
- Backport some upstream patches that fixes crashers with fdi files

* Thu Dec  6 2007 David Zeuthen <davidz@redhat.com> - 0.5.10-3%{?dist}
- Grant user 'haldaemon' an authorization to read authorizations of other users

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.10-2
- Rebuild against new dbus-glib

* Thu Oct 11 2007 David Zeuthen <davidz@redhat.com> - 0.5.10-1%{?dist}
- Update to latest upstream release

* Tue Sep 25 2007 - David Zeuthen <davidz@redhat.com> - 0.5.10-0.git20070925%{?dist}
- Update to git snapshot

* Fri Aug 31 2007 - David Zeuthen <davidz@redhat.com> - 0.5.10-0.git20070831%{?dist}
- Update to upstream 0.5.10rc2 release
- Drop patches that are upstream already

* Tue Aug 14 2007 - David Zeuthen <davidz@redhat.com> - 0.5.10-0.git20070731%{?dist}.2
- Require libsmbios-bin on x86 and x86_64

* Thu Aug 09 2007 - David Zeuthen <davidz@redhat.com> - 0.5.10-0.git20070731%{?dist}.1
- Set the correct mode when using open(3p) (Joe Orton)
- Fix bug in implementation of libhal_psi_has_more()

* Tue Jul 31 2007 - David Zeuthen <davidz@redhat.com> - 0.5.10-0.git20070731%{?dist}
- Update to RC1 git snapshot; include PolicyKit support
- Obsolete hal-gnome package as that is dropped upstream (eventually the
  functionality will be replaced by a gnome-device-manager package)
- Drop all patches as they are upstream
- Drop 99-redhat-storage-policy-fixed-drives.fdi; this is now
  controlled by PolicyKit
- Drop use of find_lang; upstream dropped all translations

* Fri May 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.5.9-8
- Really add libsmbios-devel to the BRs not the Requires

* Fri May 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.5.9-7
- Add libsmbios-devel to the BRs so we get Dell backlight support (#239225)

* Wed Apr 25 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-6
- Pick up the latest fixes from 0.5.9 stable branch
- Drop firewire prober patch as this is already in the 0.5.9 stable branch
- Resolves: #237871 (pass correct quirks)

* Wed Apr 18 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.9-5
- Update firewire prober to use correct ioctl codes.

* Tue Apr 17 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-4
- Rebuild without hal-info bits and Require new package hal-info (#230707)

* Thu Apr 12 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-3
- Add patches from 0.5.9 stable branch

* Tue Apr 03 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-2
- Fix a bug with how LUKS interacts with locking
- Obsolete older HAL packages to provide an upgrade path for multilib

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-1
- Update to upstream release 0.5.9 and hal-info 20070402

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070401.2
- Split hal package into hal and hal-libs (#231200)
- Fix hal-device-manager ownership (#234696)

* Sun Apr 01 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070401.1
- Rebuild

* Sun Apr 01 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070401
- Update to hal 0.5.9rc3 and hal-info-20070401
- Drop Fedora eject patch in favor of new --with-eject build option
- Man pages and new tools; notably hal-lock(1) and hal-disable-polling(1)

* Mon Mar 26 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070326
- Update to hal 0.5.9rc2 and hal-info-20070326
- Bring back Fedora eject patch (#231459)
- Build docs and put them in new subpackage hal-docs

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-0.git20070304.fc7.1
- Fix directory ownership issues (#233840)

* Sun Mar  4 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070304
- Update to 0.5.9rc1; notable user visible changes:
- New /sbin/umount.hal helper (#188193)
- Slow down polling if no session is non-idle (#204969)
- Refuse to eject busy devices (#207177)
- Don't mount noexec unless requested
- Use inotify to watch for new fdi files
- Support for new Firewire stack
- BT killswitch for Sony laptops (hadess)
- Pass suspend quirks to pm-utils (need new pm-utils release to use it)

* Sun Feb 18 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070218%{?dist}
- Update to git snapshot (will require SELinux policy changes)
- HAL will now add/remove ACL's for local sessions (needed for f-u-s)
- Add require on acl package for setfacl(1)
- Clean up spec file + incorporate comments from merge review (#225880)

* Tue Feb  6 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070206.1%{?dist}
- Make sure /var/cache/hald exists and has right mode / permissions (notting)

* Tue Feb  6 2007 David Zeuthen <davidz@redhat.com> - 0.5.9-0.git20070206%{?dist}
- Update to git snapshot
- Drop upstreamed patches
- Include hal-info snapshot in this SRPM for now (will be moved to it's 
  own SRPM eventually)
- Require ConsoleKit as this release denies some service to callers
  not originating from an active desktop session (f-u-s requirement)

* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.8.1-8
- Incorporate more feedback from package review

* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.8.1-7
- Use %%find_lang (#161548)
- Correct BuildRoot

* Tue Nov 14 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-6%{?dist}
- Rebuild

* Tue Nov 14 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-5%{?dist}
- Alignment fixes on ia64; Add patch fixing to work with D-Bus 1.0

* Wed Oct 04 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-4%{?dist}
- Make a patch actually apply

* Wed Oct 04 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-3%{?dist}
- Fix whether some PPC boxes can suspend, fixes #208388
- Use /usr/sbin/eject rather than /usr/bin/eject, fixes #208979
- Fix a crasher in partition table probing code, should fix #206669

* Tue Sep 26 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-2%{?dist}
- BuildRequire pciutils-devel

* Tue Sep 26 2006 David Zeuthen <davidz@redhat.com> - 0.5.8.1-1%{?dist}
- upgrade to upstream release 0.5.8.1
- helpers have moved to %%libdir/hal/scripts
- require gtk-doc instead of Doxygen
- drop upstreamed patches
- patch for correctly detecting FUSE mounts (e.g. ntfs-fuse)
- patch for not crashing on optical drives w/o write capabilities
- include devhelp gtk-doc's for libhal, libhal-storage in -devel package
- Require kernel >= 2.6.17, udev >= 089, libvolume_id >= 089
- Build require libvolume_id-devel >= 089
- Should fix #202316, #206669, #207715, #198573, #206732, #208027

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.7.1-3%{?dist}
- Add a .desktop file for hal-device-manager

* Wed Jul 26 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7.1-2%{?dist}
- Bump and rebuild

* Wed Jul 26 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7.1-1
- Point release from upstream that fixes HAL with new kernels
- Up minimum kernel version to 2.6.15

* Mon Jul 24 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-14
- Add patch to handle longer sysfs names
- add dist tag to release

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-13
- BR dbus-glib-devel
- Fix a deprecated function

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.7-12.1
- rebuild

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.7-12
- Add missing BuildRequires

* Wed May 24 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-11
- Updated autofs fix

* Fri May 19 2006 David Zeuthen <davidz@redhat.com> - 0.5.7-10
- Make PCMCIA card readers work again (#185557)

* Wed May 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-9
- Add patch that makes hald not stat nfs and autofs mounts

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-8
- Patch from Brian Pepple <bdpepple@ameritech.net> Add BR for dbus-glib

* Mon May 08 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-7
- Removed typo from spec

* Fri May 05 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-6
- Add fix so gnome-power-manager handles lid opens correctly now

* Mon Apr 24 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-5
- ifnarch the pm-utils requires for s390 and s390x

* Wed Apr 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.7-4
- Add Requires on pm-utils >= 0.10-1 (#185134, Andrew Overholt)

* Fri Mar 03 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-3
- Fix fstab clearing script to not strip whitespace

* Thu Mar 02 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.7-2
- clear out fstab of all fstab-sync entries if previous hal < 0.5.7-2

* Fri Feb 24 2006 David Zeuthen <davidz@redhat.com> - 0.5.7-1
- New upstream version 0.5.7 with several bug fixes
- Don't restart hald on package upgrade
- Pull in dmidecode on x86-ish and x86_64 architectures
- Don't let HAL's Mount() method circumvent system policy (#182352)
- Patch to use new pm-utils's new pm-powersave util properly

* Thu Feb 16 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.7-0.cvs20060213.2
- fix directory ownership
- don't ship static libraries

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 0.5.7-0.cvs20060213.1.1
- rebump for build order issues during double-long bump

* Mon Feb 13 2006 David Zeuthen <davidz@redhat.com> - 0.5.7-0.cvs20060213.1
- fix build

* Mon Feb 13 2006 David Zeuthen <davidz@redhat.com> - 0.5.7-0.cvs20060213
- Upstream CVS snapshot. Drop a patch that is upstream. Switch to using
  udev rules instead of hotplug helpers for udev->hald channel.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.6-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.6-3
- Patch storage-method policy so that the eject method is available
  to audio cd's

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.6-2
- Add policy file to ignore fixed disks.  This is a temporary solution
  until upstream comes up with a more flexable option

* Tue Jan 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.6
- New upstream release
- Remove match on capabilities patch (upstream already)

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 0.5.5.1.cvs20060111-1
- Update to an even newer CVS snapshot, to fix privelege escalation issue
- Remove mount options patch (upstreamed already)

* Mon Jan 09 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1.cvs20060109-2
- Add patch to escape mount options

* Mon Jan 09 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1.cvs20060109-1
- Update to a new CVS snapshot

* Thu Jan 05 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1.cvs20060105-2
- readd the hotplug script

* Thu Jan 05 2006 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1.cvs20060105-1
- Build CVS version of HAL which gives us the new mount support
- disable fstab-sync
- scripts have been moved from /usr/sbin to /usr/share/hal/scripts

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.5.5.1-2.1
- rebuilt

* Wed Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1-2
- Rebuild for dbus 0.60

* Wed Nov 16 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.5.1-1
- Update to latest upstream version

* Fri Nov 11 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.4.cvs2005111-1
- Update to CVS HEAD

* Tue Nov 08 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.4-4
- Add patch to fix storage policy fdi to match on the storage
  capability and not category.
  
* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com>
- Fix a typo in description

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-3
- Rebuild

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-2
- Pull in cryptsetup-luks and fix some unpackaged files

* Tue Aug 30 2005 David Zeuthen <davidz@redhat.com> - 0.5.4-1
- Update to upstream release 0.5.4 and drop patches already upstream

* Thu Aug 11 2005 David Zeuthen <davidz@redhat.com> - 0.5.3-4
- Add patch to make libhal-storage report the right fs usage (#165707)

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 0.5.3-3
- make kernel version requirement a conflicts instead

* Tue Jul 12 2005 David Zeuthen <davidz@redhat.com> 0.5.3-2
- Fix a minor packaging bug

* Tue Jul 12 2005 David Zeuthen <davidz@redhat.com> 0.5.3-1
- Update to upstream release 0.5.3
- Drop patches as they are upstream

* Mon May 23 2005 David Zeuthen <davidz@redhat.com> 0.5.2-2
- Fix doublefree when locking (#158474)
- Never use the 'sync' mount option (#157674)
- Update the fstab-sync man page (#158483)

* Thu May 12 2005 David Zeuthen <davidz@redhat.com> 0.5.2-1
- Update to upstream release 0.5.2

* Wed Apr 27 2005 David Zeuthen <davidz@redhat.com> 0.5.1-1
- Update to upstream release 0.5.1

* Tue Apr 19 2005 Florian La Roche <laroche@redhat.com>
- exclude usb reqs for mainframe (#154616)

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404b-2
- Rebuild

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404b-1
- Use new upstream tarball rather than patching configure

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-3
- Add libusb checks to configure.in

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-2
- Add BuildRequires and Requires for libusb

* Mon Apr  4 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050404-1
- New snapshot from upstream CVS

* Tue Mar 22 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050322b-1
- Another new snapshot from upstream CVS

* Tue Mar 22 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050322-1
- New snapshot from upstream CVS

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050318-1
- Snapshot from upstream CVS; should fix selinux labeling problems
  for /etc/fstab entries

* Thu Mar 10 2005 David Zeuthen <davidz@redhat.com> 0.5.0.cvs20050310-1
- Snapshot from CVS; should fix ACPI issues reported on f-d-l

* Tue Mar  8 2005 David Zeuthen <davidz@redhat.com> 0.5.0-3
- Rebuild

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> 0.5.0-2
- Update to upstream release 0.5.0

* Thu Jan 27 2005 David Zeuthen <davidz@redhat.com> 0.4.7-2
- Add patch that should close #146316

* Mon Jan 24 2005 David Zeuthen <davidz@redhat.com> 0.4.7-1
- New upstream release.
- Should close #145921, #145750, #145293, #145256

* Mon Jan 24 2005 John (J5) Palmieri <johnp@redhat.com> 0.4.6-3
- Update required dbus version to 0.23 

* Thu Jan 20 2005 David Zeuthen <davidz@redhat.com> 0.4.6-2
- Fix parameters to configure

* Thu Jan 20 2005 David Zeuthen <davidz@redhat.com> 0.4.6-1
- New upstream release
- Should close #145099, #144600, #140150, #145223, #137672

* Wed Jan 12 2005 David Zeuthen <davidz@redhat.com> 0.4.5-1
- New upstream release.
- Should close #142834, #141771, #142183

* Fri Dec 12 2004 David Zeuthen <davidz@redhat.com> 0.4.2.cvs20041210-1
- Snapshot from stable branch of upstream CVS

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-8
- Forgot to add some diffs in hal-0.4.0-pcmcia-net-support.patch

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-7
- Change default policy such that non-hotpluggable fixed disks are not
  added to the /etc/fstab file because a) ATARAID detection in hal is
  incomplete (e.g. RAID members from ATARAID controllers might be added
  to /etc/fstab); and b) default install wont corrupt multiboot 
  systems on fixed drives (#137072)

* Tue Oct 26 2004 David Zeuthen <davidz@redhat.com> 0.4.0-6
- Fix hotplug timeout handling (#136626)
- Detect ATARAID devices and do not add /etc/fstab entry for them
- Probe for ext3 before ntfs (#136966)
- Use fstype 'auto' for optical drives instead of 'iso9660,udf'
- Properly detect wireless ethernet devices  (#136591)
- Support 16-bit PCMCIA networking devices (by Dan Williams) (#136658)

* Tue Oct 19 2004 David Zeuthen <davidz@redhat.com> 0.4.0-5
- Make hal work with PCMCIA IDE hotpluggable devices (#133943)
- Fixup URL listed from rpm -qi (#136396)
- Add Portuguese translations for hal
- Fix addition of Russian and Hungarian translations

* Mon Oct 18 2004 David Zeuthen <davidz@redhat.com> 0.4.0-4
- Make hald cope with missing hotplug events from buggy drivers (#135202)
- Fix the order of mount options in fstab-sync (#136191)
- Allow x86 legacy floppy drives in default policy (#133777)
- Fix fstab-sync crashing without any options and not run from hald (#136214)
- man page for fstab-sync references non-existing files (#136026)
- Add Russian translations for hal (#135853)
- Add Hungarian translations for hal

* Fri Oct 15 2004 David Zeuthen <davidz@redhat.com> 0.4.0-3
- Fix bad use of O_NONBLOCK as the 2.6.8-1.624 kernel exposes this (#135886)
- Never use the UUID as mount point candidate in the default policy 
  as it is unfriendly (#135907)
- Fix a trivial bug in fstab-sync so the syslog messages actually expose
  the device name instead of just the word foo

* Thu Oct 14 2004 David Zeuthen <davidz@redhat.com> 0.4.0-2
- Fix issue with fstab-sync not cleaning /etc/fstab on startup

* Thu Oct 14 2004 David Zeuthen <davidz@redhat.com> 0.4.0-1
- Update to upstream stable version 0.4.0
- Remove patch for libhal shutdown since that is now upstream
- fstab-sync: man page, adds comment in /etc/fstab pointing to man page

* Fri Oct 01 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040929-3
- Fix a bug so libhal actually invoke callback functions when needed

* Fri Oct 01 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.98.cvs20040929-2
- Use "user" mount flag for now until "pamconsole" flag gets into mount

* Wed Sep 29 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040929-1
- Update to upstream CVS version
- Enable libselinux again

* Mon Sep 27 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040927-1
- Update to upstream CVS version

* Fri Sep 24 2004 David Zeuthen <davidz@redhat.com> 0.2.98.cvs20040923-1
- Update to upstream CVS release
- Include libhal-storage library
- Should close bug #132876

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-4
- Rebuilt

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-3
- Rebuilt

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-2
- Temporarily disable explicit requirement for libselinux

* Mon Sep 20 2004 David Zeuthen <davidz@redhat.com> 0.2.98-1
- Update to upstream release 0.2.98. 
- Use --with-pid-file so we don't depend on /etc/redhat-release

* Wed Sep 01 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040901-1
- Update to upstream CVS HEAD

* Tue Aug 31 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040831-3
- Add UID for haldaemon user

* Tue Aug 31 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040831-2
- Rebuilt with a newer snapshot.

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-3
- Rebuilt

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-2
- Rebuilt
- Closes RH Bug #130971

* Fri Aug 27 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040827-1
- Update to upstream CVS HEAD. 
- Should close RH Bug #130588

* Wed Aug 25 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-3
- Rebuilt

* Wed Aug 25 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-2
- Apply a patch so hald doesn't hang on startup.

* Mon Aug 23 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040823-1
- Update to upstream CVS HEAD
- Remove symlinking of fstab-sync from specfile since this is now being
  done in the package

* Mon Aug 23 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- change the %%define names to not use "-"

* Thu Aug 19 2004 David Zeuthen <davidz@redhat.com> 0.2.97.cvs20040819-1
- Update to upstream CVS HEAD
- Remove suid patch as it is fixed upstream
- Fix some dependency issues (RH Bug #130202)

* Wed Aug 18 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.97-2
- Add stopgap patch to remove suid from mount flags (RH Bug #130290)

* Mon Aug 16 2004 David Zeuthen <davidz@redhat.com> 0.2.97-1
- update to upstream release 0.2.97
- use kudzu option in fstab-sync since updfstab is now disabled

* Thu Aug 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.96-2
- fixed Requires lines to use %{} instead of ${}
- made dbus related requires lines use the = condition instead of =<
  because the dbus API is still in flux

* Thu Aug 12 2004 David Zeuthen <davidz@redhat.com> 0.2.96
- Update to upstream release 0.2.96
- Symlink fstab-sync into /etc/hal/device.d on install

* Fri Aug 06 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.95.cvs20040802-2
- Base hal package no longer requires python

* Mon Aug 02 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.95.cvs20040802-1
- Update to CVS head
- Remove Dan's patches as they were commited to CVS

* Fri Jul 30 2004 Dan Williams <dcbw@redhat.com> 0.2.93.cvs.20040712-2
- Fix netlink sockets pointer arithmetic bug

* Mon Jul 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.93.cvs.20040712-1
- Update to new CVS version as of 7-12-2004

* Fri Jun 25 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.92.cvs.20040611-2
- take out fstab-update.sh from install
- add to rawhide
 
* Fri Jun 11 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.92.cvs.20040611-1 
- update to CVS head as of 6-11-2004 which contains dcbw's 
  network link status fix 

* Wed Jun 9 2004 Ray Strode <rstrode@redhat.com> 0.2.91.cvs20040527-2
- added dependency on udev

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.91.cvs20040527-1
- update to CVS head as of 5-27-2004 which contains fixes for PCMCIA
  and wireless network devices.

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-3
- added hal-0.2.90.cvs20040511.callbackscripts.patch which installs 
  the file system mounting script in /etc/hal/device.d

* Wed May 12 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-2
- added the %%{_sysconfigdir}/hal directory tree to %files 

* Tue May 11 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90.cvs20040511-1
- update to CVS head as of 5-11-2004

* Wed May 5 2004 Christopher Blizzard <blizzard@redhat.com> 0.2.90-2
- Install hal.dev from /etc/dev.d/default/

* Mon Apr 19 2004 John (J5) Palmieri <johnp@redhat.com> 0.2.90-1
- upstream update

* Mon Apr 19 2004 John (J5) Palmieri <johnp@redhat.com> 0.2-1 
- initial checkin to package repository
- added dependency to the dbus-python package
- added %%{_libexecdir}/hal.dev to teh %%files section
