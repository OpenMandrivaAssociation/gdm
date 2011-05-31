Summary: The GNOME Display Manager
Name: gdm
Version: 2.32.2
Release: %mkrel 1
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/projects/gdm/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gdm/%{name}-%{version}.tar.xz
Source1: %gconf-tree.xml
Source2: box.png
Source3: bottom-panel-image.png
#gw are these scripts still needed? Ubuntu has dropped them 
#(replaced  by upstart?)
Source4: gdm-restart
Source5: gdm-safe-restart 
Source6: gdm-stop
# (fc) 2.2.2.1-1mdk change default configuration
Patch0: gdm-2.29.5-defaultconf.patch
Patch2: gdm-2.22.0-fix-linking.patch
# (fc) 2.28.0-1mdv Smooth integration with plymouth (Fedora)
Patch16: gdm-2.32.1-plymouth.patch
# (fc) 2.29.5-1mdv fix loosing keyboard focus (Ubuntu) (GNOME bug #598235)
Patch22: gdm-2.29.5-keyboard-focus.patch
# (fc) 2.29.5-1mdv disable fatal warnings (Ubuntu)
Patch23: gdm-disable-fatal-warnings.patch
# (fc) 2.29.5-1mdv add gconf defaults directory (Ubuntu)
Patch25: gdm-2.31.1-gconf-defaults.patch
# (fc) 2.29.5-1mdv improve greeter transparency (based on OpenSolaris)
Patch26: gdm-2.30.3-improve-greeter-transparency.patch
# (fc) 2.29.92-3mdv handle dmrc migration better (Mdv bug #58414)
Patch27: gdm-2.29.92-dmrc-migration.patch
# (fc) 2.30.0-2mdv ensure X is started on VT7, not VT1 (Ubuntu)
Patch28: 05_initial_server_on_vt7.patch
# (fc) 2.30.0-2mdv check for active VT (Ubuntu)
Patch29: gdm-2.30.0-check-active-vt.patch
# (fc) 2.30.0-3mdv do not restart autologin after logout (GNOME bug #587606)
Patch31: gdm-autologin-once.patch
# (fc) 2.30.0-4mdv run Init scripts as root
Patch33: gdm-2.30.0-init-as-root.patch
# (fc) 2.30.0-9mdv fix locale-archive path (Mdv bug #58507)
Patch34: gdm-2.31.90-fix-locale-archive-path.patch
# (fc) 2.30.2-1mdv fix pam modules (Mdv bug #58459)
Patch35: gdm-2.30.0-fix-pam.patch
# (fc) 2.30.2-1mdv fix notification location (Fedora)
Patch36: gdm-2.30.2-notification-location.patch
# (fc) 2.30.2-1mdv fix tray padding (Fedore)
Patch37: gdm-2.30.2-tray-padding.patch
# (fc) 2.30.2-1mdv add policykit support to GDM settings D-Bus interface (GNOME bug #587750) (Ubuntu)
Patch38: gdm-2.31.1-use-polkit-for-settings.patch
# (fc) 2.30.2-1mdv add more settings configurable for GDM (GNOME bug #587750) (Ubuntu)
Patch39: 09_gdmserver_gconf_settings.patch
# (fc) 2.30.2-1mdv add gdmsetup program (GNOME bug #587750) (Ubuntu)
Patch40: 09_gdmsetup.patch
# (fc) 2.30.2-1mdv group xkb layout (GNOME bug #613681)
Patch41: 33-multi-keyboard-layouts.patch
# (fc) 2.30.2-7mdv allow to set default session with gdmsetup (GNOME bug #594733) (Ubuntu)
Patch44: gdm-2.30.4-default-session-gdmsetup.patch
# (fc) 2.30.2-8mdv save space on low resolutions screen (SUSE)
Patch45: gdm-save-panel-space-on-low-resolutions.patch
# (fc) 2.30.2-9mdv don't try to manage screen if runlevel is 0 or 6 (SUSE)
Patch46: gdm-look-at-runlevel.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root

Provides: dm

Requires(pre):     rpm-helper
Requires(postun):  rpm-helper
Requires(post):	   scrollkeeper >= 0.3
Requires(postun):  scrollkeeper >= 0.3
Requires(post): desktop-common-data
Requires: pam >= 0.99.8.1-8mdv
Requires: setup >= 2.1.9-33mdk
Requires: sessreg
Requires: usermode
Requires: cdialog
Requires: zenity
Requires: gnome-session-bin
Requires: gnome-settings-daemon
Requires: metacity
Suggests: gnome-power-manager
# for XFdrake on failsafe fallback:
Requires: drakx-kbd-mouse-x11
Requires: xinitrc >= 2.4.14
Requires: polkit-gnome
Provides: gdm-Xnest
Obsoletes: gdm-Xnest

Obsoletes: gdm-themes
Conflicts: gdm-220
BuildRequires: x11-server-xorg
BuildRequires: gettext
BuildRequires: pam-devel
#BuildRequires: usermode
BuildRequires: rarian
BuildRequires: gnome-doc-utils
BuildRequires: automake1.9 
BuildRequires: intltool
#BuildRequires: consolekit-devel
BuildRequires: libwrap-devel
BuildRequires: libaudit-devel
#BuildRequires: zenity
BuildRequires: libcanberra-gtk-devel
BuildRequires: libpanel-applet-2-devel
BuildRequires: libxklavier-devel
Buildrequires: UPower-devel
BuildRequires: libcheck-devel
BuildRequires: polkit-1-devel
BuildRequires: libGConf2-devel >= 2.31.3

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%package user-switch-applet
Summary:   GDM User Switcher Panel Applet
Group:     Graphical desktop/GNOME
Requires:  gdm >= %{version}-%{release}
Obsoletes: fast-user-switch-applet
Provides:  fast-user-switch-applet = %{version}-%{release}

