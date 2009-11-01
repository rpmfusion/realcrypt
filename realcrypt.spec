%define _default_patch_fuzz 2

Name: realcrypt
Summary: Cross platform disk encryption software
Version: 6.3
Release: 1%{?dist}
License: TrueCrypt License Version 2.8
Group: Applications/File
URL: http://www.truecrypt.org/
# command to generate tarball without spaces in name
# mv TrueCrypt\ %{version}\ Source.tar.gz trueCrypt-%{version}-source.tar.gz
Source0: trueCrypt-%{version}-source.tar.gz
Source1: ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-11/v2-20/pkcs11.h
Source2: ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-11/v2-20/pkcs11f.h
Source3: ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-11/v2-20/pkcs11t.h
Source4: realcrypt.desktop
Source5: realcrypt.pam
Source6: realcrypt.console.apps
Source7: Readme.txt
# Edited versions of images: license requests that all images be
# replaced in modified versions. These images are re-done completely,
# they share only the same dimensions with the originals. -AdamW
# 2008/08
Source11:	TrueCrypt_Wizard_real.bmp.lzma
Source12:	Textual_logo_96dpi_real.bmp.lzma
Source13:	Textual_logo_288dpi_real.bmp.lzma
Source14:	Drive_icon_96dpi_real.bmp.lzma
Source15:	Drive_icon_mask_96dpi_real.bmp.lzma
Source16:	Logo_288dpi_real.bmp.lzma
Source17:	Logo_96dpi_real.bmp.lzma
Source18:	System_drive_icon_96dpi_real.bmp.lzma
Source19:	System_drive_icon_mask_96dpi_real.bmp.lzma
Source20:	TrueCrypt-16x16_real.xpm.lzma
Source21:	realcrypt_64.png.lzma
Source22:	Textual_logo_background_real.bmp.lzma
Patch1:	realcrypt-rpm_opt_flags.patch
Patch2: realcrypt-%{version}-rebranding.patch
Patch3: realcrypt-no-userguide-menuitem.patch
Patch4: realcrypt-Makefile.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: fuse, pam, usermode, wxGTK >= 2.8.0
BuildRequires: fuse-devel, wxGTK-devel >= 2.8.0
BuildRequires: desktop-file-utils, ImageMagick

%description
Based on TrueCrypt, freely available at http://www.truecrypt.org/.

realcrypt is mainly just a rebrand to allow for modifications to take place,
functionality remains all the same. 

Main Features:
- Creates a virtual encrypted disk within a file and mounts it as a
  real disk.
- Encrypts an entire hard disk partition or a storage device such as
  USB flash drive.
- Encryption is automatic, real-time (on-the-fly) and transparent.
- Provides two levels of plausible deniability, in case an adversary
  forces you to reveal the password:
  1) Hidden volume (steganography).
  2) No RealCrypt volume can be identified (volumes cannot be
  distinguished from random data).
- Encryption algorithms: AES-256, Blowfish (448-bit key), CAST5,
  Serpent, Triple DES, and Twofish. Mode of operation: LRW (CBC
  supported as legacy).

%prep
%setup -q -n truecrypt-%{version}-source
rm -f ./Readme.txt
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE7} .
%patch1 -p1 -b .realcrypt-rpm_opt_flags
%patch2 -p1 -b .realcrypt-%{version}-rebranding
%patch3 -p1 -b .realcrypt-no-userguide-menuitem
%patch4 -p1 -b .realcrypt-Makefile

# Replace graphics which include the TrueCrypt logo
rm -f `find -name *.bmp`
rm -f ./Resources/Icons/TrueCrypt-16x16.xpm
rm -f ./Resources/Icons/TrueCrypt-48x48.xpm
rm -f ./Release/Setup\ Files/TrueCrypt\ User\ Guide.pdf
lzcat %{SOURCE11} > ./Format/TrueCrypt_Wizard.bmp
lzcat %{SOURCE12} > ./Common/Textual_logo_96dpi.bmp
lzcat %{SOURCE13} > ./Common/Textual_logo_288dpi.bmp
lzcat %{SOURCE22} > ./Common/Textual_logo_background.bmp
lzcat %{SOURCE14} > ./Mount/Drive_icon_96dpi.bmp
lzcat %{SOURCE15} > ./Mount/Drive_icon_mask_96dpi.bmp
lzcat %{SOURCE16} > ./Mount/Logo_288dpi.bmp
lzcat %{SOURCE17} > ./Mount/Logo_96dpi.bmp
lzcat %{SOURCE18} > ./Mount/System_drive_icon_96dpi.bmp
lzcat %{SOURCE19} > ./Mount/System_drive_icon_mask_96dpi.bmp
lzcat %{SOURCE20} > ./Resources/Icons/TrueCrypt-16x16.xpm

