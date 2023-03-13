$Env:CONDA_EXE = "/afs/cern.ch/work/c/cdroin/private/DA_study/miniconda/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/afs/cern.ch/work/c/cdroin/private/DA_study/miniconda"
$Env:_CONDA_EXE = "/afs/cern.ch/work/c/cdroin/private/DA_study/miniconda/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs