select
colab.BDCODEMP,
count(colab.BDCODCOL)
from VRH_EMP_TCOLCON colab
full join VRH_EMP_TRESCISAO res
on res.bdcodemp = colab.bdcodemp and res.bdcodcol = colab.BDCODCOL
where
res.BDDATARESCISAO IS NULL
group by colab.BDCODEMP