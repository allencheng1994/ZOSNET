class ZSystem:
    def __init__(self, zfile, imh=None, wavelength=None):
        self.__zfile = zfile
        self.__zSystemData = self.__zfile.SystemData
        self.__LDE = self.__zfile.LDE
        self.__imh = imh
        self.__image_plane = self.__LDE.NumberOfSurfaces

        self.__wavelength_init(wavelength)

    def __wavelength_init(self, wavelength):
        max_wave = self.__zSystemData.Wavelengths.NumberOfWavelengths
        if wavelength:
            self.__wavelength = wavelength
            self.__primary_wave_id = len(self.__wavelength) // 2 + 1
        else:
            self.__wavelength = []
            self.__primary_wave_id = len(self.__wavelength) // 2 + 1
            for i in range(max_wave):
                self.__wavelength.append(
                    self.__zSystemData.Wavelengths.GetWavelength(i + 1).Wavelength
                )
                if self.__zSystemData.Wavelengths.GetWavelength(i + 1).IsPrimary:
                    self.__primary_wave_id = i + 1

    def get_wavelength(self):
        return self.__wavelength

    def get_wave_primary_id(self):
        return self.__primary_wave_id

    def get_image_plane(self):
        return self.__image_plane


if __name__ == '__main__':
    from ZOSNET.ZOSCOM import PyZOS

    zmx_file = 'D:\\Lens\\fd-42085A1\\tol\\KEK8_tol67.zmx'

    lens_data = {}
    with PyZOS(zmx_file) as zfile:
        zSystem = ZSystem(zfile)
        lens_data.setdefault('wavelength', zSystem.get_wavelength())
        lens_data.setdefault('primary_wave', zSystem.get_wave_primary_id())
        lens_data.setdefault('image_plane', zSystem.get_image_plane())

    print(lens_data)
