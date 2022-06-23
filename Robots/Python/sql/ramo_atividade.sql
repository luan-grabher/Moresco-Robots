select
    BDCODEMP,
    BDREFEMP,
    BDCOMERCIO,
    BDINDUSTRIA,
    BDSERVICO
from VEF_BASE_TEMPCADATV AS REF
where
bdrefemp = (select max(bdrefemp) from VEF_BASE_TEMPCADATV where REF.bdcodemp = bdcodemp group by bdcodemp )
GROUP BY
    BDCODEMP,
    BDREFEMP,
    BDCOMERCIO,
    BDINDUSTRIA,
    BDSERVICO