%build
sed -i -e 's,TrueCrypt,RealCrypt,g' Main/Forms/Forms.cpp Main/Forms/Forms.h Main/LanguageStrings.cpp
sed -i -e 's,namespace RealCrypt,namespace TrueCrypt,g' Main/Forms/Forms.cpp Main/Forms/Forms.h Main/LanguageStrings.cpp

make \
VERBOSE=1 NOSTRIP=1 %{?_smp_mflags}

%check
./Main/realcrypt --text --test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps}
install -D -m755 Main/realcrypt $RPM_BUILD_ROOT%{_sbindir}
install -D -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/realcrypt
install -D -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/realcrypt
# Icon
lzcat %{SOURCE21} > %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
convert -scale 48 %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
# create consolehelper link
ln -sf %{_bindir}/consolehelper $RPM_BUILD_ROOT%{_bindir}/realcrypt

desktop-file-install \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE4}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root,-)
%doc Readme.txt License.txt
%{_bindir}/realcrypt
%{_sbindir}/realcrypt
%config(noreplace) %{_sysconfdir}/pam.d/realcrypt
%config(noreplace) %{_sysconfdir}/security/console.apps/realcrypt
%{_datadir}/icons/hicolor/*/apps/realcrypt.png
%{_datadir}/applications/realcrypt.desktop


%changelog
* Sat Oct 31 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.3-1
- update to 6.3 and fix rebranding patches

* Sun Jul 12 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-8
- replace README.txt
- fix for help menu (link to rpmfusion wiki)

* Fri Jul 10 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-7
- Add patch to remove user guide from menu (patch created by Stewart Adam)
- patch makefile to export APPNAME := realcrypt
- fix description
- add picture to TrueCrypt_Wizard_real.bmp 

* Wed Jul 8 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-6
- rename truecrypt binary

* Wed Jul 8 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-5
- Change source to source0
- fix description
- merge truecrypt changelog

* Sat Jul 4 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-4
- temporary fix for help menu (link to mandriva wiki)
- fix some mistakes in spec file
- merge mandriva spec file by Adam Williamson and rebuild
  branding patch
- add -fno-strict-aliasing to C_CXX_FLAGS in patch

* Fri Jul 3 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-3
- make the recommended changes to the desktop file. 
- change to 48x48 icon and convert it to .png
- add build requires ImageMagick

* Thu Jul 2 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-2
- correct licence version 
- change summary
- add build requires desktop-file-utils

* Tue Jun 30 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2a-1
- update to version 6.2a

* Fri Jun 12 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2-4
- merge spec file from Dominik Mierzejewski (rpm@greysector.net)

* Fri Jun 12 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2-3
- use spec to add pkcs11.h, pkcs11f.h & pkcs11t.h

* Thu Jun 11 2009 Tom Griffiths <linuxtom68@gmail.com> - 6.2-2
- added PAM authentication support, to alleviate the need for use of sudo

* Thu Jun 11 2009 Leigh Scott <leigh123linux@googlemail.com> - 6.2-1
- update to 6.2

* Sun Dec 7 2008 Leigh Scott <leigh123linux@googlemail.com> - 6.1-1
- update to 6.1 , added pkcs11.h, pkcs11f.h & pkcs11t.h to source

* Thu Jul 10 2008 Leigh Scott <leigh123linux@googlemail.com> - 6.0a-2
- added menu laucher & icon

* Wed Jul 9 2008 Levente Farkas <lfarkas@lfarkas.org> - 6.0a-1
- update to 6.0a

* Tue Feb 19 2008 Levente Farkas <lfarkas@lfarkas.org> - 5.0-1
- update to 5.0a

* Tue Feb 12 2008 Levente Farkas <lfarkas@lfarkas.org> - 5.0-2
- update the build for x86_64 and text mode using Tom Horsley's patches from :
  http://home.att.net/~Tom.Horsley/tah-tc-5.0.tar.gz

* Thu Feb  7 2008 Levente Farkas <lfarkas@lfarkas.org> - 5.0-1
- Update to 5.0

