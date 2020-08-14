from cpt.packager import ConanMultiPackager
from collections import defaultdict

if __name__ == "__main__":
    builder = ConanMultiPackager(cppstds=[14],
                                archs=["x86_64"],
                                build_types=["Release"])
                              
    builder.add_common_builds(pure_c=False,shared_option_name="gdal:shared") #, build_all_options_values=["gdal:libcurl", "gdal:netcdf"])

    builder.remove_build_if(lambda build: build.settings["compiler.libcxx"] == "libstdc++")

    named_builds = defaultdict(list)
    for settings, options, env_vars, build_requires, reference in builder.items:

        shared="shared"

        if not options['gdal:shared']:
            shared = "static" 

        options["gdal:libcurl"]=True
        options["gdal:netcdf"]=True
        # name = f'{settings['compiler']}_{shared}_libcurl-{options['gdal:libcurl']}_netcdf-{options['gdal:netcdf']}'

        named_builds[settings['compiler']+'_'+shared].append([settings, options, env_vars, build_requires, reference])

    builder.named_builds = named_builds

    builder.run()