%description user-switch-applet
The GDM user switcher applet provides a mechanism for changing among
multiple simulanteous logged in users.

%prep
%setup -q
cp data/Init.in data/Default.in
%patch0 -p1 -b .defaultconf
%patch2 -p1 -b .fixlinking
%patch16 -p1 -b .plymouth
# disabled, cause session warning
#patch22 -p1 -b .keyboard-focus
%patch23 -p1 -b .disable-fatal-warnings
%patch25 -p1 -b .gconf-defaults
%patch26 -p1 -b .improve-greeter-transparency
%patch27 -p1 -b .dmrc-migration
%patch28 -p1 -b .vt7
%patch29 -p1 -b .active-vt
%patch31 -p1 -b .autologin-once
%patch33 -p1 -b .init-as-root
%patch34 -p1 -b .locale-archive
%patch35 -p1 -b .fix-pam
%patch36 -p1 -b .notification-location
%patch37 -p1 -b .tray-padding
%patch38 -p1 -b .polkit-for-settings
%patch39 -p1 -b .gdmserver-gconf-settings
%patch40 -p1 -b .gdmsetup
#do not apply, cause crashes with some keyboard layout, see upstream bug
#patch41 -p1 -b .multi-keyboard-layout
%patch44 -p1 -b .default-session-gdmsetup
%patch45 -p1 -b .low-resolution-screen
%patch46 -p1 -b .look-at-runlevel

libtoolize
autoreconf

%build

%configure2_5x --enable-console-helper  \
  --with-sysconfsubdir=X11/gdm \
  --with-dmconfdir=%_sysconfdir/X11/dm \
  --with-console-kit=yes 

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std PAM_PREFIX=%{_sysconfdir} 

# don't provide PreSession/PostSession, pam handle this
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/PreSession/Default
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/PostSession/Default

install -m644 %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/gdm


mkdir -p $RPM_BUILD_ROOT%{_datadir}/hosts


%{find_lang} %{name} --with-gnome --all-name

for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


mkdir -p $RPM_BUILD_ROOT%{_var}/log/gdm $RPM_BUILD_ROOT%{_sysconfdir}/X11/dm/Sessions

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gdm/.gconf.defaults
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_var}/lib/gdm/.gconf.defaults

install -m755 %{SOURCE4} %{SOURCE5} %{SOURCE6} %buildroot%_sbindir

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
  $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd gdm %{_var}/lib/gdm /bin/false
%_pre_groupadd xgrp gdm

%post

if [ -f /%{_sysconfdir}/X11/xdm/Xsession -a ! -x /%{_sysconfdir}/X11/xdm/Xsession ]; then
	chmod +x /%{_sysconfdir}/X11/xdm/Xsession
fi
if [ -x /usr/sbin/chksession ]; then /usr/sbin/chksession -g || true; fi

%if %mdkversion < 200900
/sbin/ldconfig
%endif
%update_scrollkeeper
%{_sbindir}/gdm-safe-restart >/dev/null 2>&1 || :


%postun
%{make_session}
%_postun_userdel gdm
%_postun_groupdel xgrp gdm
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%clean_scrollkeeper

%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS COPYING NEWS README
%_sysconfdir/dbus-1/system.d/gdm.conf
%{_bindir}/gdm-screenshot
%{_bindir}/gdmflexiserver
%{_bindir}/gdmsetup
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_sbindir}/gdm-restart
%{_sbindir}/gdm-safe-restart
%{_sbindir}/gdm-stop
%dir %{_sysconfdir}/X11/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%config(noreplace) %{_sysconfdir}/X11/gdm/Xsession
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%_sysconfdir/gconf/schemas/gdm-simple-greeter.schemas
%_libexecdir/gdm-crash-logger
%_libexecdir/gdm-factory-slave
%_libexecdir/gdm-host-chooser
%_libexecdir/gdm-product-slave
%_libexecdir/gdm-session-worker
%_libexecdir/gdm-simple-chooser
%_libexecdir/gdm-simple-greeter
%_libexecdir/gdm-simple-slave
%_libexecdir/gdm-xdmcp-chooser-slave
%_libexecdir/gdm-set-default-session
%{_datadir}/pixmaps/*
%{_datadir}/gdm
%{_datadir}/applications/gdmsetup.desktop
%dir %{_datadir}/omf/%name
%{_datadir}/omf/%name/%name-C.omf
%{_datadir}/polkit-1/actions/gdm.policy
%dir %{_datadir}/hosts
%dir %{_localstatedir}/spool/gdm
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.mandatory
%attr(1640, gdm, gdm) %{_localstatedir}/lib/gdm/.gconf.mandatory/*.xml
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.defaults
%attr(1640, gdm, gdm) %{_localstatedir}/lib/gdm/.gconf.defaults/*.xml
%attr(1640, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.path
%attr(1755, gdm, gdm) %dir %{_localstatedir}/run/gdm/greeter
%attr(1777, root, gdm) %dir %{_localstatedir}/run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm

%dir %{_var}/log/gdm
%_datadir/icons/hicolor/*/apps/gdm*
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/applications
%attr(1640, gdm, gdm) %{_localstatedir}/lib/gdm/.local/share/applications/*.*

%files user-switch-applet
%defattr(-, root, root)
%{_libexecdir}/gdm-user-switch-applet
%{_libdir}/bonobo/servers/GNOME_FastUserSwitchApplet.server
%{_datadir}/gnome-2.0/ui/GNOME_FastUserSwitchApplet.xml
