
import os
from fnmatch import fnmatch
from conans import ConanFile, AutoToolsBuildEnvironment, tools, RunEnvironment
from conans.tools import download, unzip

class GdalConan(ConanFile):
    """ Conan package for GDAL """

    name = "gdal"
    version = "2.4.1"
    description = "GDAL - Geospatial Data Abstraction Library"
    url = "http://www.gdal.org/"
    license = "LGPL"
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False], 
               "libcurl": [True, False],
               "netcdf": [True, False] }
    
    default_options = {"shared": True,
     "libcurl": False, 
     "netcdf": False}

    
    exports_sources = ['patches/*']
    exports = ["LICENSE.md"]

    _folder = "gdal-%s" % version


    def requirements(self):
        self.requires("zlib/[>=1.2]")
        self.requires("proj/[>=4 <5]@CHM/stable")
        self.requires("libiconv/1.15")

        if self.options.libcurl:
            self.requires("libcurl/[>=7.70.0]")

        if self.options.netcdf:
            self.requires("netcdf-c/4.6.2@CHM/stable")

        # if not self.options.shared:
        #     self.requires("sqlite3/3.27.1@bincrafters/stable", private=False, override=False)


    def source(self):
        archive_name = "gdal-%s.tar.gz" % self.version
        src_url = "http://download.osgeo.org/gdal/%s/%s" % (self.version, archive_name)

        download(src_url, archive_name)
        unzip(archive_name)
        os.unlink(archive_name)

        tools.replace_in_file("%s/configure" % self._folder, r"-install_name \$rpath/", "-install_name @rpath/")
        tools.replace_in_file("%s/m4/libtool.m4" % self._folder, r"-install_name \$rpath/", "-install_name @rpath/")

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

        if self.options.libcurl:
                    config_args += ["--with-curl="+self.deps_cpp_info["libcurl"].rootpath+'/bin/curl-config']
        else:
                    config_args += ["--without-curl"]

        config_args += ["--with-proj="+self.deps_cpp_info["proj"].rootpath]
        config_args += ["--without-geos"]
        config_args += ["--with-geotiff=internal"]
        config_args += ["--with-hide-internal-symbols"]
        config_args += ["--with-libtiff=internal"]
        config_args += ["--with-libz=internal"]
        config_args += ["--with-libjson-c=internal"]
        config_args += ["--with-threads"]
        config_args += ["--without-bsb"]
        config_args += ["--without-cfitsio"]
        config_args += ["--without-cryptopp"]
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

        if self.options.netcdf:
            config_args += ["--with-netcdf=" + self.deps_cpp_info["netcdf-c"].rootpath ]
        else:
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
        config_args += ["--without-sfcgal"]
        config_args += ["--without-sde"]
        config_args += ["--without-sqlite3"]
        config_args += ["--without-webp"]
        config_args += ["--without-xerces"]
        config_args += ["--without-xml2"]
        config_args += ["--without-crypto"]
        config_args += ["--without-kea"]
        config_args += ["--without-zstd"]

        with tools.chdir(self._folder):

            run_str = './configure ' + ' '.join(config_args)
            

            self.run(run_str, run_environment=True)
            self.run('make', run_environment=True)
            self.run('make install', run_environment=True)

            # env_build = RunEnvironment(self)
            # with tools.environment_append(env_build.vars):

            #     autotools = AutoToolsBuildEnvironment(self)
                
            #         autotools.configure(args=config_args)
            #         autotools.make()
            #         autotools.install()

        if tools.os_info.is_macos:
            for path, subdirs, names in os.walk(os.path.join(self.package_folder, 'lib')):
                for name in names:
                    if fnmatch(name, '*.dylib*'):
                        so_file = os.path.join(path, name)

                        cmd = "install_name_tool -id @rpath/{0} {1}".format(name, so_file)
                        os.system(cmd)



    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["gdal"]
