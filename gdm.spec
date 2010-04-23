Summary: The GNOME Display Manager
Name: gdm
Version: 2.30.0
Release: %mkrel 6
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/projects/gdm/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gdm/%{name}-%{version}.tar.bz2
Source1: %gconf-tree.xml
Source6: 90-grant-audio-devices-to-gdm.fdi

# (fc) 2.2.2.1-1mdk change default configuration
Patch0: gdm-2.29.5-defaultconf.patch
Patch2: gdm-2.22.0-fix-linking.patch
# (fc) 2.20.4-3mdv grab translation from gtk+mdk for "Welcome to %n" until upstream has enough translations
Patch13: gdm-2.20.4-welcome.patch
# (fc) 2.28.0-1mdv Smooth integration with plymouth (Fedora)
Patch16: gdm-2.30.0-plymouth.patch
# (fc) 2.29.5-1mdv cache ck history (Ubuntu) (GNOME bug #594344)
Patch20: gdm-2.29.5-cache-ck-history.patch
# (fc) 2.29.5-1mdv fix loosing keyboard focus (Ubuntu) (GNOME bug #598235)
Patch22: gdm-2.29.5-keyboard-focus.patch
# (fc) 2.29.5-1mdv disable fatal warnings (Ubuntu)
Patch23: gdm-disable-fatal-warnings.patch
# (fc) 2.29.5-1mdv add gconf defaults directory (Ubuntu)
Patch25: gdm-2.29.5-gconf-defaults.patch
# (fc) 2.29.5-1mdv improve greeter transparency (based on OpenSolaris)
Patch26: gdm-2.29.5-improve-greeter-transparency.patch
# (fc) 2.29.92-3mdv handle dmrc migration better (Mdv bug #58414)
Patch27: gdm-2.29.92-dmrc-migration.patch
# (fc) 2.30.0-2mdv ensure X is started on VT7, not VT1 (Ubuntu)
Patch28: 05_initial_server_on_vt7.patch
# (fc) 2.30.0-2mdv check for active VT (Ubuntu)
Patch29: gdm-2.30.0-check-active-vt.patch
# (fc) 2.30.0-3mdv do not restart autologin after logout (GNOME bug #587606)
Patch31: gdm-autologin-once.patch
# (fc) 2.30.0-3mdv ensure Init/Default is started before autologin
Patch32: gdm-2.30.0-init-before-autologin.patch
# (fc) 2.30.0-4mdv run Init scripts as root
Patch33: gdm-2.30.0-init-as-root.patch

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
#Requires: gnome-settings-daemon
#Requires: metacity
# for XFdrake on failsafe fallback:
Requires: drakx-kbd-mouse-x11
Requires: xinitrc >= 2.4.14
Requires: polkit-gnome
Provides: gdm-Xnest
Obsoletes: gdm-Xnest
#needed by patch13
#Requires: menu-messages
#BuildRequires: X11-static-devel
BuildRequires: x11-server-xorg
BuildRequires: gettext
#BuildRequires: libglade2.0-devel
#BuildRequires: libgnomeui2-devel
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
BuildRequires: libcanberra-devel
BuildRequires: libpanel-applet-2-devel
BuildRequires: libxklavier-devel
Buildrequires: UPower-devel
BuildRequires: libcheck-devel

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
%patch20 -p1 -b .ck-history-cache
# disabled, cause session warning
#patch22 -p1 -b .keyboard-focus
%patch23 -p1 -b .disable-fatal-warnings
%patch25 -p1 -b .gconf-defaults
#%patch13 -p1 -b .welcome
%patch26 -p1 -b .improve-greeter-transparency
%patch27 -p1 -b .dmrc-migration
%patch28 -p1 -b .vt7
%patch29 -p1 -b .active-vt
%patch31 -p1 -b .autologin-once
%patch32 -p1 -b .init-before-autologin
%patch33 -p1 -b .init-as-root

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


mkdir -p $RPM_BUILD_ROOT%{_datadir}/hosts

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdm/themes/mdv-nolist
ln -f -s ../../../mdk/dm/GdmGreeterTheme-nolist.desktop $RPM_BUILD_ROOT%{_datadir}/gdm/themes/mdv-nolist/GdmGreeterTheme.desktop
for i in disconnect.png languages.png sessions.png system.png mdk-gdm-nolist.xml screenshot-gdm-nolist.png ; do
 ln -f -s ../../../mdk/dm/$i $RPM_BUILD_ROOT%{_datadir}/gdm/themes/mdv-nolist/
done


mkdir -p $RPM_BUILD_ROOT%{_datadir}/PolicyKit/policy
install -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/PolicyKit/policy

%{find_lang} %{name} --with-gnome --all-name

for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


mkdir -p $RPM_BUILD_ROOT%{_var}/log/gdm $RPM_BUILD_ROOT%{_sysconfdir}/X11/dm/Sessions

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gdm/.gconf.defaults
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_var}/lib/gdm/.gconf.defaults

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
  $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd gdm %{_var}/lib/gdm /bin/false
%_pre_groupadd xgrp gdm

%post
%define schemas gdm-simple-greeter
%post_install_gconf_schemas %schemas

if [ -f /%{_sysconfdir}/X11/xdm/Xsession -a ! -x /%{_sysconfdir}/X11/xdm/Xsession ]; then
	chmod +x /%{_sysconfdir}/X11/xdm/Xsession
fi
if [ -x /usr/sbin/chksession ]; then /usr/sbin/chksession -g || true; fi

%if %mdkversion < 200900
/sbin/ldconfig
%endif
%update_scrollkeeper
%{_sbindir}/gdm-safe-restart >/dev/null 2>&1 || :


%preun
%preun_uninstall_gconf_schemas %schemas

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
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_sbindir}/gdm-restart
%{_sbindir}/gdm-safe-restart
%{_sbindir}/gdm-stop
%dir %{_sysconfdir}/X11/gdm
%config(noreplace) %{_sysconfdir}/X11/gdm/gdm.schemas
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
%{_datadir}/pixmaps/*
%{_datadir}/gdm
%dir %{_datadir}/omf/%name
%{_datadir}/omf/%name/%name-C.omf
%{_datadir}/PolicyKit/policy/*
%dir %{_datadir}/hosts
%dir %{_localstatedir}/spool/gdm
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.mandatory
%attr(1640, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.mandatory/*.xml
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.defaults
%attr(1640, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.defaults/*.xml
%attr(1640, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.path
%attr(1755, gdm, gdm) %dir %{_localstatedir}/run/gdm/greeter
%attr(1777, root, gdm) %dir %{_localstatedir}/run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm

%dir %{_var}/log/gdm
%_datadir/icons/hicolor/*/apps/gdm*

%files user-switch-applet
%defattr(-, root, root)
%{_libexecdir}/gdm-user-switch-applet
%{_libdir}/bonobo/servers/GNOME_FastUserSwitchApplet.server
%{_datadir}/gnome-2.0/ui/GNOME_FastUserSwitchApplet.xml
