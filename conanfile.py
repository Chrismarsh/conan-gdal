
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip

class GdalConan(ConanFile):
    """ Conan package for GDAL """

    name = "gdal"
    version = "2.4.1"
    description = "GDAL - Geospatial Data Abstraction Library"
    url = "http://www.gdal.org/"
    license = "LGPL"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}

    

    exports = ["LICENSE.md", "FindGDAL.cmake"]

    _folder = "gdal-%s" % version


    def requirements(self):
        self.requires("zlib/[>=1.2]")
        self.requires("proj/[>=4 <5]@CHM/dev")
        # if not self.options.shared:
        #     self.requires("sqlite3/3.27.1@bincrafters/stable", private=False, override=False)


    def source(self):
        archive_name = "gdal-%s.tar.gz" % self.version
        src_url = "http://download.osgeo.org/gdal/%s/%s" % (self.version, archive_name)

        download(src_url, archive_name)
        unzip(archive_name)
        os.unlink(archive_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self._folder)


    def build(self):
        config_args = ["--with-geos=yes"]
        if self.options.shared:
            config_args += ["--disable-static", "--enable-shared"]
        else:
            config_args += [
                "--without-ld-shared", "--disable-shared", "--enable-static",
            ]
        config_args += ["--with-static-proj4="+self.deps_cpp_info["proj"].rootpath]
        config_args += ["--with-geos"]
        config_args += ["--with-geotiff=internal"]
        config_args += ["--with-hide-internal-symbols"]
        config_args += ["--with-libtiff=internal"]
        config_args += ["--with-libz=internal"]
        config_args += ["--with-threads"]
        config_args += ["--without-bsb"]
        config_args += ["--without-cfitsio"]
        config_args += ["--without-cryptopp"]
        config_args += ["--without-curl"]
        config_args += ["--without-ecw"]
        config_args += ["--without-expat"]
        config_args += ["--without-fme"]
        config_args += ["--without-freexl"]
        config_args += ["--without-gif"]
        config_args += ["--without-gif"]
        config_args += ["--without-gnm"]
        config_args += ["--without-grass"]
        config_args += ["--without-grib"]
        config_args += ["--without-hdf4"]
        config_args += ["--without-hdf5"]
        config_args += ["--without-idb"]
        config_args += ["--without-ingres"]
        config_args += ["--without-jasper"]
        config_args += ["--without-jp2mrsid"]
        config_args += ["--without-jpeg"]
        config_args += ["--without-kakadu"]
        config_args += ["--without-libgrass"]
        config_args += ["--without-libkml"]
        config_args += ["--without-libtool"]
        config_args += ["--without-mrf"]
        config_args += ["--without-mrsid"]
        config_args += ["--without-mysql"]
        config_args += ["--without-netcdf"]
        config_args += ["--without-odbc"]
        config_args += ["--without-ogdi"]
        config_args += ["--without-openjpeg"]
        config_args += ["--without-pcidsk"]
        config_args += ["--without-pcraster"]
        config_args += ["--without-pcre"]
        config_args += ["--without-perl"]
        config_args += ["--without-pg"]
        config_args += ["--without-png"]
        config_args += ["--without-python"]
        config_args += ["--without-qhull"]
        config_args += ["--without-sde"]
        config_args += ["--without-sqlite3"]
        config_args += ["--without-webp"]
        config_args += ["--without-xerces"]
        config_args += ["--without-xml2"]
        config_args += ["--without-crypto"]
        config_args += ["--without-kea"]

        autotools = AutoToolsBuildEnvironment(self)
        with tools.chdir(self._folder):
            autotools.configure(args=config_args)
            autotools.make()
            autotools.install()

        self.run("cp %s/FindGDAL.cmake %s/" % (self.source_folder, self.package_folder))


    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["gdal"]
