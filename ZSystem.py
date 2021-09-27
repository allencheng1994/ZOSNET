class ZSystem:
    def __init__(self, zfile, imh=None, wavelength=None):
        self.__app = zfile
        self.__TheSystem = self.__app.TheSystem
        self.__MeritOperandType = self.__app.ZOSAPI.Editors.MFE.MeritOperandType
        self.__zSystemData = self.__TheSystem.SystemData
        self.__LDE = self.__TheSystem.LDE
        self.__MFE = self.__TheSystem.MFE
        self.__imh = imh
        self.__nsur = self.__LDE.NumberOfSurfaces

        self.__wavelength_init(wavelength)
        self.__find_stop_surface()

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

    def __find_stop_surface(self):
        self.__stop = 0
        for i in range(self.__nsur):
            if self.__LDE.GetSurfaceAt(i + 1).IsStop:
                self.__stop = i + 1
                break

    def get_mf_value(self, op_type, a1=0, a2=0, hx=0, hy=0, px=0, py=0, ex=0, ey=0):
        return self.__MFE.GetOperandValue(op_type, a1, a2, hx, hy, px, py, ex, ey)

    @property
    def stop_sur(self):
        return self.__stop

    @property
    def ri(self):
        return self.get_mf_value(
            self.__MeritOperandType.RELI, 20, self.__primary_wave_id, 11, 1
        )

    @property
    def op_ttl(self):
        return self.get_mf_value(self.__MeritOperandType.TTHI, 2, self.__nsur - 1)

    @property
    def eflm(self):
        objy = self.get_mf_value(
            self.__MeritOperandType.REAY, 0, self.__primary_wave_id, 0, 0.001, 0, 0
        )

        imhy = self.get_mf_value(
            self.__MeritOperandType.REAY,
            self.__nsur,
            self.__primary_wave_id,
            0,
            0.001,
            0,
            0,
        )

        obj_dist = self.get_mf_value(self.__MeritOperandType.TTHI, 0, 0)

        return abs(imhy / objy * obj_dist)

    @property
    def p1r1_semi(self):
        return self.get_mf_value(self.__MeritOperandType.DMVA, 2)

    def get_fov(self, nominal):
        return self.get_mf_value(
            self.__MeritOperandType.RAID, 1, self.__primary_wave_id, 0, nominal, 0, 0
        )

    def get_mtfs(self, line_pair, field):
        return self.get_mf_value(self.__MeritOperandType.MTFS, 2, 0, field, line_pair)

    def get_mtft(self, line_pair, field):
        return self.get_mf_value(self.__MeritOperandType.MTFT, 2, 0, field, line_pair)

    def get_cra(self, nominal):
        return self.get_mf_value(
            self.__MeritOperandType.RAID,
            self.__nsur,
            self.__primary_wave_id,
            0,
            nominal,
        )


if __name__ == '__main__':
    from ZOSNET.ZOSCOM import PyZOS

    zmx_file = 'D:\\Lens\\fd-42085A1\\tol\\KEK8_tol67.zmx'

    lens_data = {}
    with PyZOS(zmx_file) as zfile:
        zSystem = ZSystem(zfile)
        lens_data.setdefault('ri', zSystem.ri)
        lens_data.setdefault('stop_sur', zSystem.stop_sur)

    print(lens_data)
